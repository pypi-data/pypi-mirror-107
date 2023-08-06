import pandas as pd
import tensorflow as tf
import numpy as np
from tensorflow.keras import layers,activations
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.callbacks import ModelCheckpoint

#SE模块
#如需使用，得加到下采样层里
class Squeeze_excitation_layer(tf.keras.Model):
    def __init__(self, filter_sq):
    	# filter_sq 是 Excitation 中第一个卷积过程中卷积核的个数
        super().__init__()
        self.avepool = tf.keras.layers.GlobalAveragePooling1D()
        self.dense = tf.keras.layers.Dense(filter_sq)
        self.relu = tf.keras.layers.Activation('relu')
        self.sigmoid = tf.keras.layers.Activation('sigmoid')

    def call(self, inputs):
        squeeze = self.avepool(inputs)
        
        excitation = self.dense(squeeze)

        excitation = self.relu(excitation)

        excitation = tf.keras.layers.Dense(inputs.shape[-1])(excitation)

        excitation = self.sigmoid(excitation)

        excitation = tf.keras.layers.Reshape((1, inputs.shape[-1]))(excitation)

        scale = inputs * excitation

        return scale

#下采样层
class DownSample(tf.keras.layers.Layer):
    #units，使用多少个filter
    #k_size:确定第一个卷积层的kernel_size
    def __init__(self,units,is_pool=True,use_se = False,k_size=3):
        super(DownSample,self).__init__()
        #注意，原始unet是valid填充，此处简化为same填充
        self.conv1 = tf.keras.layers.Conv1D(units,kernel_size=k_size,
                                            padding = 'same')
        self.conv2 = tf.keras.layers.Conv1D(units,kernel_size=3,
                                            padding = 'same')
        if is_pool:
            self.pool = tf.keras.layers.MaxPooling1D(pool_size=2)
        else:
            self.pool=False
        
        if use_se:
            self.se = Squeeze_excitation_layer(units)
        else:
            self.se = False
            
 
    def call(self,x):
        if self.pool:
            x = self.pool(x)
        x = self.conv1(x)
        x = tf.nn.relu(x)
        x = self.conv2(x)
        x = tf.nn.relu(x)
        if self.se:
            x = self.se(x)
        return x


#上采样层
class UpSample(tf.keras.layers.Layer):
    #units，使用多少个filter
    def __init__(self,units):
        super(UpSample,self).__init__()
        #注意，原始unet是valid填充，此处简化为same填充
        self.conv1 = tf.keras.layers.Conv1D(units,kernel_size=3,
                                            padding = 'same')
        self.conv2 = tf.keras.layers.Conv1D(units,kernel_size=3,
                                            padding = 'same')
        #反卷积上采样,注意上采样的stride是放大的关键
        #注意上采样中
        self.deconv = tf.keras.layers.Conv1DTranspose(units//2,kernel_size=2,
                                            padding = 'same',strides=2)
    #输入x，是否添加pool的控制属性
    def call(self,x):
        x = self.conv1(x)
        x = tf.nn.relu(x)
        x = self.conv2(x)
        x = tf.nn.relu(x)
        x = self.deconv(x)
        x = tf.nn.relu(x)
        return x



#现在其实是SE-uNET
class SE_Unet_1d(tf.keras.Model):
    def __init__(self):
        super(SE_Unet_1d,self).__init__()
        #第一层64个卷积核
        #注意is_pool在call时候传入，必须注意
        #第一层给11，会不会好一些
        self.down1 = DownSample(64,is_pool=False,k_size=11)
        #都不加use_se=True，就是原始的
        self.down2 = DownSample(128,use_se=True)
        self.down3 = DownSample(256,use_se=True)
        self.down4 = DownSample(512,use_se=True) 
        self.down5 = DownSample(1024)

        #单独定义一个上采样
        self.up = tf.keras.layers.Conv1DTranspose(512,kernel_size=2,
                                                  strides=2,padding='same'
                                                  )
        self.up1 = UpSample(512)
        self.up2 = UpSample(256)
        self.up3 = UpSample(128)
        
        #注意此处借用下采样，is_pool设false
        self.last_conv = DownSample(64,is_pool=False)

        #对每个像素点进行回归（只需要1个filter，n分类需要n个filter）
        self.out_conv = tf.keras.layers.Conv1D(1,kernel_size=1,
                                            padding = 'same')
    def call(self,inputs):
        x1 = self.down1(inputs)
        x2 = self.down2(x1)
        x3 = self.down3(x2)
        x4 = self.down4(x3)
        x5 = self.down5(x4)

        x6 = self.up(x5)

        #合并
        x7 = tf.concat([x4,x6],2)

        x8 = self.up1(x7)

        x9 = tf.concat([x3,x8],2)

        x10 = self.up2(x9)

        x11 = tf.concat([x2,x10],2)

        x12 = self.up3(x11)

        x13 =  tf.concat([x1,x12],2)
        
        x14 = self.last_conv(x13)

        out = self.out_conv(x14)

        return out

