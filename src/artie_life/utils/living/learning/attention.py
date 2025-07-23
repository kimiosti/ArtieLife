"""Module containing attention lobe utilities."""
from keras import Sequential
from keras.api.layers import Input, Dense
from utils.living.actions import EntityType

MAX_INPUT_LENGTH: "int" = 8
POSITIVE_REWARD: "float" = 1
NEGATIVE_REWARD: "float" = -1
INPUT_LAYER_DIM: "int" = 2 * (len(EntityType) - 1) + MAX_INPUT_LENGTH
OUTPUT_LAYER_DIM: "int" = len(EntityType) - 1

ATTENTION_MODEL: "Sequential" = Sequential([
    Input(shape=(INPUT_LAYER_DIM,)),
    Dense(32, activation="relu"),
    Dense(16, activation="relu"),
    Dense(8, activation="relu"),
    Dense(OUTPUT_LAYER_DIM)
])
