#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ReversibleTokenizer class.

Main method is transform or __call__, which receives a string and return list of strings, 
each being a token.
Cut the text in word (string separated by ' '), sentence (string separeted by '\n'),
n-grams (succession of words of a given size), char-grams (succession of characters).

"""

from itertools import islice

class ReversibleTokenizer():
    
    def _check_analyzer(self,analyzer):
        if analyzer not in ['word','sentence','ngram','chargram','document','original']:
            mess = "analyzer must be document, sentence, word, ngram or chargram"
            mess += ', received {}'.format(analyzer)
            raise ValueError(mess)
        self.analyzer = str(analyzer)
        return None
    
    def _check_size(self,size):
        if self.analyzer in ['ngram','chargram'] and not size:
            mess = "size must be provided for ngram and chargram values"
            mess += " of analyzer, received {}".format(size)
            raise ValueError(mess)
        if size:
            self.size = int(size)
        else:
            self.size = None
        return None
    
    def __init__(self,analyzer='word',size=None,generator=False):
        self._check_analyzer(analyzer)
        self._check_size(size)
        self.generator = bool(generator)
        self.pipeline = list()
        return None
    
    def __call__(self,doc):
        return self.transform(doc)
    
    def _split_doc(self,doc,string):
        for tok in doc.split(string):
            if tok:
                self.pipeline.append((string,1))
                yield tok
            else:
                try:
                    string,increment = self.pipeline[-1]
                    self.pipeline[-1] = (string,increment+1)
                except IndexError: # in case the pipeline is empty
                    self.pipeline.append((string,1))
        return None
    
    def _unsplit_doc(self,tokens):
        s = str()
        if len(self.pipeline) > len(tokens):
            string,increment = self.pipeline.pop(0)
            s += string*increment
        for tok in tokens[:-1]:
            try:
                string,increment = self.pipeline.pop(0)
            except IndexError:
                return print("Problem with Tokenizer : no longer pipeline")
            s += tok + string*increment
        s += tokens[-1]
        try:
            string,increment = self.pipeline.pop(0)
            if increment > 1:
                s += string*(increment-1)
        except IndexError:
            pass
        return s
    
    def split_doc(self,doc,string):
        yield from self._split_doc(doc,string)
    
    def unsplit_doc(self,tokens):
        return self._unsplit_doc(tokens)
    
    def _generate(self,doc):
        self.pipeline = list()
        if self.analyzer=='sentence':
            yield from self._split_doc(doc,'\n')
        elif self.analyzer=='word':
            yield from self._split_doc(doc,' ')
        elif self.analyzer=='ngram':
            toks = list(self._split_doc(doc,' '))
            n = len(toks)-self.size+1
            for i in range(n):
                yield ' '.join(toks[i:i+self.size])
        elif self.analyzer=='chargram':
            for i in range(len(doc)-self.size+1):
                yield doc[i:i+self.size]
        elif self.analyzer in ['document','original']:
            yield doc
        else:
            raise AttributeError("Didn't understand the analyzer in _generate")
    
    def transform(self,doc):
        if not self.generator:
            return list(self._generate(doc))
        else:
            return self._generate(doc)
    
    def undo(self,tokens):
        if self.analyzer in ['sentence','word']:
            return self._unsplit_doc(tokens)
        elif self.analyzer=='ngram':
            toks = [ngram.split(' ')[0] for ngram in tokens]
            toks += tokens[-1].split(' ')[1:]
            return self._unsplit_doc(toks)
        elif self.analyzer=='chargram':
            s = str()
            for tok in tokens:
                s += tok[0]
            return s[:-1] + tok
        elif self.analyzer in ['document','original']:
            return tokens[0]
    
    def pipe(self,docs,batch_size=1):
        iterable = iter(docs)
        batch = list(islice(iterable,batch_size))
        while batch:
            tokens = (self.transform(doc) for doc in batch)
            yield tokens
            batch = list(islice(iterable,batch_size))
            


