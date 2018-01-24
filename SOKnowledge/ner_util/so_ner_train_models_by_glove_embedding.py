#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys

from train import NERTaggerTrainer

if __name__ == "__main__":

    set_num = sys.argv[1]
    start_subset = int(sys.argv[2])
    end_subset = int(sys.argv[3])

    for i in range(start_subset, end_subset):
        trainer = NERTaggerTrainer()
        train_set_location = "corpus/so_ner/dataSet{0}/{1}/S{2}train{3}.conll".format(set_num, i, set_num, i)
        dev_set_location = "corpus/so_ner/dataSet{0}/{1}/S{2}dev{3}.conll".format(set_num, i, set_num, i)
        test_set_location = "corpus/so_ner/dataSet{0}/{1}/S{2}test{3}.conll".format(set_num, i, set_num, i)
        pre_emb = "corpus/glove/vectors.txt"

        print "trainset:", train_set_location
        print  "devset:", dev_set_location
        print "test:", test_set_location
        print "pre_emb:", pre_emb
        model_name = "SO_LSTM_CRF_S{0}_{1}_GLOVE".format(set_num, i)
        print "model_name:", model_name

        trainer.init_model_parameters(train_set_location=train_set_location,
                                      dev_set_location=dev_set_location,
                                      test_set_location=test_set_location,
                                      pre_emb=pre_emb
                                      )
        trainer.init_model(model_name)
        best_dev, best_test = trainer.train(n_epochs=40, freq_eval=300)

        print "-----------------------------"
        print "Model{0} training finish".format(str(i))
        print "best_dev:", str(best_dev)
        print "best_test:", str(best_test)
        print "-----------------------------"
