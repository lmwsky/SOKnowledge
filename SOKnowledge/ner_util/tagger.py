#!/usr/bin/env python
# coding:utf8
import os
import time
import numpy as np

from SOKnowledge.tagger.loader import prepare_sentence

from SOKnowledge.tagger.utils import create_input

from SOKnowledge.tagger.utils import zero_digits

from SOKnowledge.tagger.utils import iobes_iob

from SOKnowledge.tagger.model import Model


class NERTagger(object):
    def __init__(self):
        self.tag_to_id = None
        self.char_to_id = None
        self.word_to_id = None
        self.opts = None
        self.model = None
        self.f_eval = None
        self.parameters = None

    def load_model(self, model_path):
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
        _, self.f_eval = self.model.build(training=False, **self.parameters)
        self.model.reload()

    def tag(self, input_text):
        """
        tag the input text for NER
        :param input_text: promise that the line is well format,each line is a sentence,
        each line is words(tokenized words is much better ) with white space as separator
        :return: the tag for all words
        """
        words_list = []  # each element in list is a list of words which are from the same sentence in order.
        # [] stands for a empty line .[['I','am','happy','.'],[],['are','you','happy','?']]
        tags_list = []  # each element in list is a list of tags which are tags for the same sentence in order.
        # [] stands for a empty line .[['O','O','O','O'],[],['O','O','O','O']]
        start = time.time()
        print 'Tagging...'
        sentences = input_text.split('\n')
        count = 0
        for line in sentences:
            # clean the input,remove the empty char from sentence start and end
            line = line.rstrip().lstrip()
            if line:
                # Lowercase sentence
                if self.parameters['lower']:
                    line = line.lower()
                # Replace all digits with zeros
                if self.parameters['zeros']:
                    line = zero_digits(line)
                words = line.split()

                # Prepare input
                sentence = prepare_sentence(words, self.word_to_id, self.char_to_id,
                                            lower=self.parameters['lower'])
                input = create_input(sentence, self.parameters, False)
                # Decoding
                if self.parameters['crf']:
                    y_preds = np.array(self.f_eval(*input))[1:-1]
                else:
                    y_preds = self.f_eval(*input).argmax(axis=1)
                y_preds = [self.model.id_to_tag[y_pred] for y_pred in y_preds]
                # Output tags in the IOB2 format
                if self.parameters['tag_scheme'] == 'iobes':
                    y_preds = iobes_iob(y_preds)

                # Write tags
                assert len(y_preds) == len(words)
                words_list.append(words)
                tags_list.append(y_preds)
            else:
                words_list.append([])
                tags_list.append([])
            count += 1
            if count % 100 == 0:
                print count
        print '---- %i lines tagged in %.4fs ----' % (count, time.time() - start)
        return words_list, tags_list


if __name__ == '__main__':
    tagger = NERTagger()
    tagger.load_model('models/so_for_epochs50_splitwords')
    text = """I want to use a track-bar to change a form 's opacity .
This is my code : @ code1 @ When I try to build it , I get this error : Can not implicitly convert type 'decimal ' to 'double ' .
I tried making trans a double , but then the control does n't work .
This code has worked fine for me in VB.NET in the past .I have an absolutely positioned div containing several children , one of which is a relatively positioned div .
When I use a percentage-based width on the child div , it collapses to 0 width on IE7 , but not on Firefox or Safari .
If I use pixel width , it works .
If the parent is relatively positioned , the percentage width on the child works .
Is there something I 'm missing here ?
If conversion works , the return true .
If an exception is thrown , return false .
Regular expressions designed to match the pattern of an int or double Some other method ?If the data modification is not too time consuming ( meaning , if the main purpose of the background thread is not the actual data modification ) , try moving the section that modifies the data to a delegate and Invoke'ing that delegate .
If the actual heavy work is on the data , you 'll probably have to create a deep copy of this data to pass to the background thread , which will send the processed data back to the UI thread via Invoke again .You should be able to do something like : if ( control.InvokeRequired ) { control.Invoke ( delegateWithMyCode ) ; } else { delegateWithMyCode ( ) ; } InvokeRequired is a property on Controls to see if you are on the correct thread , then Invoke will invoke the delegate on the correct thread .
UPDATE : Actually , at my last job we did something like this : private void SomeEventHandler ( Object someParam ) { if ( this.InvokeRequired ) { this.Invoke ( new SomeEventHandlerDelegate ( SomeEventHandler ) , someParam ) ; } // Regular handling code } which removes the need for the else block and kind of tightens up the code .
    """
    words_list, tags_list = tagger.tag(text)
    print words_list
    print tags_list
    words_list, tags_list = tagger.tag(text)
    print words_list
    print tags_list