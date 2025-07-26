"""Module containing utilities for the Reason lobe."""
from keras import Sequential
from keras import layers
from utils.living.needs import Need
from utils.living.actions import Action, EntityType

INPUT_LAYER_DIM: "int" = len(Need) + len(EntityType) - 1
OUTPUT_LAYER_DIM: "int" = len(Action)

def create_reason_model() -> "Sequential":
    """Instantiates the model underlying the Reason lobe."""
    return Sequential([
        layers.Input(shape=(INPUT_LAYER_DIM,)),
        layers.Dense(16, activation="relu", kernel_initializer="random_uniform"),
        layers.Dense(32, activation="relu", kernel_initializer="random_uniform"),
        layers.Dense(16, activation="relu", kernel_initializer="random_uniform"),
        layers.Dense(OUTPUT_LAYER_DIM)
    ])
