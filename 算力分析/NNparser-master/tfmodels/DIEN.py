import numpy as np
import tensorflow as tf
import tensorflow.keras.layers as nn

# ============================ Layers  ====================================
class attention(tf.keras.layers.Layer):
    def __init__(self, keys_dim, dim_layers):
        super(attention, self).__init__()
        self.keys_dim = keys_dim

        self.fc = tf.keras.Sequential()
        for dim_layer in dim_layers[:-1]:
            self.fc.add(nn.Dense(dim_layer, activation='sigmoid'))
        self.fc.add(nn.Dense(dim_layers[-1], activation=None))

    def call(self, queries, keys, keys_length):
        queries = tf.tile(tf.expand_dims(queries, 1), [1, tf.shape(keys)[1], 1])
        # outer product ?
        din_all = tf.concat([queries, keys, queries-keys, queries*keys], axis=-1)
        outputs = tf.transpose(self.fc(din_all), [0,2,1])

        # Mask
        key_masks = tf.sequence_mask(keys_length, max(keys_length), dtype=tf.bool)  # [B, T]
        key_masks = tf.expand_dims(key_masks, 1)
        paddings = tf.ones_like(outputs) * (-2 ** 32 + 1)
        outputs = tf.where(key_masks, outputs, paddings)  # [B, 1, T]

        # Scale
        outputs = outputs / (self.keys_dim ** 0.5)

        # Activation
        outputs = tf.keras.activations.softmax(outputs, -1)  # [B, 1, T]

        # Weighted sum
        outputs = tf.squeeze(tf.matmul(outputs, keys))  # [B, H]

        return outputs

class dice(tf.keras.layers.Layer):
    def __init__(self, feat_dim):
        super(dice, self).__init__()
        self.feat_dim = feat_dim
        self.alphas= tf.Variable(tf.zeros([feat_dim]), dtype=tf.float32)
        self.beta  = tf.Variable(tf.zeros([feat_dim]), dtype=tf.float32)

        self.bn = tf.keras.layers.BatchNormalization(center=False, scale=False)

    def call(self, _x, axis=-1, epsilon=0.000000001):

        reduction_axes = list(range(len(_x.get_shape())))
        del reduction_axes[axis]
        broadcast_shape = [1] * len(_x.get_shape())
        broadcast_shape[axis] = self.feat_dim

        mean = tf.reduce_mean(_x, axis=reduction_axes)
        brodcast_mean = tf.reshape(mean, broadcast_shape)
        std = tf.reduce_mean(tf.square(_x - brodcast_mean) + epsilon, axis=reduction_axes)
        std = tf.sqrt(std)
        brodcast_std = tf.reshape(std, broadcast_shape)

        x_normed = self.bn(_x)
        x_p = tf.keras.activations.sigmoid(self.beta * x_normed)

        return self.alphas * (1.0 - x_p) * _x + x_p * _x

def parametric_relu(_x):
    with tf.variable_scope(name_or_scope='', reuse=tf.AUTO_REUSE):
        alphas = tf.get_variable('alpha', _x.get_shape()[-1],
                                 initializer=tf.constant_initializer(0.0),
                                 dtype=tf.float32)
    pos = tf.nn.relu(_x)
    neg = alphas * (_x - abs(_x)) * 0.5

    return pos + neg

class Bilinear(tf.keras.layers.Layer):
    def __init__(self, units):
        super(Bilinear, self).__init__()
        self.linear_act = nn.Dense(units, activation=None, use_bias=True)
        self.linear_noact = nn.Dense(units, activation=None, use_bias=False)

    def call(self, a, b, gate_b=None):
        if gate_b is None:
            return tf.keras.activations.sigmoid(self.linear_act(a) + self.linear_noact(b))
        else:
            return tf.keras.activations.tanh(tf.math.multiply(gate_b, self.linear_noact(b)))

class AUGRU(tf.keras.layers.Layer):
    def __init__(self, units):
        super(AUGRU, self).__init__()

        self.u_gate = Bilinear(units)
        self.r_gate = Bilinear(units)
        self.c_memo = Bilinear(units)

    def call(self, inputs, state, att_score):
        u = self.u_gate(inputs, state)
        r = self.r_gate(inputs, state)
        c = self.c_memo(inputs, state, r)

        u_= att_score * u
        final = (1 - u_) * state + u_ * c

        return final

