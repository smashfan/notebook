# -*- coding: utf-8 -*-
"""
Created on Mon Jul  6 10:33:46 2020
@author: LL

Updated on Mon Sep 16 17:00:31 2020
@Stephen Qian
"""
import tensorflow.keras as keras
import numpy as np
import pandas as pd
import nnutils.formattable as ft


def headgen(isconv):
    # todo: adjust the names according to models
    header = ['Layer', 'Type']
    header0 = ['Layer Hierarchy'] * 2
    if isconv:
        dim = 3 # 4 dim tensor: BHWC, no B
        feat_dim = ['Height', 'Width', 'Channel'] * 3
        feat_dim0 = ['Input Dim (Weight)'] * dim + ['Input Dim (Bias)'] * dim + ['Output Dimension'] * dim
        lweights = ['Height', 'Width', 'X', 'Y', 'X', 'Y'] # kernel, stride, padding
        lweights0 = ['Kernel'] * 2 + ['Stride'] * 2 + ['Padding'] * 2
    else:
        dim = 2 # 3 dim: B+ 1XW vector,no B
        feat_dim = ['Height', 'Width'] * 3
        feat_dim0 = ['Input Dim (Weight)'] * dim + ['Input Dim (Bias)'] * dim + ['Output Dimension'] * dim
        lweights = []
        lweights0 = []

    header.extend(feat_dim + lweights)
    header.extend(['Input', 'Output', 'Weight'] + ['GEMM', 'ElemWise', 'Activation'] * 2)
    header0.extend(feat_dim0 + lweights0)
    header0.extend(['Size of Parameters'] * 3 + ['Forward Ops'] * 3 + ['Backward Ops'] * 3)
    return [header0, header]

def inputgen(x,inp0,inp1,extin):
    # input tensors
    if not isinstance(x.input, list): # single input
        datai0=1
        for i in range(1,4):
            try:
                inp0[i-1]=x.input.shape[i]
            except IndexError:
                None
        for item in inp0:
            if isinstance(item,int):
                datai0=datai0*item
        datai=(datai0)
    elif len(x.input)>1:       # 2 inputs
        datai0=1
        for i in range(1,4):
            try:
                inp0[i-1]=x.input[0].shape[i]
            except IndexError:
                None
        for item in inp0:
            if isinstance(item,int):
                datai0=datai0*item
        datai1=1
        for i in range(1,4):
            try:
                inp1[i-1]=x.input[1].shape[i]
            except IndexError:
                None
        for item in inp1:
            if isinstance(item,int):
                datai1=datai1*item
        datai=(datai0+datai1)
        if len(x.input)>2:
            for inp in x.input_shape[2:]:
                tmp = inp[1:]
                dtmp = 1
                for item in tmp:
                    if isinstance(item,int):
                        dtmp=dtmp*item
                datai += dtmp
                extin = extin + str(tmp) + ', '
            extin = extin[:-1]
    return inp0,inp1,datai,extin

def outputgen(x,out,extin):
    # output:
    if not isinstance(x.output, list):
        # single output：2d vector or 4d tensor: batch x oh x ow x oc
        datao=1
        for i in range(1,4):
            try:
                out[i-1]=x.output.shape[i]
            except IndexError:
                None
        for item in out:
            if isinstance(item,int):
                datao=datao*item
    else: # output0,size of more outputs
        datao=1
        for i in range(1,4):
            try:
                out[i-1]=x.output[0].shape[i]
            except IndexError:
                None
        for item in out:
            if isinstance(item,int):
                datao=datao*item
        if len(x.output)>1:
            extin += ';' # addtional output
        for i in range(1,len(x.output),1):
            dtmp=1
            tmp=x.output[i].shape
            for item in tmp:
                if isinstance(item,int):
                    dtmp=dtmp*item
            datao +=dtmp
            extin += str(tmp) + ','
        extin = extin[:-1]
    ltype = str(type(x)).split(".")[-1].split("'")[0]
    if ltype:
        if ltype=='MultiHeadAttention': #attentio layer
            # outputs: features of a sentence
            seqlen = x.input_shape[1]
            datao= datao*seqlen
            out[0] = seqlen # to fix output dim1 = None

    return out,datao,extin

