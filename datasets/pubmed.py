import json
import os
import re
import sys
import csv
import numpy as np
import torch
from torchtext.data import NestedField, Field, TabularDataset
from torchtext.data.iterator import BucketIterator
from torchtext.vocab import Vectors

csv.field_size_limit(sys.maxsize)

# Performs tokenization and string cleaning for the Pubmed dataset
def clean_string(string):
    string = re.sub(r"[^A-Za-z0-9(),!?\'`]", " ", string)
    string = re.sub(r"\s{2,}", " ", string)
    return string.lower().strip().split()


def split_sents(string):
    string = re.sub(r"[!?]"," ", string)
    return string.strip().split('.')


def generate_ngrams(tokens, n=2):
    n_grams = zip(*[tokens[i:] for i in range(n)])
    tokens.extend(['-'.join(x) for x in n_grams])
    return tokens

''' I may have to create a method to load xml similarly to the method below ''' 

def load_json(string):
    split_val = json.loads(string)
    return np.asarray(split_val, dtype=np.float32)


def char_quantize(string, max_length=1000):
    identity = np.identity(len(PubmedCharQuantized.ALPHABET))
    quantized_string = np.array([identity[PubmedCharQuantized.ALPHABET[char]] for char in list(string.lower()) if char in PubmedCharQuantized.ALPHABET], dtype=np.float32)
    if len(quantized_string) > max_length:
        return quantized_string[:max_length]
    else:
        return np.concatenate((quantized_string, np.zeros((max_length - len(quantized_string), len(PubmedCharQuantized.ALPHABET)), dtype=np.float32)))

# Returns the label string as a list of integers
def process_labels(string):    
    return [float(x) for x in string]

class Pubmed(TabularDataset):
    NAME = 'Pubmed'
    NUM_CLASSES = 2
    IS_MULTILABEL = False

    TEXT_FIELD = Field(batch_first=True, tokenize=clean_string, include_lengths=True)
    LABEL_FIELD = Field(sequential=False, use_vocab=False, batch_first=True, preprocessing=process_labels)

    @staticmethod
    def sort_key(ex):
        return len(ex.text)

    @classmethod
    def splits(cls, path, train=os.path.join('Pubmed', 'train.tsv'), validation=os.path.join('Pubmed', 'dev.tsv'), test=os.path.join('Pubmed', 'test.tsv'), **kwargs):
        return super(Pubmed, cls).splits(path, train=train, validation=validation, test=test, format='tsv', fields=[('label', cls.LABEL_FIELD), ('text', cls.TEXT_FIELD)])

    @classmethod
    def iters(cls, path, vectors_name, vectors_cache, batch_size=64, shuffle=True, device=0, vectors=None, unk_init=torch.Tensor.zero_):
        # :param path: directory containing train, test, dev files              # :param vectors_name: name of word vectors file
        # :param vectors_cache: path to directory containing word vectors file  # :param batch_size: batch size
        # :param device: GPU device                                             # :param vectors: custom vectors - either predefined torchtext vectors or your own custom Vector classes
        # :param unk_init: function used to generate vector for OOV words       # :return:
        if vectors is None:
            vectors = Vectors(name=vectors_name, cache=vectors_cache, unk_init=unk_init)
        train, val, test = cls.splits(path)
        cls.TEXT_FIELD.build_vocab(train, val, test, vectors=vectors)
        return BucketIterator.splits((train, val, test), batch_size=batch_size, repeat=False, shuffle=shuffle, sort_within_batch=True, device=device)


class PubmedBOW(Pubmed):
    TEXT_FIELD = Field(batch_first=True, tokenize=clean_string, preprocessing=generate_ngrams, include_lengths=True)


class PubmedHierarchical(Pubmed):
    NESTING_FIELD = Field(batch_first=True, tokenize=clean_string)
    TEXT_FIELD = NestedField(NESTING_FIELD, tokenize=split_sents)


class PubmedCharQuantized(Pubmed):
    ALPHABET = dict(map(lambda t: (t[1], t[0]), enumerate(list("""abcdefghijklmnopqrstuvwxyz0123456789,;.!?:'\"/\\|_@#$%^&*~`+-=<>()[]{}"""))))
    TEXT_FIELD = Field(sequential=False, use_vocab=False, batch_first=True, preprocessing=char_quantize)
    @classmethod
    def iters(cls, path, vectors_name, vectors_cache, batch_size=64, shuffle=True, device=0, vectors=None, unk_init=torch.Tensor.zero_):
        # :param path: directory containing train, test, dev files # :param batch_size: batch size  # :param device: GPU device  # :return:
        train, val, test = cls.splits(path)
        return BucketIterator.splits((train, val, test), batch_size=batch_size, repeat=False, shuffle=shuffle, device=device)