#  ======================= utils ================================
def calc_auc(raw_arr):
    """Summary
    Args:
        raw_arr (TYPE): Description
    Returns:
        TYPE: Description
    """
    # sort by pred value, from small to big
    arr = sorted(raw_arr, key=lambda d:d[2])

    auc = 0.0
    fp1, tp1, fp2, tp2 = 0.0, 0.0, 0.0, 0.0
    for record in arr:
        fp2 += record[0] # noclick
        tp2 += record[1] # click
        auc += (fp2 - fp1) * (tp2 + tp1)
        fp1, tp1 = fp2, tp2

    # if all nonclick or click, disgard
    threshold = len(arr) - 1e-3
    if tp2 > threshold or fp2 > threshold:
        return -0.5

    if tp2 * fp2 > 0.0:  # normal auc
        return (1.0 - auc / (2.0 * tp2 * fp2))
    else:
        return None

def auc_arr(score_p, score_n):
    score_arr = []
    for s in score_p.numpy():
        score_arr.append([0, 1, s])
    for s in score_n.numpy():
        score_arr.append([1, 0, s])
    return score_arr

def eval(model, test_data):
    auc_sum = 0.0
    score_arr = []
    for u, i, j, hist_i, sl in test_data:
        p_out, p_logit = model(u,i,hist_i,sl)
        n_out, n_logit = model(u,j,hist_i,sl)
        mf_auc = tf.reduce_sum(tf.cast(p_out>n_out, dtype=tf.float32))

        score_arr += auc_arr(p_logit, n_logit)
        auc_sum += mf_auc
    test_gauc = auc_sum / len(test_data)
    auc = calc_auc(score_arr)
    return test_gauc, auc

def sequence_mask(lengths, maxlen=None, dtype=tf.bool):
    """Returns a mask tensor representing the first N positions of each cell.

    If `lengths` has shape `[d_1, d_2, ..., d_n]` the resulting tensor `mask` has
    dtype `dtype` and shape `[d_1, d_2, ..., d_n, maxlen]`, with

    ```
    mask[i_1, i_2, ..., i_n, j] = (j < lengths[i_1, i_2, ..., i_n])
    ```

    Examples:

    ```python
    tf.sequence_mask([1, 3, 2], 5)  # [[True, False, False, False, False],
                                    #  [True, True, True, False, False],
                                    #  [True, True, False, False, False]]
    tf.sequence_mask([[1, 3],[2,0]])  # [[[True, False, False],
                                      #   [True, True, True]],
                                      #  [[True, True, False],
                                      #   [False, False, False]]]
    ```

    Args:
        lengths: integer tensor, all its values <= maxlen.
        maxlen: scalar integer tensor, size of last dimension of returned tensor.
            Default is the maximum value in `lengths`.
        dtype: output type of the resulting tensor.
        name: name of the op.

    Returns:
        A mask tensor of shape `lengths.shape + (maxlen,)`, cast to specified dtype.
    Raises:
        ValueError: if `maxlen` is not a scalar.
    """
    # lengths = lengths.numpy()

    if maxlen is None:
        maxlen = max(lengths)
    # else:
    #     maxlen = maxlen
    # if maxlen.get_shape().ndims is not None and maxlen.get_shape().ndims != 0:
    #     raise ValueError("maxlen must be scalar for sequence_mask")

    # The basic idea is to compare a range row vector of size maxlen:
    # [0, 1, 2, 3, 4]
    # to length as a matrix with 1 column: [[1], [3], [2]].
    # Because of broadcasting on both arguments this comparison results
    # in a matrix of size (len(lengths), maxlen)
    row_vector = range(maxlen)
    # Since maxlen >= max(lengths), it is safe to use maxlen as a cast
    # authoritative type. Whenever maxlen fits into tf.int32, so do the lengths.
    matrix = np.expand_dims(lengths, -1)
    result = row_vector < matrix

    if dtype is None:
        return tf.convert_to_tensor(result)
    else:
        return tf.cast(tf.convert_to_tensor(result), dtype)

