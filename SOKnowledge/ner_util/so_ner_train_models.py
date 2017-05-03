#!/usr/bin/env python
# -*- coding:utf-8 -*-
from train import NERTaggerTrainer
if __name__ == "__main__":

    for i in range(0,10):
        trainer = NERTaggerTrainer()
        train_set_location = "corpus/so_ner/dataSet3/{0}/S3train{1}.conll".format(i, i)
        dev_set_location = "corpus/so_ner/dataSet3/{0}/S3dev{1}.conll".format(i, i)
        test_set_location = "corpus/so_ner/dataSet3/{0}/S3test{1}.conll".format(i, i)
        pre_emb = "corpus/replace_large_code_block/word_embedding.txt"

        print "trainset:",train_set_location
        print  "devset:",dev_set_location
        print "test:",test_set_location
        print "pre_emb:",pre_emb
        model_name = "SO_LSTM_CRF{0}".format(i)
        print "model_name:",model_name

        trainer.init_model_parameters(train_set_location=train_set_location,
                                      dev_set_location=dev_set_location,
                                      test_set_location=test_set_location,
                                      pre_emb=pre_emb
                                      )
        trainer.init_model(model_name)
        best_dev,best_test=trainer.train(n_epochs=50, freq_eval=300)

        print "-----------------------------"
        print "Model{0} training finish".format(str(i))
        print "best_dev:"+best_dev
        print "best_test:"+best_test
        print "-----------------------------"
