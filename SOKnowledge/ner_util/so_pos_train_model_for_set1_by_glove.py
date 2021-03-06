#!/usr/bin/env python
# -*- coding:utf-8 -*-
from train import NERTaggerTrainer

if __name__ == "__main__":
    trainer = NERTaggerTrainer()
    train_set_location = "corpus/so_pos1/train.conll"
    dev_set_location = "corpus/so_pos1/dev.conll"
    test_set_location = "corpus/so_pos1/test.conll"
    pre_emb = "corpus/glove/vectors.txt"

    print "trainset:", train_set_location
    print  "devset:", dev_set_location
    print "test:", test_set_location
    print "pre_emb:", pre_emb
    model_name = "SO_LSTM_CRF_POS_1_ep_100_freq_100_glove"

    trainer.init_model_parameters(train_set_location=train_set_location,
                                  dev_set_location=dev_set_location,
                                  test_set_location=test_set_location,
                                  pre_emb=pre_emb
                                  )
    trainer.init_model(model_name)
    best_dev, best_test = trainer.train(n_epochs=100, freq_eval=100)

    print "-----------------------------"
    print "best_dev:", str(best_dev)
    print "best_test:", str(best_test)
    print "-----------------------------"