def getweightsize(x,dataw):
    weights=x.get_weights()
    if len(weights)>0:
        dataw=0
        for item in weights:
            dataw += int(np.prod(item.shape))
    return dataw

def opscomputation(x,datao,inp0):
    ltype = str(type(x)).split(".")[-1].split("'")[0]
    gemm, vect, acti, gemmB, vectB, actiB = '','','','','',''
    if ltype:
        if ltype=='BatchNormalization': # BN
            vect = datao*2 #1 elem* 1elem+
            vectB = vect
        elif ltype=='Add': #add layer
            vect = datao # output tensor size
            vectB = vect
        elif ltype=='LayerNormalization': #add layer
            acti = datao # output tensor size
            actiB = acti
        elif ltype=='MultiHeadAttention': #attention layer
            head = x.head_num
            seqlen,emblen = inp0[:2]
            keylen =emblen//head # feature_dim
            gemm=0; vect=0; acti=0
            #one head of one sentence
            ub = 1 if x.use_bias else 0
            # Q*K'= X*W_q*W_k'*X'
            QS = seqlen*emblen*keylen + seqlen*keylen*ub # size: seqlen*keylen
            KS = seqlen*emblen*keylen + seqlen*keylen*ub # size: seqlen*keylen
            gemm += QS+KS + seqlen*keylen*seqlen
            # / sqrt(kenlen)
            vect += seqlen*seqlen
            # softmax
            acti += seqlen*seqlen
            # f(Q*K') * (x*W_v), Wv emblen*keylen (same dim on W_q,W_k,W_v)
            VS = seqlen*emblen*keylen + seqlen*keylen*ub # V: seqlen*keylen
            FV = seqlen*seqlen*keylen # F(QK)*V: seqlen*keylen
            gemm += VS+FV
            gemmoh = gemm
            vectoh = vect
            actioh = acti
            # multihead
            # concate
            keylen=keylen*head
            gemm = gemm*head
            vect = vect*head
            acti = acti*head
            # x*W_o
            gemm += seqlen*keylen*emblen + seqlen*emblen*ub
            gemm = [gemmoh, gemm]
            vect = [vectoh,vect]
            acti = [actioh, acti]
            # TODO add backprop

        elif ltype=='LayerNormalization': #attention layer
            seqlen,emblen = inp0[:2]
            vect=0; acti=0
            #  along last dim, emb dim
            # mean
            vect += (seqlen-1)
            # var:sum(x*x-mx)
            vect += (seqlen*3-1)
            # std: sqrt(var+epsi)
            vect += (seqlen)
            acti += (seqlen)
            # output:( x-mx)/std
            vect += (seqlen*2)

        elif ltype=='FeedForward': #attention layer
            seqlen,emblen = inp0[:2]
            units=x.units
            gemm=0; acti=0
            ub = 1 if x.use_bias else 0
            # w1x+b
            gemm += seqlen*emblen*units +seqlen*units*ub
            acti += seqlen*units #gelu
            # w2x+b
            gemm += seqlen*units*emblen +seqlen*emblen*ub
            acti += seqlen*emblen

        elif ltype=='Dense':
            lens = x.input_shape[1]
            ub = 1 if x.use_bias else 0
            units=x.units
            gemm = lens*units+ units*ub #1 add 2mac
            acti = lens*ub
            gemmB = gemm
            actiB = acti

        elif ltype=='Conv2D':
            ub = 1 if x.use_bias else 0
            gemm = int(np.prod(x.kernel_size))*inp0[2]*datao+x.output_shape[3]*ub
            gemmB = gemm

        elif ltype== 'GlobalAveragePooling2D':
            vect=datao*(inp0[0]*inp0[1]-1) #add op
            vectB = vect

        elif ltype=='Activation':
            acti = datao  #activation functions
            actiB = acti

        elif ltype=='DepthwiseConv2D':
            ub = 1 if x.use_bias else 0
            gemm=int(np.prod(x.kernel_size))*datao+x.output_shape[3]*ub
            gemmB = gemm

        elif ltype=='MaxPooling2D':
            vect = datao*int((np.prod(x.pool_size)-1)) #max op
            vectB = datao*int(np.prod(x.pool_size))

        else:
            weights=x.get_weights()
            if len(weights)>0:
                gemm=0
                for item in weights:
                    gemm += int(np.prod(item.shape))
            gemmB = gemm

    return gemm,vect,acti,gemmB,vectB,actiB

