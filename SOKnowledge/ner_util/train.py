#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import numpy as np
import optparse
import itertools
from collections import OrderedDict

from loader import update_tag_scheme, word_mapping, augment_with_pretrained, char_mapping, \
    tag_mapping, prepare_dataset, load_sentences
from model import Model
from utils import create_input, evaluate, models_path, eval_script, eval_temp


def get_opts_from_command():
    # Read parameters from command line
    optparser = optparse.OptionParser()
    optparser.add_option(
        "-T", "--train", default="",
        help="Train set location"
    )
    optparser.add_option(
        "-d", "--dev", default="",
        help="Dev set location"
    )
    optparser.add_option(
        "-t", "--test", default="",
        help="Test set location"
    )
    optparser.add_option(
        "-s", "--tag_scheme", default="iobes",
        help="Tagging scheme (IOB or IOBES)"
    )
    optparser.add_option(
        "-l", "--lower", default="0",
        type='int', help="Lowercase words (this will not affect character inputs)"
    )
    optparser.add_option(
        "-z", "--zeros", default="0",
        type='int', help="Replace digits with 0"
    )
    optparser.add_option(
        "-c", "--char_dim", default="25",
        type='int', help="Char embedding dimension"
    )
    optparser.add_option(
        "-C", "--char_lstm_dim", default="25",
        type='int', help="Char LSTM hidden layer size"
    )
    optparser.add_option(
        "-b", "--char_bidirect", default="1",
        type='int', help="Use a bidirectional LSTM for chars"
    )
    optparser.add_option(
        "-w", "--word_dim", default="100",
        type='int', help="Token embedding dimension"
    )
    optparser.add_option(
        "-W", "--word_lstm_dim", default="100",
        type='int', help="Token LSTM hidden layer size"
    )
    optparser.add_option(
        "-B", "--word_bidirect", default="1",
        type='int', help="Use a bidirectional LSTM for words"
    )
    optparser.add_option(
        "-p", "--pre_emb", default="",
        help="Location of pretrained embeddings"
    )
    optparser.add_option(
        "-A", "--all_emb", default="0",
        type='int', help="Load all embeddings"
    )
    optparser.add_option(
        "-a", "--cap_dim", default="0",
        type='int', help="Capitalization feature dimension (0 to disable)"
    )
    optparser.add_option(
        "-f", "--crf", default="1",
        type='int', help="Use CRF (0 to disable)"
    )
    optparser.add_option(
        "-D", "--dropout", default="0.5",
        type='float', help="Droupout on the input (0 = no dropout)"
    )
    optparser.add_option(
        "-L", "--lr_method", default="sgd-lr_.005",
        help="Learning method (SGD, Adadelta, Adam..)"
    )
    optparser.add_option(
        "-r", "--reload", default="0",
        type='int', help="Reload the last saved model"
    )
    opts = optparser.parse_args()[0]
    return opts


def get_parameters_from_opts(opts):
    # Parse parameters
    parameters = OrderedDict()
    parameters['tag_scheme'] = opts.tag_scheme
    parameters['lower'] = opts.lower == 1
    parameters['zeros'] = opts.zeros == 1
    parameters['char_dim'] = opts.char_dim
    parameters['char_lstm_dim'] = opts.char_lstm_dim
    parameters['char_bidirect'] = opts.char_bidirect == 1
    parameters['word_dim'] = opts.word_dim
    parameters['word_lstm_dim'] = opts.word_lstm_dim
    parameters['word_bidirect'] = opts.word_bidirect == 1
    parameters['pre_emb'] = opts.pre_emb
    parameters['all_emb'] = opts.all_emb == 1
    parameters['cap_dim'] = opts.cap_dim
    parameters['crf'] = opts.crf == 1
    parameters['dropout'] = opts.dropout
    parameters['lr_method'] = opts.lr_method

    return parameters


