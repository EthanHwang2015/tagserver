#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import Counter
import tensorflow.contrib.keras as kr
import numpy as np
import os

def open_file(filename, mode='r'):
    """
    Commonly used file reader, change this to switch between python2 and python3.
    mode: 'r' or 'w' for read or write
    """
    return open(filename, mode, encoding='utf-8', errors='ignore')

def read_file(filename):
    """读取文件数据"""
    contents, labels = [], []
    with open_file(filename) as f:
        for line in f:
            try:
                label, content = line.strip().split('\t')
                contents.append(list(content))
                labels.append(label)
            except:
                pass
    return contents, labels

def build_vocab(train_dir, vocab_dir, vocab_size=5000):
    """根据训练集构建词汇表，存储"""
    data_train, _ = read_file(train_dir)

    all_data = []
    for content in data_train:
        all_data.extend(content)

    counter = Counter(all_data)
    count_pairs = counter.most_common(vocab_size - 1)
    words, _ = list(zip(*count_pairs))
    # 添加一个 <PAD> 来将所有文本pad为同一长度
    words = ['<PAD>'] + list(words)

    open_file(vocab_dir, mode='w').write('\n'.join(words) + '\n')

def read_vocab(vocab_dir):
    """读取词汇表"""
    words = open_file(vocab_dir).read().strip().split('\n')
    word_to_id = dict(zip(words, range(len(words))))

    return words, word_to_id

def read_category():
    """读取分类目录，固定"""
    #####v1.0 类目
    #categories = [u'物流',u'代办',u'运动',u'游戏',u'社交',u'出行',
        #u'学习',u'维修',u'招聘',u'家教',u'信息咨询',u'租房',u'美容',
        #u'宠物',u'各种无聊',u'代课点名',u'租借',u'求购',u'出租',u'出售']
    #####

    #####v2.0 类目
    categories = [u'广告',u'刷单',u'屏蔽',u'物流',u'代办',u'代课',
        u'运动',u'游戏',u'社交',u'出行',u'学习',u'维修',u'招聘',
        u'家教',u'咨询',u'租售',u'求购',u'美容',u'宠物',u'无聊']

    categories_code = ['advert', 'brush', 'mask', 'logistics', 'agent', 'class',
        'sports', 'game', 'social', 'goout', 'learn', 'repair', 'recruit',
        'teacher', 'consult', 'lease', 'buy', 'beauty', 'pet', 'bored']

    cat_to_id = dict(zip(categories, range(len(categories))))

    return categories, cat_to_id, categories_code

def to_words(content, words):
    """将id表示的内容转换为文字"""
    return ''.join(words[x] for x in content)

def process_test(filename, word_to_id, max_length=200):
    contents, _= read_file(filename)
    data_id = [] 
    for i in range(len(contents)):
        data_id.append([word_to_id[x] for x in contents[i] if x in word_to_id])

    # 使用keras提供的pad_sequences来将文本pad为固定长度
    x_pad = kr.preprocessing.sequence.pad_sequences(data_id, max_length)
    return x_pad


def process_file(filename, word_to_id, cat_to_id, max_length=200):
    """将文件转换为id表示"""
    contents, labels = read_file(filename)

    data_id, label_id = [], []
    for i in range(len(contents)):
        data_id.append([word_to_id[x] for x in contents[i] if x in word_to_id])
        label_id.append(cat_to_id[labels[i]])

    # 使用keras提供的pad_sequences来将文本pad为固定长度
    x_pad = kr.preprocessing.sequence.pad_sequences(data_id, max_length)
    y_pad = kr.utils.to_categorical(label_id)  # 将标签转换为one-hot表示

    return x_pad, y_pad

def batch_iter(x, y, batch_size=64):
    """生成批次数据"""
    data_len = len(x)
    num_batch = int((data_len - 1) / batch_size) + 1

    indices = np.random.permutation(np.arange(data_len))
    x_shuffle = x[indices]
    y_shuffle = y[indices]

    for i in range(num_batch):
        start_id = i * batch_size
        end_id = min((i + 1) * batch_size, data_len)
        yield x_shuffle[start_id:end_id], y_shuffle[start_id:end_id]

if __name__ == '__main__':

    base_dir = 'suiyi'
    train_dir = os.path.join(base_dir, 'suiyi.train.txt')
    test_dir = os.path.join(base_dir, 'suiyi.test.txt')
    val_dir = os.path.join(base_dir, 'suiyi.valid.txt')
    vocab_dir = os.path.join(base_dir, 'suiyi.vocab.txt')
    build_vocab(train_dir, vocab_dir, 5000)