def pararetrival(x):
    conf = x.get_config()
    kh, kw, sh, sw, ph, pw = ['']*6
    # Conv2d, MaxPooling2D,
    if isinstance(x, keras.layers.Conv2D):
        # kernel size
        kh, kw = x.kernel_size
        # stride size
        sh, sw = x.strides
        # padding
        if conf['padding']=='valid':
            ph=0
            pw=0
        elif conf['padding']=='same':
            ph=kh//2
            pw=kw//2

    if isinstance(x, keras.layers.DepthwiseConv2D):
        # kernel size
        kh, kw = x.kernel_size
        # stride size
        sh, sw = x.strides
        # padding
        if conf['padding']=='valid':
            ph=0
            pw=0
        elif conf['padding']=='same':
            ph=kh//2
            pw=kw//2

    if isinstance(x, keras.layers.MaxPooling2D): # ignore GlobalAveragePooling2D
        # kernel size
        kh, kw = x.pool_size
        # stride size
        sh, sw = x.strides
        # padding
        if conf['padding']=='valid':
            ph=0
            pw=0
        elif conf['padding']=='same':
            ph=kh//2
            pw=kw//2
    return kh,kw,sh,sw,ph,pw

def GetModel(ucfg, draw_graph=True):
    ''' ucfg: user's Config for the table output: nnname, BS, BPE '''

    nnname = ucfg['nnname']
    isconv = True

    if nnname == 'newmodel':
        import sys
        sys.path.append("..")
        from newmodel import tfmodel
        model,isconv = tfmodel()
        sys.path.remove("..")

    import tensorflow.keras.applications as nn
    if hasattr(nn,nnname):
        model = getattr(nn, nnname)(weights=None)

    # efficientnet: B0-B7
    elif nnname[:-2] == 'EfficientNet':
        import tfmodels.efficientnet.tfkeras as nn
        model = getattr(nn, nnname)(weights=None)

    # TF2.x Models:
    elif nnname == 'ncf':
        import tfmodels.ncf as nn
        name = 'ncfmodel'
        model = getattr(nn, name)(istrain=False)
        isconv = False

    elif nnname == 'din':
        import tfmodels.din as nn
        name = 'din'
        _, model = getattr(nn, name)(item_count=63001, cate_count=801, hidden_units=128)
        isconv = False

    # bert from bert_keras
    elif nnname == 'bert':
        isconv =False
        from keras_bert import get_base_dict, get_model, compile_model
        # Build token dictionary
        token_dict = get_base_dict()
        training = True
        if training:
            # # bert base
            # embed_dim=768 # bert small
            # headnum=12
            # layernum=12
            # bert large
            embed_dim=1024 # bert small
            headnum=16
            layernum=24

            ff_dim=embed_dim*4
            token_num = 30522 # number of words from paper
            model = get_model(token_num=token_num,
                              pos_num=512,
                              seq_len=512,
                              embed_dim=embed_dim,
                              transformer_num= layernum,
                              head_num=headnum,
                              feed_forward_dim=ff_dim,
                              training=training)
        else:
            # Revise lib\site-packages\keras_bert\bert.py: line164
            # "return inputs, transformed" -> "return inputs, transformed,model"
            _,_,model = get_model(token_num=len(token_dict),embed_dim=1024,head_num=16,training=training)

        compile_model(model)

    if nnname =='mymodel':
        isconv = False

        ## ===== To add a customized model ====
        # refer to: https://keras.io/guides/sequential_model/
        from tensorflow.keras import layers
        # Define a customized model
        model = keras.Sequential()
        model.add(keras.Input(shape=(ucfg['height'], ucfg['width'], ucfg['channel'])))
        model.add(layers.Conv2D(32, 5, strides=2, activation="relu"))
        model.add(layers.Conv2D(32, 3, activation="relu"))
        model.add(layers.MaxPooling2D(3))
        model.add(layers.Conv2D(32, 3, activation="relu"))
        model.add(layers.Conv2D(32, 3, activation="relu"))
        model.add(layers.MaxPooling2D(3))
        model.add(layers.Conv2D(32, 3, activation="relu"))
        model.add(layers.Conv2D(32, 3, activation="relu"))
        model.add(layers.MaxPooling2D(2))
        # Now that we have 4x4 feature maps, time to apply global max pooling.
        model.add(layers.GlobalMaxPooling2D())
        # Finally, we add a classification layer.
        model.add(layers.Dense(10))

        ## ===== end of your codes  ======

    if draw_graph:
        g = keras.utils.model_to_dot(model,show_shapes=True)
        if nnname =='newmodel':
            nnname = ucfg['model']
        g.write_pdf(".//outputs//tf//"+nnname+'.pdf')
    return model, isconv

