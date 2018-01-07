#encoding=utf8
from concurrent import futures
import time
import grpc
import suiyi_tag_pb2
import suiyi_tag_pb2_grpc

import os
import sys
import numpy as np
import tensorflow.contrib.keras as kr
ROOT= '/home/algorithm/suiyi_tag/'
sys.path.append(os.path.join(ROOT,'offline_train'))
from cnn_model import *
from suiyi_loader import *



_ONE_DAY_IN_SECONDS = 60 * 60 * 24

class TagServer(suiyi_tag_pb2_grpc.TagServerServicer):
    def __init__(self): 
        #类别
        self.categories, self.cat_to_id, self.categories_code = read_category()

        #读取词表
        base_dir = os.path.join(ROOT,'data/suiyi')
        vocab_dir = os.path.join(base_dir, 'suiyi.vocab.txt')
        words, self.word_to_id = read_vocab(vocab_dir)

        config = TCNNConfig()
        config.vocab_size = len(words)
        self.model = TextCNN(config)

        save_dir = os.path.join(ROOT,'checkpoints/textcnn')
        save_path = os.path.join(save_dir, 'best_validation')   # 最佳验证结果保存路径

        self.session = tf.Session()
        self.session.run(tf.global_variables_initializer())
        saver = tf.train.Saver()
        saver.restore(sess=self.session, save_path=save_path)  # 读取保存的模型
        print("Model loaded!")
    
    def _process(self, contents, word_to_id, max_length=200):
        data_id = [] 
        for i in range(len(contents)):
            data_id.append([word_to_id[x] for x in contents[i] if x in word_to_id])
        x_pad = kr.preprocessing.sequence.pad_sequences(data_id, max_length)
        return x_pad
        
    def _feed_data(self, x_batch, y_batch, keep_prob):
        feed_dict = {
            self.model.input_x: x_batch,
            self.model.input_y: y_batch,
            self.model.keep_prob: keep_prob
        }
        return feed_dict
 

    def Tag(self, request, context):
        contents =  request.content

        if isinstance(contents,str):
            contents = [contents]
        x_test = self._process(contents, self.word_to_id,  200)
        fake_label = np.zeros(len(self.categories))
        feed_dict = self._feed_data(x_test, [fake_label],1.0)
        y_pred, y_pred_cls = self.session.run([self.model.y_pred,self.model.y_pred_cls], feed_dict=feed_dict)
 
        preds = []
        for p in y_pred_cls:
            preds.append(self.categories_code[p])
        return suiyi_tag_pb2.TagResponse(content=",".join(preds))


def main():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    suiyi_tag_pb2_grpc.add_TagServerServicer_to_server(TagServer(),
                                                          server)
    server.add_insecure_port('[::]:10033')
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    main()
