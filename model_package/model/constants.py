import string

ALL_LETTERS = string.ascii_letters + " .,;'-"
N_LETTERS = len(ALL_LETTERS)

# Model configuration
N_HIDDEN = 128
N_CATEGORIES = 18
N_EPOCHS = 100000
PRINT_EVERY = 5000
PLOT_EVERY = 1000
LEARNING_RATE = (
    0.005  # If you set this too high, it might explode. If too low, it might not learn
)