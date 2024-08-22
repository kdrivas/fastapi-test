"""Adapted from https://pytorch.org/tutorials/intermediate/char_rnn_classification_tutorial.html"""

import torch
import torch.nn as nn
import pickle
import time
import os

from model.classifier import RNN
from model.utils import get_categories, randomTrainingPair, categoryFromOutput, timeSince
from model.constants import (
    N_HIDDEN,
    N_LETTERS,
    LEARNING_RATE,
    N_EPOCHS,
    PLOT_EVERY,
    PRINT_EVERY,
)


def make_step(category_tensor, line_tensor, rnn, optimizer, criterion):
    hidden = rnn.initHidden()
    optimizer.zero_grad()

    for i in range(line_tensor.size()[0]):
        output, hidden = rnn(line_tensor[i], hidden)

    loss = criterion(output, category_tensor)
    loss.backward()

    optimizer.step()

    return output, loss.data.item()


def train(filename: str, artifact_path: str = "") -> None:
    all_categories, category_lines = get_categories(filename)
    n_categories = len(all_categories)

    rnn = RNN(input_size=N_LETTERS, hidden_size=N_HIDDEN, output_size=n_categories)
    optimizer = torch.optim.SGD(rnn.parameters(), lr=LEARNING_RATE)
    criterion = nn.NLLLoss()

    # Keep track of losses for plotting
    current_loss = 0
    all_losses = []

    start = time.time()

    for epoch in range(1, N_EPOCHS + 1):
        category, line, category_tensor, line_tensor = randomTrainingPair(
            all_categories, category_lines,
        )
        output, loss = make_step(category_tensor, line_tensor, rnn, optimizer, criterion)
        current_loss += loss

        # Print epoch number, loss, name and guess
        if epoch % PRINT_EVERY == 0:
            guess = categoryFromOutput(output, all_categories)
            correct = "✓" if guess == category else "✗ (%s)" % category
            print(
                "%d %d%% (%s) %.4f %s / %s %s"
                % (
                    epoch,
                    epoch / N_EPOCHS * 100,
                    timeSince(start),
                    loss,
                    line,
                    guess,
                    correct,
                )
            )

        # Add current loss avg to list of losses
        if epoch % PLOT_EVERY == 0:
            all_losses.append(current_loss / PLOT_EVERY)
            current_loss = 0

    torch.save(rnn.state_dict(), os.path.join(artifact_path, "model.pt"))

    with open(os.path.join(artifact_path, "categories.pkl"), "wb") as f:
        pickle.dump(all_categories, f)