def ListGen(model,isconv,ucfg):
    bs = ucfg['batchsize']*ucfg['BPE']
    paralist = headgen(isconv)
    for x in model.layers: #model.layers[::-1]
        # no batch, hxwxc
        inp0 = ['']*3; inp1 = ['']*3; out = ['']*3
        kh = ''; kw = ''; sh = ''; sw = ''; ph = ''; pw=''
        extin=''
        datai=''; datao=''; dataw=''
        gemm=''; vect='' ; acti =''
        ltype = str(type(x)).split(".")[-1].split("'")[0]

        # input tensor & size
        (inp0, inp1, datai, extin) = inputgen(x,inp0,inp1,extin)
        # output tensor & size
        (out,datao,extin) = outputgen(x,out,extin)
        # weight size
        dataw = getweightsize(x,dataw)
        # # of ops: gemm, elememwise, activiation(transcendental functions)
        (gemm, vect, acti, gemmB, vectB, actiB) = opscomputation(x,datao,inp0)
        # conv tensor
        (kh, kw, sh, sw, ph, pw) = pararetrival(x)

        datai = datai*bs
        datao = datao*bs
        dataw = dataw*bs
        # extin last column
        if isconv:
            new_row = [x.name,ltype]+ inp0+inp1+out+[kh,kw,sh,sw,ph,pw,datai,datao,dataw,gemm,vect,acti,gemmB, vectB, actiB]
            paralist.append(new_row)
        else:
            doublerow = False
            dim=2
            if isinstance(gemm, list):
                if doublerow: # multihead attention: tow rows
                    new_row = [x.name,ltype]+ inp0[:dim]+inp1[:dim]+out[:dim]+[datai,datao,dataw,gemm[0],vect[0],acti[0],gemmB, vectB, actiB]
                    paralist.append(new_row)
                    new_row = ['']*11+[gemm[1],vect[1],acti[1]]+['']
                    paralist.append(new_row)
                else:
                    new_row = [x.name,ltype]+ inp0[:dim]+inp1[:dim]+out[:dim]+[datai,datao,dataw,gemm[1],vect[1],acti[1],gemmB, vectB, actiB]
                    paralist.append(new_row)
            else:
                new_row = [x.name,ltype]+ inp0[:dim]+inp1[:dim]+out[:dim]+[datai,datao,dataw,gemm,vect,acti,gemmB, vectB, actiB]
                paralist.append(new_row)
    return paralist

def tableExport(paralist,nnname, backward):
    paraout = './/outputs//tf//'+nnname+'.xlsx'
    headers = list(zip(*paralist[:2]))
    df = pd.DataFrame(paralist[2:], columns=pd.MultiIndex.from_tuples(headers))
    if not backward:
        df.drop('Backward Ops', axis=1, level=0, inplace=True)

    df.to_excel(paraout, sheet_name='Details')
    ft.SumAndFormat(paraout, df)