#!/usr/bin/env python
'''
architect
Created by Seria at 2021/5/22 11:23 AM
Email: zzqsummerai@yeah.net

                    _ooOoo_
                  o888888888o
                 o88`_ . _`88o
                 (|  0   0  |)
                 O \   。   / O
              _____/`-----‘\_____
            .’   \||  _ _  ||/   `.
            |  _ |||   |   ||| _  |
            |  |  \\       //  |  |
            |  |    \-----/    |  |
             \ .\ ___/- -\___ /. /
         ,--- /   ___\<|>/___   \ ---,
         | |:    \    \ /    /    :| |
         `\--\_    -. ___ .-    _/--/‘
   ===========  \__  NOBUG  __/  ===========
   
'''
# -*- coding:utf-8 -*-
from ... import dock

import numpy as np


class RNNE(dock.Craft):
    def __init__(self, in_chs, hidden_dim, nlayers, voc_size, scope='RNNE'):
        super(RNNE, self).__init__(scope)
        self.emb = dock.Embed(voc_size, in_chs)
        self.rnn = dock.RNN(in_chs, hidden_dim, nlayers)

    def run(self, x, h=None):
        x = self.emb(x)
        y, h = self.rnn(x, h)
        return y, h


class BiRNNE(dock.Craft):
    def __init__(self, in_chs, hidden_dim, nlayers, voc_size, scope='BIRNNE'):
        super(BiRNNE, self).__init__(scope)
        self.emb = dock.Embed(voc_size, in_chs)
        self.birnn = dock.BiRNN(in_chs, hidden_dim, nlayers)

    def run(self, x, h=None):
        x = self.emb(x)
        y, h = self.birnn(x, h)
        return y, h


class RNND(dock.Craft):
    def __init__(self, in_chs, hidden_dim, nlayers, voc_size, scope='RNND'):
        super(RNND, self).__init__(scope)
        self.emb = dock.Embed(voc_size, in_chs)
        self.relu = dock.Relu()
        self.rnn = dock.RNN(in_chs, hidden_dim, nlayers)
        self.fc = dock.Dense(hidden_dim, voc_size)

    def run(self, x, h=None):
        x = self.emb(x)
        x = self.relu(x)
        y, h = self.rnn(x, h)
        y = self.fc(y)
        return y, h


class AttnRNND(dock.Craft):
    def __init__(self, in_chs, hidden_dim, nlayers, voc_size, max_len, scope='ATTNRNND'):
        super(AttnRNND, self).__init__(scope)
        self.emb = dock.Embed(voc_size, in_chs)
        self.lut = [p for p in self.emb.vars()]
        self.relu = dock.Relu()
        self.rnn = dock.RNN(in_chs, hidden_dim, nlayers)
        self.fc = dock.Dense(hidden_dim, voc_size)
        self.drp = dock.Dropout(0.1, dim=1)
        # self.perm = dock.Permute()
        # self.sqsh = dock.Squash()
        # self.expd = dock.Expand()

        self.attn = dock.Dense(in_chs+hidden_dim, max_len)
        self.proj = dock.Dense(hidden_dim+hidden_dim, hidden_dim)
        self.dot = dock.Dot()
        self.cat = dock.Concat()
        self.sftm = dock.Sftm()

    def run(self, x, o, h=None):
        x = self.emb(x)
        x = self.drp(x)

        a = self.cat((x, h))
        a = self.attn(a)
        a = self.sftm(a)
        a = self.dot(a, o, in_batch=True)
        h = self.cat((h, a))
        h = self.proj(h)

        x = self.relu(x)
        y, h = self.rnn(x, h)
        y = self.fc(y)
        # y = self.expd(self.dot(self.sqsh(y, 0), self.perm(self.lut[0], (1,0))), 0)
        return y, h


# class AttnRNND(dock.Craft):
#     def __init__(self, in_chs, hidden_dim, nlayers, voc_size, max_len, scope='ATTNRNND'):
#         super(AttnRNND, self).__init__(scope)
#         self.emb = dock.Embed(voc_size, in_chs)
#         self.perm = dock.Permute()
#         self.expd = dock.Expand()
#         self.relu = dock.Relu()
#         self.rnn = dock.RNN(in_chs, hidden_dim, nlayers)
#         self.fc = dock.Dense(hidden_dim, voc_size)
#
#         self.attn = dock.Dense(hidden_dim+hidden_dim, hidden_dim)
#         self.mat = dock.Dense(hidden_dim, 1)
#         self.proj = dock.Dense(hidden_dim+hidden_dim, hidden_dim)
#         self.dot = dock.Dot()
#         self.cat = dock.Concat()
#         self.sftm = dock.Sftm()
#
#     def run(self, x, o, h=None):
#         x = self.emb(x)
#         l = o.shape[1]
#         _h = self.perm(self.cat(l*[h], 0), (1, 0, 2))
#
#         a = self.cat((o, _h)) # B x L x 2H
#         a = self.attn(a) # B x L x H
#         a = self.relu(a)
#         a = self.perm(self.mat(a), (0, 2, 1)) # B x 1 x L
#         a = self.sftm(a)
#         a = self.dot(a, o, in_batch=True)
#         x = self.cat((x, a))
#         x = self.proj(x)
#
#         x = self.relu(x)
#         y, h = self.rnn(x, h)
#         y = self.fc(y)
#         return y, h


class LSTME(dock.Craft):
    def __init__(self, in_chs, hidden_dim, nlayers, voc_size, scope='LSTME'):
        super(LSTME, self).__init__(scope)
        self.emb = dock.Embed(voc_size, in_chs)
        self.lstm = dock.LSTM(in_chs, hidden_dim, nlayers)

    def run(self, x, h=None, c=None):
        x = self.emb(x)
        y, h, c = self.lstm(x, h, c)
        return y, h, c


class LSTMD(dock.Craft):
    def __init__(self, in_chs, hidden_dim, nlayers, voc_size, attention=0, scope='LSTMD'):
        super(LSTMD, self).__init__(scope)
        self.emb = dock.Embed(voc_size, in_chs)
        self.relu = dock.Relu()
        self.lstm = dock.LSTM(in_chs, hidden_dim, nlayers)
        self.fc = dock.Dense(hidden_dim, voc_size)
        if attention>0:
            self.attn = dock.Dense(in_chs+hidden_dim, attention)

    def run(self, x, h=None, c=None):
        x = self.emb(x)
        x = self.relu(x)
        y, h, c = self.lstm(x, h, c)
        y = self.fc(y)
        return y, h, c


class AttnLSTMD(dock.Craft):
    def __init__(self, in_chs, hidden_dim, nlayers, voc_size, max_len, scope='ATTNLSTMD'):
        super(AttnLSTMD, self).__init__(scope)
        self.emb = dock.Embed(voc_size, in_chs)
        self.relu = dock.Relu()
        self.rnn = dock.LSTM(in_chs, hidden_dim, nlayers)
        self.fc = dock.Dense(hidden_dim, voc_size)

        self.attn = dock.Dense(in_chs+hidden_dim, max_len)
        self.proj = dock.Dense(hidden_dim+hidden_dim, hidden_dim)
        self.dot = dock.Dot()
        self.cat = dock.Concat()
        self.sftm = dock.Sftm()

    def run(self, x, o, h=None, c=None):
        x = self.emb(x)

        a = self.cat((x, c))
        a = self.attn(a)
        a = self.sftm(a)
        a = self.dot(a, o, in_batch=True)
        c = self.cat((c, a))
        c = self.proj(c)

        x = self.relu(x)
        y, h, c = self.rnn(x, h, c)
        y = self.fc(y)
        return y, h, c