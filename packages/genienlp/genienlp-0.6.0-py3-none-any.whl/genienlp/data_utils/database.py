#
# Copyright (c) 2020-2021 The Board of Trustees of the Leland Stanford Junior University
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# * Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import logging

from .database_utils import has_overlap, is_banned, normalize_text

tracer = logging.getLogger('elasticsearch')
tracer.setLevel(logging.CRITICAL)

logger = logging.getLogger(__name__)


class Database(object):
    def __init__(self, canonical2type, typeqid2id, all_canonicals, ned_features_default_val, ned_features_size):
        self.canonical2type = canonical2type
        self.typeqid2id = typeqid2id
        self.id2type = {v: k for k, v in self.typeqid2id.items()}
        self.all_canonicals = all_canonicals

        self.unk_id = ned_features_default_val[0]
        self.unk_type = self.id2type[self.unk_id]

        self.ned_features_default_val = ned_features_default_val
        self.ned_features_size = ned_features_size

    def lookup_ngrams(self, tokens, min_entity_len, max_entity_len):
        # load nltk lazily
        import nltk

        nltk.download('averaged_perceptron_tagger', quiet=True)

        tokens_type_ids = [[self.unk_id] * self.ned_features_size[0]] * len(tokens)

        max_entity_len = min(max_entity_len, len(tokens))
        min_entity_len = min(min_entity_len, len(tokens))

        pos_tagged = nltk.pos_tag(tokens)
        verbs = set([x[0] for x in pos_tagged if x[1].startswith('V')])

        used_aliases = []
        for n in range(max_entity_len, min_entity_len - 1, -1):
            ngrams = nltk.ngrams(tokens, n)
            start = -1
            end = n - 1
            for gram in ngrams:
                start += 1
                end += 1
                gram_text = normalize_text(" ".join(gram))

                if not is_banned(gram_text) and gram_text not in verbs and gram_text in self.all_canonicals:
                    if has_overlap(start, end, used_aliases):
                        continue

                    used_aliases.append([self.typeqid2id.get(self.canonical2type[gram_text], self.unk_id), start, end])

        for type_id, beg, end in used_aliases:
            tokens_type_ids[beg:end] = [[type_id] * self.ned_features_size[0]] * (end - beg)

        return tokens_type_ids

    def lookup_smaller(self, tokens):

        tokens_type_ids = []
        i = 0
        while i < len(tokens):
            token = tokens[i]
            # sort by number of tokens so longer keys get matched first
            matched_items = sorted(self.all_canonicals.keys(token), key=lambda item: len(item), reverse=True)
            found = False
            for key in matched_items:
                type = self.canonical2type[key]
                key_tokenized = key.split()
                cur = i
                j = 0
                while cur < len(tokens) and j < len(key_tokenized):
                    if tokens[cur] != key_tokenized[j]:
                        break
                    j += 1
                    cur += 1

                if j == len(key_tokenized):
                    if is_banned(' '.join(key_tokenized)):
                        continue

                    # match found
                    found = True
                    tokens_type_ids.extend([[self.typeqid2id[type] * self.ned_features_size[0]] for _ in range(i, cur)])

                    # move i to current unprocessed position
                    i = cur
                    break

            if not found:
                tokens_type_ids.append([self.unk_id * self.ned_features_size[0]])
                i += 1

        return tokens_type_ids

    def lookup_longer(self, tokens):
        i = 0
        tokens_type_ids = []

        length = len(tokens)
        found = False
        while i < length:
            end = length
            while end > i:
                tokens_str = ' '.join(tokens[i:end])
                if tokens_str in self.all_canonicals:
                    # match found
                    found = True
                    tokens_type_ids.extend(
                        [[self.typeqid2id[self.canonical2type[tokens_str]] * self.ned_features_size[0]] for _ in range(i, end)]
                    )
                    # move i to current unprocessed position
                    i = end
                    break
                else:
                    end -= 1
            if not found:
                tokens_type_ids.append([self.unk_id * self.ned_features_size[0]])
                i += 1
            found = False

        return tokens_type_ids

    def lookup_entities(self, tokens, entities):
        tokens_type_ids = [[self.unk_id] * self.ned_features_size[0]] * len(tokens)
        tokens_text = " ".join(tokens)

        for ent in entities:
            if ent not in self.all_canonicals:
                continue
            ent_num_tokens = len(ent.split(' '))
            idx = tokens_text.index(ent)
            token_pos = len(tokens_text[:idx].strip().split(' '))

            type = self.typeqid2id.get(self.canonical2type[ent], self.unk_id)

            tokens_type_ids[token_pos : token_pos + ent_num_tokens] = [[type] * self.ned_features_size[0]] * ent_num_tokens

        return tokens_type_ids

    def lookup(self, tokens, database_lookup_method=None, min_entity_len=2, max_entity_len=4, answer_entities=None):

        tokens_type_ids = [[self.unk_id] * self.ned_features_size[0]] * len(tokens)

        if answer_entities is not None:
            tokens_type_ids = self.lookup_entities(tokens, answer_entities)
        else:
            if database_lookup_method == 'smaller_first':
                tokens_type_ids = self.lookup_smaller(tokens)
            elif database_lookup_method == 'longer_first':
                tokens_type_ids = self.lookup_longer(tokens)
            elif database_lookup_method == 'ngrams':
                tokens_type_ids = self.lookup_ngrams(tokens, min_entity_len, max_entity_len)

        return tokens_type_ids