# ===================== models =======================
class Base(tf.keras.Model):
    def __init__(self, user_count, item_count, cate_count, cate_list,
                       user_dim, item_dim, cate_dim,
                       dim_layers):
        super(Base, self).__init__()
        self.item_dim = item_dim
        self.cate_dim = cate_dim

        self.user_emb = nn.Embedding(user_count, user_dim)
        self.item_emb = nn.Embedding(item_count, item_dim)
        self.cate_emb = nn.Embedding(cate_count, cate_dim)
        self.item_bias= tf.Variable(tf.zeros([item_count]), trainable=True)
        self.cate_list = cate_list

        self.hist_bn = nn.BatchNormalization()
        self.hist_fc = nn.Dense(item_dim+cate_dim)

        self.fc = tf.keras.Sequential()
        self.fc.add(nn.BatchNormalization())
        for dim_layer in dim_layers[:-1]:
            self.fc.add(nn.Dense(dim_layer, activation='sigmoid'))
        self.fc.add(nn.Dense(dim_layers[-1], activation=None))

    def get_emb(self, user, item, history):
        user_emb = self.user_emb(user)

        item_emb = self.item_emb(item)
        item_cate_emb = self.cate_emb(tf.gather(self.cate_list, item))
        item_join_emb = tf.concat([item_emb, item_cate_emb], -1)
        item_bias= tf.gather(self.item_bias, item)

        hist_emb = self.item_emb(history)
        hist_cate_emb = self.cate_emb(tf.gather(self.cate_list, history))
        hist_join_emb = tf.concat([hist_emb, hist_cate_emb], -1)

        return user_emb, item_join_emb, item_bias, hist_join_emb

    def call(self, user, item, history, length):
        user_emb, item_join_emb, item_bias, hist_join_emb = self.get_emb(user, item, history)

        hist_mask = tf.sequence_mask(length, max(length), dtype=tf.float32)
        hist_mask = tf.tile(tf.expand_dims(hist_mask, -1), (1,1,self.item_dim+self.cate_dim))
        hist_join_emb = tf.math.multiply(hist_join_emb, hist_mask)
        hist_join_emb = tf.reduce_sum(hist_join_emb, 1)
        hist_join_emb = tf.math.divide(hist_join_emb, tf.cast(tf.tile(tf.expand_dims(length, -1),
                                                      [1,self.item_dim+self.cate_dim]), tf.float32))

        hist_hid_emb = self.hist_fc(self.hist_bn(hist_join_emb))
        join_emb = tf.concat([user_emb, item_join_emb, hist_hid_emb], -1)

        output = tf.squeeze(self.fc(join_emb)) + item_bias
        logit = tf.keras.activations.sigmoid(output)

        return output, logit


class DIN(Base):
    def __init__(self, user_count, item_count, cate_count, cate_list,
                       user_dim, item_dim, cate_dim,
                       dim_layers):
        super(DIN, self).__init__(user_count, item_count, cate_count, cate_list,
                                  user_dim, item_dim, cate_dim,
                                  dim_layers)

        self.hist_at = attention(item_dim+cate_dim, dim_layers)

        self.fc = tf.keras.Sequential()
        self.fc.add(nn.BatchNormalization())
        for dim_layer in dim_layers[:-1]:
            self.fc.add(nn.Dense(dim_layer, activation=None))
            self.fc.add(dice(dim_layer))
        self.fc.add(nn.Dense(dim_layers[-1], activation=None))

    def call(self, user, item, history, length):
        user_emb, item_join_emb, item_bias, hist_join_emb = self.get_emb(user, item, history)

        hist_attn_emb = self.hist_at(item_join_emb, hist_join_emb, length)
        hist_attn_emb = self.hist_fc(self.hist_bn(hist_attn_emb))

        join_emb = tf.concat([user_emb, item_join_emb, hist_attn_emb], -1)

        output = tf.squeeze(self.fc(join_emb)) + item_bias
        logit = tf.keras.activations.sigmoid(output)

        return output, logit

class DIEN(Base):
    def __init__(self, user_count, item_count, cate_count, cate_list,
                       user_dim, item_dim, cate_dim,
                       dim_layers):
        super(DIEN, self).__init__(user_count, item_count, cate_count, cate_list,
                                   user_dim, item_dim, cate_dim,
                                   dim_layers)

        self.hist_gru = nn.GRU(item_dim+cate_dim, return_sequences=True)
        self.hist_augru = AUGRU(item_dim+cate_dim)

    def call(self, user, item, history, length):
        user_emb, item_join_emb, item_bias, hist_join_emb = self.get_emb(user, item, history)

        hist_gru_emb = self.hist_gru(hist_join_emb)
        hist_mask = tf.sequence_mask(length, max(length), dtype=tf.bool)
        hist_mask = tf.tile(tf.expand_dims(hist_mask, -1), (1,1,self.item_dim+self.cate_dim))
        hist_attn = tf.nn.softmax(tf.matmul(tf.expand_dims(item_join_emb, 1), hist_gru_emb, transpose_b=True))

        hist_hid_emb = tf.zeros_like(hist_gru_emb[:,0,:])
        for in_emb, in_att in zip(tf.transpose(hist_gru_emb, [1,0,2]),
                                  tf.transpose(hist_attn, [2,0,1])):
            hist_hid_emb = self.hist_augru(in_emb, hist_hid_emb, in_att)

        join_emb = tf.concat([user_emb, item_join_emb, hist_hid_emb], -1)

        output = tf.squeeze(self.fc(join_emb)) + item_bias
        logit = tf.keras.activations.sigmoid(output)

        return output, logit
