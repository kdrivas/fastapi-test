import torch
from torch.autograd import Variable
import logging

from model.constants import N_HIDDEN, N_CATEGORIES, N_LETTERS
from model.classifier import RNN
from model.utils import lineToTensor

logger = logging.getLogger(__name__)


def load_model(weights_file: str) -> RNN:
    rnn = RNN(input_size=N_LETTERS, hidden_size=N_HIDDEN, output_size=N_CATEGORIES)
    rnn.load_state_dict(torch.load(weights_file))
    rnn.eval()

    return rnn


def evaluate(line_tensor: Variable, model):
    """ Just return an output given a line """
    hidden = model.initHidden()

    for i in range(line_tensor.size()[0]):
        output, hidden = model(line_tensor[i], hidden)

    return output  


def predict(name: str, n_predictions: int, model, all_categories: dict):
    output = evaluate(Variable(lineToTensor(name)), model)  

    # Get top N categories
    topv, topi = output.data.topk(n_predictions, 1, True)
    predictions = []
    probabilities = []

    for i in range(n_predictions):
        value = topv[0][i]
        category_index = topi[0][i]
        predictions.append(all_categories[category_index])
        probabilities.append(value.item())

    return predictions, probabilities
