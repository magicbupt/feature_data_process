#!/usr/bin/env python
#encoding:utf-8

__author__ = 'caiting'

#计算信息熵以及信息增益

import math

def entropy(data_set):
    '''
    计算指定的信息熵
    data_set format: {label:count}
    '''
    if data_set == None:
        return

    label_count_sum = 0
    for label, label_count in data_set.items():
        label_count_sum += label_count

    key_pro_dt = {} #存不同key下的概率
    for label, label_count in data_set.items():
        key_pro_dt[label] = label_count/(1.0*label_count_sum)

    #计算信息熵
    ent = 0
    for label, pro in key_pro_dt.items():
        ent += pro*math.log(pro)
    ent = 0 - ent

    return ent

def entropy4Overall(data_set):
    '''
    计算样本的整体信息熵
    '''
    label_count = {}
    for pid, sample in data_set.items():
        label_val = smaple['label']
        if label_val not in label_count:
            label_count[label_val] = 0
        label_count[label_val] += 1
    entropy_S = entropy(label_count)
    return entropy_S

def GrainFeature(feature, data_set):
    '''
    计算指定feature的信息增益
    feature: feature的索引号,标示位
    data_set:样本集合， format:{pid:{1:val_1, ..., n:val_n, 'label':value}}
    '''
    if data_set == None:
        return

    key_label_count_dt = {}
    for pid, sample in data_set.items():
        if feature not in sample:
            continue
        key = data_set[feature]
        label = data_set['label']
        if key not in key_label_count_dt:
            key_label_count_dt[key] = {}
        if label not in key_label_count_dt[key]:
            key_label_count_dt[key][label] = 0
        key_label_count_dt[key][label] += 1

    sample_sum = len(data_set)
    feature_ent = 0
    for key in key_label_count_dt:
        label_count = key_label_count_dt[key]
        key_count = 0
        for label, val in label_count:
            key_count += val
        pro_key = key_count/(1.0*sample_sum)
        feature_ent += pro_key*entropy(label_count)

    entropy_S = entropy4Overall(data_set)

    return entropy_S - feature_ent

def Grain4AllFeature(feature_set, data_set):
    '''
    计算各个特征的信息增益
    '''
    feature_grain_dt = {}
    for feature in feature_set:
        feature_grain_dt[feature] = GrainFeature(feature, data_set)

    return feature_grain_dt



def main():
    pass

if __name__=="__main__":
    main()

