#!/usr/bin/env python
#encoding:utf-8

__author__ = 'caiting'

#特征联合：feature1*feature2
#如：人口统计学特征与商品特征联合
#基本思路：需要联合的特征分别放在两个文件中，将其中一个文件的特征读入内存（较小的那个），
# 另外一个文件按行读取各个样例，按sample_id实现联合

class FeatureCombination():
    def __init__(self, feature_filepath_1, feature_num_1, feature_filepath_2,\
                 feature_num_2, combine_feature_filepath):
        '''
        feature_filepath_1:特征文件1的路径， feature_num_1:特征文件1中的特征数目
        feature_filepath_2:特征文件2的路径， feature_num_2:特征文件2中的特征数目
        combine_feature_filepath: 联合特征输出位置
        '''
        self.feature_num_1 = feature_num_1
        self.feature_num_2 = feature_num_2
        self.feature_filepath_1 = feature_filepath_1
        self.feature_filepath_2 = feature_filepath_2
        self.combine_feature_filepath = combine_feature_filepath
        self.sample_dict = {}
        pass

    def readSmallFeatureFile(self):
        '''
        读取其中一个file到内存中
        '''
        file = None
        try:
            file = open(self.feature_filepath_1, 'r')
            while True:
                line = file.readline()
                if not line:
                    break
                sample_id, feature_dict = self.cutSampleFeatureLine(line)
                if sample_id == None:
                    continue
                self.sample_dict[sample_id] = feature_dict
        except Exception,ex:
            print ex
        finally:
            if file:
                file.close()

    def cutSampleFeatureLine(self, line):
        '''
        将读入的每行样例，进行处理，并将结果保存在内存中
        '''
        array = line.strip().split()
        if len(array) < 1:
            return
        sample_id = int(array[0])
        feature_dict = {}
        for i in range(1, len(array)):
            index_value = array[i].split(":")
            if len(index_value) != 2:
                continue
            index = int(index_value[0])
            value = float(index_value[1])

            feature_dict[index] = value

        return sample_id, feature_dict


    def readBigFeatureFileAndCombineFeature(self):
        '''
        读入另外一个特征file文件，并按行联合后写入到磁盘
        '''
        srcfile = None
        disfile = None
        try:
            srcfile = open(self.feature_filepath_2, 'r')
            disfile = open(self.combine_feature_filepath, 'w+')
            while True:
                line = srcfile.readline()
                if not line:
                    break
                qid, feature_dict_2 = self.cutSampleFeatureLine(line)
                if qid == None:
                    continue

                feature_dict_1 = {}
                if qid in self.sample_dict:
                    feature_dict_1 = self.sample_dict[qid]
                if len(feature_dict_1) == 0:
                    continue

                combine_feature = self.combineFeature(feature_dict_1, feature_dict_2)

                self.writeCombineFeatureToFile(disfile, qid, combine_feature)

        except Exception,ex:
            print ex
        finally:
            if srcfile:
                srcfile.close()
            if disfile:
                disfile.close()

    def combineFeature(self, feature_dict_1, feature_dict_2):
        '''
        feature_dict_1 对应文件1，内存文件, feature_dict_2对应文件2，读入文件
        '''
        combine_feature = {}
        for feature_index_1, value_1 in feature_dict_1.items():
            for feature_index_2, value_2 in feature_dict_2.items():
                value = value_1*value_2
                index = (feature_index_1 - 1)*self.feature_num_1 + feature_index_2
                combine_feature[index] = value

        return combine_feature

    def writeCombineFeatureToFile(self, disfile, qid, combine_feature):
        '''
        联合特征写入文件
        '''
        sample_line = "%s" % qid
        for index, value in combine_feature.items():
            sample_line = "%s %s:%s" % (sample_line, index, value)

        disfile.write("%s\n" % sample_line)

    def runCombineJob(self):
        '''
        运行特征联合，并输出到指定文件
        '''
        self.readSmallFeatureFile()
        self.readBigFeatureFileAndCombineFeature()


def main():
    feature_filepath_1 = "../data/sample_feature_file_1"
    feature_num_1 = 10
    feature_filepath_2 = "../data/sample_feature_file_2"
    feature_num_2 = 10
    combine_feature_filepath = "../data/combine.txt"
    o = FeatureCombination(feature_filepath_1, feature_num_1, feature_filepath_2,\
        feature_num_2, combine_feature_filepath)
    o.runCombineJob()

if __name__=="__main__":
    main()