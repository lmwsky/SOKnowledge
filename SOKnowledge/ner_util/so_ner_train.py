#!/usr/bin/env python
# -*- coding:utf-8 -*-
from train import NERTaggerTrainer
if __name__ == "__main__":

    trainer = NERTaggerTrainer()
    trainer.init_model_parameters(train_set_location="corpus/so_ner/0/S3train0.conll",
                                  dev_set_location="corpus/so_ner/0/S3dev0.conll",
                                  test_set_location="corpus/so_ner/0/S3test0.conll",
                                  pre_emb="corpus/replace_large_code_block/word_embedding.txt"
                                  )
    trainer.init_model("SO_LSTM_CRF0")
    #trainer.train(n_epochs=20, freq_eval=1000,best_dev=17.75000,best_test=0)
    trainer.train(n_epochs=50, freq_eval=300)
