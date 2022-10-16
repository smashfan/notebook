# -*- coding: utf-8 -*-
"""
Created on Mon Jul  1 2020
@author: LL

Updated on Mon Sep 17 19:02:21 2020
@Stephen Qian
"""
import nnutils.tftools as tt
# tested models
    # 1. keras pretrianed models:
        # 'DenseNet121',  'DenseNet169',  'DenseNet201',
        # 'InceptionResNetV2',  'InceptionV3',
        # 'MobileNet',  'MobileNetV2',
        # 'NASNetLarge', 'NASNetMobile',
        # 'ResNet101', 'ResNet101V2', 'ResNet152', 'ResNet152V2', 'ResNet50', 'ResNet50V2',
        # 'VGG16',  'VGG19',
        # 'Xception',
    # 2 Reomendeation: din
    # 3 EfficientNet: EfficientNetB0 ~ EfficientNetB7
    # 4 NLP: bert

import argparse
parser = argparse.ArgumentParser()

parser.add_argument("-n","--nnname", help="Neural Networkto be parsed",
                    default='VGG16')
parser.add_argument("-b","--batchsize", help="Batch Sized",
                    default=1, type=int)
parser.add_argument("-e","--BPE", help="Byte per element",
                    default=1, type=int)

parser.add_argument("-c","--channel", help="Channels",
                    default=3, type=int)
parser.add_argument("-H","--height", help="Height Size",
                    default=250, type=int)
parser.add_argument("-W","--width", help="Width Size",
                    default=250, type=int)

parser.add_argument("--backward", help="Include Backward Ops", dest='backward', action='store_true')
parser.set_defaults(backward=False)

parser.add_argument("--model", help="name of new model",
                    default='simpleconv', type=str)
args = parser.parse_args()

(model,isconv) = tt.GetModel(vars(args))

# Producing Parameter table of given Model
paralist = tt.ListGen(model,isconv,vars(args))

# exproting tables to //outputs//tf
if args.nnname == 'newmodel':
    nnname = args.model
else:
    nnname = args.nnname
tt.tableExport(paralist,nnname,args.backward)