class NERTaggerTrainer(object):
    def __init__(self):
        self.model = None
        self.reload = None
        self.train_set_location = None
        self.dev_set_location = None
        self.test_set_location = None
        self.parameters = None

        self.f_train = None
        self.f_eval = None

        self.train_data = None
        self.dev_data = None
        self.test_data = None

        self.singletons = None
        self.train_sentences = None
        self.dev_sentences = None
        self.test_sentences = None
        self.dico_tags = None
        self.id_to_tag = None

    def check_parameters_validity(self):
        parameters = self.parameters
        # Check parameters validity
        assert os.path.isfile(self.train_set_location)
        assert os.path.isfile(self.dev_set_location)
        assert os.path.isfile(self.test_set_location)
        assert parameters['char_dim'] > 0 or parameters['word_dim'] > 0
        assert 0. <= parameters['dropout'] < 1.0
        assert parameters['tag_scheme'] in ['iob', 'iobes']
        assert not parameters['all_emb'] or parameters['pre_emb']
        assert not parameters['pre_emb'] or parameters['word_dim'] > 0
        assert not parameters['pre_emb'] or os.path.isfile(parameters['pre_emb'])

        # Check evaluation script / folders
        if not os.path.isfile(eval_script):
            raise Exception('CoNLL evaluation script not found at "%s"' % eval_script)
        if not os.path.exists(eval_temp):
            os.makedirs(eval_temp)
        if not os.path.exists(models_path):
            os.makedirs(models_path)

    def init_model_parameters_from_disk(self,model_path):
        # Check parameters validity
        assert os.path.isdir(model_path)

        # Load existing models
        print "Loading model from", model_path, ' ...'
        self.model = Model(model_path=model_path)
        self.parameters = self.model.parameters
        # Load reverse m appings
        self.word_to_id, self.char_to_id, self.tag_to_id = [
            {v: k for k, v in x.items()}
            for x in [self.model.id_to_word, self.model.id_to_char, self.model.id_to_tag]
            ]

        # Load the models
        self.f_train, self.f_eval = self.model.build(training=True, **self.parameters)
        self.model.reload()
    def init_training_data_for_retraining(self,
        train_set_location,
        dev_set_location,
        test_set_location,

    ):
        self.train_set_location = train_set_location
        self.dev_set_location = dev_set_location
        self.test_set_location = test_set_location

        parameters=self.parameters
        # Data parameters
        lower = parameters['lower']
        zeros = parameters['zeros']
        tag_scheme = parameters['tag_scheme']

        # Load sentences
        train_sentences = load_sentences(self.train_set_location, lower, zeros)
        dev_sentences = load_sentences(self.dev_set_location, lower, zeros)
        test_sentences = load_sentences(self.test_set_location, lower, zeros)

        # Use selected tagging scheme (IOB / IOBES)
        update_tag_scheme(train_sentences, tag_scheme)
        update_tag_scheme(dev_sentences, tag_scheme)
        update_tag_scheme(test_sentences, tag_scheme)

        word_to_id=self.word_to_id
        char_to_id=self.char_to_id
        tag_to_id=self.tag_to_id
        # Index data
        self.train_data = prepare_dataset(
            train_sentences, word_to_id, char_to_id, tag_to_id, lower
        )
        self.dev_data = prepare_dataset(
            dev_sentences, word_to_id, char_to_id, tag_to_id, lower
        )
        self.test_data = prepare_dataset(
            test_sentences, word_to_id, char_to_id, tag_to_id, lower
        )

        print "%i / %i / %i sentences in train / dev / test." % (
            len(self.train_data), len(self.dev_data), len(self.test_data))
        dico_words_train = word_mapping(train_sentences, lower)[0]

        #self.singletons = set([word_to_id[k] for k, v
        #                       in dico_words_train.items() if v == 1])


        #self.dico_tags = self.model. this value doesn't need
        self.id_to_tag = self.model.id_to_tag
        self.train_sentences = train_sentences
        self.dev_sentences = dev_sentences
        self.test_sentences = test_sentences

    def init_model_parameters(self,
                              train_set_location,
                              dev_set_location,
                              test_set_location,
                              tag_scheme="iob",
                              lower=0,
                              zeros=0,
                              char_dim=25,
                              char_lstm_dim=25,
                              char_bidirect=1,
                              word_dim=400,
                              word_lstm_dim=100,
                              word_bidirect=1,
                              pre_emb="",
                              all_emb=0,
                              cap_dim=1,
                              crf=1,
                              dropout=0.5,
                              lr_method="sgd-lr_.005",
                              reload=0):
        # Parse parameters
        parameters = OrderedDict()
        parameters['tag_scheme'] = tag_scheme
        parameters['lower'] = lower == 1
        parameters['zeros'] = zeros == 1
        parameters['char_dim'] = char_dim
        parameters['char_lstm_dim'] = char_lstm_dim
        parameters['char_bidirect'] = char_bidirect == 1
        parameters['word_dim'] = word_dim
        parameters['word_lstm_dim'] = word_lstm_dim
        parameters['word_bidirect'] = word_bidirect == 1
        parameters['pre_emb'] = pre_emb
        parameters['all_emb'] = all_emb == 1
        parameters['cap_dim'] = cap_dim
        parameters['crf'] = crf == 1
        parameters['dropout'] = dropout
        parameters['lr_method'] = lr_method

        self.parameters = parameters
        self.reload = reload
        self.train_set_location = train_set_location
        self.dev_set_location = dev_set_location
        self.test_set_location = test_set_location
        pass

    def init_model(self, model_name=""):
        self.check_parameters_validity()

        parameters = self.parameters
        print 'modelpath=', models_path
        # Initialize model
        model = Model(parameters=parameters, models_path=models_path, model_name=model_name)
        print "Model location: %s" % model.model_path

        # Data parameters
        lower = parameters['lower']
        zeros = parameters['zeros']
        tag_scheme = parameters['tag_scheme']

        # Load sentences
        train_sentences = load_sentences(self.train_set_location, lower, zeros)
        dev_sentences = load_sentences(self.dev_set_location, lower, zeros)
        test_sentences = load_sentences(self.test_set_location, lower, zeros)

        # Use selected tagging scheme (IOB / IOBES)
        update_tag_scheme(train_sentences, tag_scheme)
        update_tag_scheme(dev_sentences, tag_scheme)
        update_tag_scheme(test_sentences, tag_scheme)

        # Create a dictionary / mapping of words
        # If we use pretrained embeddings, we add them to the dictionary.
        if parameters['pre_emb']:
            dico_words_train = word_mapping(train_sentences, lower)[0]
            dico_words, word_to_id, id_to_word = augment_with_pretrained(
                dico_words_train.copy(),
                parameters['pre_emb'],
                list(itertools.chain.from_iterable(
                    [[w[0] for w in s] for s in dev_sentences + test_sentences])
                ) if not parameters['all_emb'] else None
            )
        else:
            dico_words, word_to_id, id_to_word = word_mapping(train_sentences, lower)
            dico_words_train = dico_words

        # Create a dictionary and a mapping for words / POS tags / tags
        dico_chars, char_to_id, id_to_char = char_mapping(train_sentences)
        dico_tags, tag_to_id, id_to_tag = tag_mapping(train_sentences)

        # Index data
        self.train_data = prepare_dataset(
            train_sentences, word_to_id, char_to_id, tag_to_id, lower
        )
        self.dev_data = prepare_dataset(
            dev_sentences, word_to_id, char_to_id, tag_to_id, lower
        )
        self.test_data = prepare_dataset(
            test_sentences, word_to_id, char_to_id, tag_to_id, lower
        )

        print "%i / %i / %i sentences in train / dev / test." % (
            len(self.train_data), len(self.dev_data), len(self.test_data))

        # Save the mappings to disk
        print 'Saving the mappings to disk...'
        model.save_mappings(id_to_word, id_to_char, id_to_tag)

        # Build the model
        self.f_train, self.f_eval = model.build(**parameters)

        # Reload previous model values
        if self.reload:
            print 'Reloading previous model...'
            model.reload()

        self.model = model
        self.singletons = set([word_to_id[k] for k, v
                               in dico_words_train.items() if v == 1])

        self.train_sentences = train_sentences
        self.dev_sentences = dev_sentences
        self.test_sentences = test_sentences
        self.dico_tags = dico_tags
        self.id_to_tag = id_to_tag

    def train(self, n_epochs=50, freq_eval=10000,best_dev=-np.inf,best_test=-np.inf):
        """
        Train network
        :param n_epochs: number of epochs over the training set
        :param freq_eval: evaluate on dev every freq_eval steps
        :return:
        """
        #
        #
        #

        count = 0
        for epoch in xrange(n_epochs):
            epoch_costs = []
            print "Starting epoch %i..." % epoch
            for i, index in enumerate(np.random.permutation(len(self.train_data))):
                count += 1
                input = create_input(self.train_data[index], self.parameters, True, self.singletons)
                new_cost = self.f_train(*input)
                epoch_costs.append(new_cost)
                if i % 50 == 0 and i > 0 == 0:
                    print "%i, cost average: %f" % (i, np.mean(epoch_costs[-50:]))
                if count % freq_eval == 0:
                    dev_score = evaluate(self.parameters, self.f_eval, self.dev_sentences,
                                         self.dev_data, self.id_to_tag, self.dico_tags)
                    test_score = evaluate(self.parameters, self.f_eval, self.test_sentences,
                                          self.test_data, self.id_to_tag, self.dico_tags)
                    print "Score on dev: %.5f" % dev_score
                    print "Score on test: %.5f" % test_score
                    if dev_score > best_dev:
                        best_dev = dev_score
                        print "New best score on dev."
                        print "Saving model to disk..."
                        self.model.save()
                    if test_score > best_test:
                        best_test = test_score
                        print "New best score on test."
            print "Epoch %i done. Average cost: %f" % (epoch, np.mean(epoch_costs))


