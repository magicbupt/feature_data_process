#!/usr/bin/env python
#encoding:utf-8

__author__ = 'caiting'

#特征聚合平台：实现将各个不同的特征结果文件聚合成一个特征文件
#特征文件名称：sample_feature_file_1 ... sample_feature_file_n
#要求各输入特征文件格式：sample_id feature_1:value_1 ... feature_n:value_n
#target文件名称：sample_value
#target文件格式为：sample_id label
#输出文件格式为：label id:sample_id feature_1:value_1 ... feature_n:value_n

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import math
from ConfigParser import RawConfigParser
from ConfigParser import *

sys.path.append('../lib')
sys.path.append('lib')
import logging
import logging.config
#from mail_sender import MailSender

class DataAggregationPlatform(object):
    def __init__(self, conf_path = '../'):

        #other config such as email recivers
        self.modelcfg = '%s/conf/DataAggregationPlatform.cfg' % (conf_path)
        self.modelconfig = RawConfigParser()
        self.modelconfig.read(self.modelcfg)

        #self.feature_num = int(self.modelconfig.get('model', 'model_feature_num'))
        # the model[0] is bias
        #self.model = [0 for i in range(self.feature_num + 1)]

        #value_file
        self.sample_value_file_name = self.modelconfig.get('value_file', 'value_file_name')

        #feature_file
        self.sample_feature_file_name = self.modelconfig.get('feature_file', 'feature_file_name')
        self.feature_file_num = int(self.modelconfig.get('feature_file', 'feature_file_num'))
        self.feature_num_4_file_dt = self.readFeatureFileConf()

        #sample_dict format "sample_id:feature_dict"
        self.sample_feature_dict = {}
        self.sample_value_dict = {}

    def readFeatureFileConf(self, section = 'feature_file', index = 'feature_num_4_file_'):
        #读取特征文件的特征数量
        feature_num_4_file_dt = {}
        file_num = self.feature_file_num
        for i in range(1, file_num + 1):
            i_feature_file_index = '%s%s' % (index, i)
            feature_num_4_file_i = int(self.modelconfig.get(section, i_feature_file_index))
            feature_num_4_file_dt[i_feature_file_index] = feature_num_4_file_i

        return feature_num_4_file_dt

    def readSampleValue(self, filepath = '../data/'):
        '''
        读取各个sample的y值，
        '''
        value_file_path = '%s%s' % (filepath, self.sample_value_file_name)
        file = None
        try:
            file = open(value_file_path, 'r')
            while True:
                line = file.readline()
                if not line:
                    break
                word_arr = line.strip().split()
                if len(word_arr) != 2:
                    continue

                sample_id = int(word_arr[0])
                value = float(word_arr[1])
                self.sample_value_dict[sample_id] = value
        except Exception,ex:
            print ex
        finally:
            if file:
                file.close()

    def readAllSampleFeatureFile(self, file_path = '../data/'):
        '''
        读取各个feature文件中的特征值，并按如下公式对应到model中各自权重
        feature_index[m,n] = sum(feature_num_4_file_i) + n (i = 1 ... m-1)
        '''
        base_index = 0
        for i in range(1, self.feature_file_num + 1):
            file_name = '%s%s' % (self.sample_feature_file_name, i)
            i_file_path = '%s%s' % (file_path, file_name)
            #print i_file_path,  base_index

            self.readEachSampleFeatureFile(i_file_path,base_index)

            feature_num_4_file = self.feature_num_4_file_dt['feature_num_4_file_%s' % i]
            base_index += feature_num_4_file

    def readEachSampleFeatureFile(self, file_path, base_index):
        '''
        读取feature文件
        '''
        file = None
        try:
            file = open(file_path, 'r')
            while True:
                line = file.readline()
                if not line:
                    break
                word_arr = line.strip().split()

                length = len(word_arr)
                #print word_arr, length
                if length < 2:
                    continue

                sample_id = int(word_arr[0])
                sample_feature = {}
                if sample_id in self.sample_feature_dict:
                    sample_feature = self.sample_feature_dict[sample_id]

                for i in range(1, length):
                    index_value = word_arr[i].strip().split(':')
                    if len(index_value) != 2:
                        continue
                    index = int(index_value[0]) + base_index
                    value = float(index_value[1])
                    sample_feature[index] = value

                self.sample_feature_dict[sample_id] = sample_feature
        except Exception,ex:
            print ex
        finally:
            if file:
                file.close()

    def writeTrainingOrTestingDataFile(self, disfile = '../data/train_data.txt'):
        '''
        将数据按sample_id整理成完整的样本数据
        输出格式： value id:sample_id 1:feature1 2:feature ... n:feature
        '''
        file = None
        try:
            file = open(disfile, 'w+')
            for id, value in self.sample_value_dict.items():
                if id not in self.sample_feature_dict:
                    continue
                sample = self.sample_feature_dict[id]
                sample_str = '%s id:%s ' % (value, id)
                for feature_index, feature_value in sample.items():
                    sample_str = '%s %s:%s' % (sample_str, feature_index, feature_value)
                sample_str = '%s\n' % sample_str.strip()
                file.write(sample_str)
        except Exception,ex:
            print ex
        finally:
            if file:
                file.close()

def test():
    o = DataAggregationPlatform()
    o.readSampleValue()
    o.readAllSampleFeatureFile()
    for k in o.sample_feature_dict:
        print k, o.sample_feature_dict[k]
    o.writeTrainingOrTestingDataFile()

if __name__=='__main__':
    test()

