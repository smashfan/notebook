# Copyright 2018 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""NCF framework to train and evaluate the NeuMF model.

The NeuMF model assembles both MF and MLP models under the NCF framework. Check
`neumf_model.py` for more details about the models.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import json
import os

# pylint: disable=g-bad-import-order
from absl import app
from absl import flags
from absl import logging
import tensorflow.compat.v2 as tf
# pylint: enable=g-bad-import-order

from official.recommendation import constants as rconst
from official.recommendation import movielens
from official.recommendation import ncf_common
from official.recommendation import ncf_input_pipeline
from official.recommendation import neumf_model
from official.utils.flags import core as flags_core
from official.utils.misc import distribution_utils
from official.utils.misc import keras_utils
from official.utils.misc import model_helpers


FLAGS = flags.FLAGS


def metric_fn(logits, dup_mask, match_mlperf):
  dup_mask = tf.cast(dup_mask, tf.float32)
  logits = tf.slice(logits, [0, 1], [-1, -1])
  in_top_k, _, metric_weights, _ = neumf_model.compute_top_k_and_ndcg(
      logits,
      dup_mask,
      match_mlperf)
  metric_weights = tf.cast(metric_weights, tf.float32)
  return in_top_k, metric_weights


class MetricLayer(tf.keras.layers.Layer):
  """Custom layer of metrics for NCF model."""

  def __init__(self, match_mlperf):
    super(MetricLayer, self).__init__()
    self.match_mlperf = match_mlperf

  def get_config(self):
    return {"match_mlperf": self.match_mlperf}

  @classmethod
  def from_config(cls, config, custom_objects=None):
    return cls(**config)

    #0606: training -> istraining; training is a tf varible in base layer, 
    # not reset in debug mode, cause tyep mismatch error
  def call(self, inputs, istraining=False):
    logits, dup_mask = inputs
    if istraining:
      hr_sum = 0.0
      hr_count = 0.0
    else:
      metric, metric_weights = metric_fn(logits, dup_mask, self.match_mlperf)
      hr_sum = tf.reduce_sum(metric * metric_weights)
      hr_count = tf.reduce_sum(metric_weights)

    self.add_metric(hr_sum, name="hr_sum", aggregation="mean")
    self.add_metric(hr_count, name="hr_count", aggregation="mean")
    return logits


class LossLayer(tf.keras.layers.Layer):
  """Pass-through loss layer for NCF model."""

  def __init__(self, loss_normalization_factor):
    # The loss may overflow in float16, so we use float32 instead.
    super(LossLayer, self).__init__(dtype="float32")
    self.loss_normalization_factor = loss_normalization_factor
    self.loss = tf.keras.losses.SparseCategoricalCrossentropy(
        from_logits=True, reduction="sum")

  def get_config(self):
    return {"loss_normalization_factor": self.loss_normalization_factor}

  @classmethod
  def from_config(cls, config, custom_objects=None):
    return cls(**config)

  def call(self, inputs):
    logits, labels, valid_pt_mask_input = inputs
    loss = self.loss(
        y_true=labels, y_pred=logits, sample_weight=valid_pt_mask_input)
    loss = loss * (1.0 / self.loss_normalization_factor)
    self.add_loss(loss)
    return logits


class IncrementEpochCallback(tf.keras.callbacks.Callback):
  """A callback to increase the requested epoch for the data producer.

  The reason why we need this is because we can only buffer a limited amount of
  data. So we keep a moving window to represent the buffer. This is to move the
  one of the window's boundaries for each epoch.
  """

  def __init__(self, producer):
    self._producer = producer

  def on_epoch_begin(self, epoch, logs=None):
    self._producer.increment_request_epoch()


