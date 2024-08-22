"""Adapted from https://pytorch.org/tutorials/intermediate/char_rnn_classification_tutorial.html"""

import torch
from torch.autograd import Variable
import random

import os
import time
import math
import unicodedata

from model.constants import ALL_LETTERS, N_LETTERS


def unicodeToAscii(s: str) -> str:
    """ Turn a Unicode string to plain ASCII, thanks to http://stackoverflow.com/a/518232/2809427 """
    return "".join(
        c
        for c in unicodedata.normalize("NFD", s)
        if unicodedata.category(c) != "Mn" and c in ALL_LETTERS
    )


def readLines(filename: str) -> list:
    """ Read a file and split into lines """
    lines = open(filename).read().strip().split("\n")
    return [unicodeToAscii(line) for line in lines]


def get_categories(data_path: str) -> tuple[list, dict]:
    """ Build the category_lines dictionary and a list of lines per category """
    category_lines = {}
    all_categories = []
    for filename in os.listdir(data_path):
        category = filename.split("/")[-1].split(".")[0]
        all_categories.append(category)
        lines = readLines(os.path.join(data_path, filename))
        category_lines[category] = lines

    return all_categories, category_lines


def letterToIndex(letter: str) -> int:
    """ Find letter index from all_letters, e.g. "a" = 0 """
    return ALL_LETTERS.find(letter)


def lineToTensor(line):
    """
     Turn a line into a <line_length x 1 x n_letters>,
     or an array of one-hot letter vectors
    """
    tensor = torch.zeros(len(line), 1, N_LETTERS)
    for li, letter in enumerate(line):
        tensor[li][0][letterToIndex(letter)] = 1
    return tensor


def categoryFromOutput(output, all_categories: dict) -> str:
    top_n, top_i = output.data.topk(1)  # Tensor out of Variable with .data
    category_i = top_i[0][0]
    return all_categories[category_i]


def randomChoice(l: list) -> int:
    return l[random.randint(0, len(l) - 1)]


def randomTrainingPair(all_categories: list, category_lines: dict):
    category = randomChoice(all_categories)
    line = randomChoice(category_lines[category])
    category_tensor = Variable(torch.LongTensor([all_categories.index(category)]))
    line_tensor = Variable(lineToTensor(line))
    return category, line, category_tensor, line_tensor


def timeSince(since):
    now = time.time()
    s = now - since
    m = math.floor(s / 60)
    s -= m * 60
    return "%dm %ds" % (m, s)
