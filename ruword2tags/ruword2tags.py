from __future__ import print_function

import gzip
import pathlib
import os
import pickle


class TrieNode:
    def __init__(self, char):
        self.char = char
        self.hit_count = 0
        self.tagset_indeces = []
        self.nextchar2node = dict()

    def add(self, next_chars, tagset_index):
        self.hit_count += 1
        if len(next_chars) == 0:
            self.tagset_indeces.append(tagset_index)
        else:
            next_char = next_chars[0]
            if next_char not in self.nextchar2node:
                self.nextchar2node[next_char] = TrieNode(next_char)

            self.nextchar2node[next_char].add(next_chars[1:], tagset_index)

    def count_children(self):
        return 1 + sum(child.count_children() for child in self.nextchar2node.values())

    def count_leaves(self):
        return len(self.tagset_indeces) + sum(child.count_leaves() for child in self.nextchar2node.values())

    def find_tagsets(self, word):
        if word:
            found_tagsets = []
            next_char = word[0]
            if next_char in self.nextchar2node:
                found_tagsets.extend(self.nextchar2node[next_char].find_tagsets(word[1:]))
            return found_tagsets
        else:
            return self.tagset_indeces


class RuWord2Tags:
    dict_filename = 'ruword2tags.dat'

    def __init__(self):
        self.ending_len = None
        self.index2tagset = None
        self.ending2tagsets = None
        self.trie_root = None

    def load(self):
        module_folder = str(pathlib.Path(__file__).resolve().parent)
        p = os.path.join(module_folder, '../output', self.dict_filename)
        if not os.path.exists(p):
            p = os.path.join(module_folder, self.dict_filename)

        with gzip.open(p, 'r') as f:
            data = pickle.load(f)
            self.ending_lens = data['ending_lens']
            self.index2tagset = data['index2tagset']
            self.ending2tagsets = data['ending2tagsets']
            trie_words = data['trie_words']

            self.trie_root = TrieNode('')
            for word, itagset in trie_words:
                self.trie_root.add(word, itagset)

    def __getitem__(self, word):
        hit_by_ending = False
        for ending_len in self.ending_lens:
            ending = word[-ending_len:] if len(word) > ending_len else u''
            if ending in self.ending2tagsets:
                for itagset in self.ending2tagsets[ending]:
                    yield self.index2tagset[itagset]
                hit_by_ending = True
                break

        if not hit_by_ending:
            for itagset in self.trie_root.find_tagsets(word):
                yield self.index2tagset[itagset]