if __name__ == "__main__":
    trainer = NERTaggerTrainer()
    """
    trainer.init_model_parameters(train_set_location="corpus/large_code_block_tagged/train_12000000_12008000__only_label_large_code_block__large_code_block_ner.txt",
                                  dev_set_location="corpus/large_code_block_tagged/dev_12000000_12008000__only_label_large_code_block__large_code_block_ner.txt",
                                  test_set_location="corpus/large_code_block_tagged/test_12000000_12008000__only_label_large_code_block__large_code_block_ner.txt",
                                  pre_emb="corpus/replace_large_code_block/word_embedding.txt"
                                  )
    trainer.init_model("large_code_block_tagger")

    """


    trainer.init_model_parameters_from_disk('models/large_code_block_tagger')
    trainer.init_training_data_for_retraining(train_set_location="corpus/large_code_block_tagged/train_11002000_11004000__only_label_large_code_block__large_code_block_ner.txt",
                               dev_set_location="corpus/large_code_block_tagged/dev_12000000_12008000__only_label_large_code_block__large_code_block_ner.txt",
                               test_set_location="corpus/large_code_block_tagged/test_11000000_11002000__only_label_large_code_block__large_code_block_ner.txt"
                                )

    trainer.train(n_epochs=20, freq_eval=3000,best_dev=17.75000,best_test=0)
