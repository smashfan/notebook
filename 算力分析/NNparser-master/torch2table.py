# -*- coding: utf-8 -*-
"""
Created on Mon Jul 5 2020

@author: LL
"""
import nnutils.pytools as pt

# Tested Models
# 1. torchvision:
#   alexnet, vgg11, vgg13, vgg16, vgg19, vgg11_bn, vgg13_bn, vgg16_bn,
#   vgg19_bn, resnet18, resnet34, resnet50, resnet101, resnet152, googlenet
#   squeezenet1_0, squeezenet1_1, mobilenet_v2,
#   densenet121, densenet161, densenet169, densenet_201,
#   resnext50_32x4d, resnext101_32x8d, wide_resnet50_2, wide_resnet101_2
#   mnasnet'n'_'n', shufflenet_v2_x'n'_'n',
# 2. Recomendation: dlrm
# 3. Detection: maskrcnn, ssd_mobilenet, ssd_r34
# 4. RNN: lstm, gru
# 5. NLP: gnmt

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-n","--nnname", help="Neural Network to be parsed",
                    default='resnet50')
parser.add_argument("-b","--batchsize", help="Batch Size",
                    default=1, type=int)
parser.add_argument("-e","--BPE", help="Byte per element",
                    default=1, type=int)

parser.add_argument("-c","--channel", help="Channels",
                    default=3, type=int)
parser.add_argument("-H","--height", help="Height Size",
                    default=224, type=int)
parser.add_argument("-W","--width", help="Width Size",
                    default=224, type=int)
parser.add_argument("--backward", help="Include Backward Ops", dest='backward', action='store_true')
parser.set_defaults(backward=False)
parser.add_argument("--model", help="name of new model",
                    default='ssd_mob', type=str)
args = parser.parse_args()


# producing the table of the model paramter list
(ms, depth, isconv,y) = pt.modelLst(vars(args))
ms = pt.tableGen(ms,depth,isconv)

# exporting the table at //output//torch//
if args.nnname == 'newmodel':
    nnname = args.model
else:
    nnname = args.nnname

pt.tableExport(ms,nnname,y,args.backward)