class CustomEarlyStopping(tf.keras.callbacks.Callback):
  """Stop training has reached a desired hit rate."""

  def __init__(self, monitor, desired_value):
    super(CustomEarlyStopping, self).__init__()

    self.monitor = monitor
    self.desired = desired_value
    self.stopped_epoch = 0

  def on_epoch_end(self, epoch, logs=None):
    current = self.get_monitor_value(logs)
    if current and current >= self.desired:
      self.stopped_epoch = epoch
      self.model.stop_training = True

  def on_train_end(self, logs=None):
    if self.stopped_epoch > 0:
      print("Epoch %05d: early stopping" % (self.stopped_epoch + 1))

  def get_monitor_value(self, logs):
    logs = logs or {}
    monitor_value = logs.get(self.monitor)
    if monitor_value is None:
      logging.warning("Early stopping conditioned on metric `%s` "
                      "which is not available. Available metrics are: %s",
                      self.monitor, ",".join(list(logs.keys())))
    return monitor_value


def _get_keras_model(params):
  """Constructs and returns the model."""
  batch_size = params["batch_size"]

  user_input = tf.keras.layers.Input(
      shape=(1,), name=movielens.USER_COLUMN, dtype=tf.int32)

  item_input = tf.keras.layers.Input(
      shape=(1,), name=movielens.ITEM_COLUMN, dtype=tf.int32)

  valid_pt_mask_input = tf.keras.layers.Input(
      shape=(1,), name=rconst.VALID_POINT_MASK, dtype=tf.bool)

  dup_mask_input = tf.keras.layers.Input(
      shape=(1,), name=rconst.DUPLICATE_MASK, dtype=tf.int32)

  label_input = tf.keras.layers.Input(
      shape=(1,), name=rconst.TRAIN_LABEL_KEY, dtype=tf.bool)

  base_model = neumf_model.construct_model(user_input, item_input, params)

  logits = base_model.output

  zeros = tf.keras.layers.Lambda(
      lambda x: x * 0)(logits)

  softmax_logits = tf.keras.layers.concatenate(
      [zeros, logits],
      axis=-1)

  # Custom training loop calculates loss and metric as a part of
  # training/evaluation step function.
  if not params["keras_use_ctl"]:
    softmax_logits = MetricLayer(
        params["match_mlperf"])([softmax_logits, dup_mask_input])
    # TODO(b/134744680): Use model.add_loss() instead once the API is well
    # supported.
    softmax_logits = LossLayer(batch_size)(
        [softmax_logits, label_input, valid_pt_mask_input])

  keras_model = tf.keras.Model(
      inputs={
          movielens.USER_COLUMN: user_input,
          movielens.ITEM_COLUMN: item_input,
          rconst.VALID_POINT_MASK: valid_pt_mask_input,
          rconst.DUPLICATE_MASK: dup_mask_input,
          rconst.TRAIN_LABEL_KEY: label_input},
      outputs=softmax_logits)

  return base_model, keras_model


def run_ncf(_):
  """Run NCF training and eval with Keras."""

  model_helpers.apply_clean(FLAGS)

  params = ncf_common.parse_flags(FLAGS)
  '''
  params["distribute_strategy"] = strategy'''

  #num_users, num_items, _, _, producer = ncf_common.get_inputs(params)
  num_users, num_items = 6040,3706 # dummy values from original dataset
  params["num_users"], params["num_items"] = num_users, num_items

  infermodel,trainmodel = _get_keras_model(params)
    # optimizer = tf.keras.optimizers.Adam(
    #     learning_rate=params["learning_rate"],
    #     beta_1=params["beta1"],
    #     beta_2=params["beta2"],
    #     epsilon=params["epsilon"])
   
  return infermodel,trainmodel

def ncfmodel(istrain=False):
    ncf_common.define_ncf_flags()
    infermodel,trainmodel = run_ncf(FLAGS)
    if istrain:
        model=trainmodel
    else:
        model = infermodel
    return model

def main(_):
    model = run_ncf(FLAGS)
    model.summary()
  #logging.info("Result is %s", run_ncf(FLAGS))

if __name__ == "__main__":
  ncf_common.define_ncf_flags()
  app.run(main)
