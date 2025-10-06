"""Module containing common utilities for the learning process."""

BATCH_SIZE: "int" = 32
REPLAY_BUFFER_SIZE: "int" = 1000
PRIMARY_REWARD_MULTIPLIER: "float" = 1.2
SECONDARY_REWARD_MULTIPLIER: "float" = 0.75

USER_INTERACTION_PERIOD: "float" = 2.0

POSITIVE_USER_REWARD: "float" = 1.0
NEGATIVE_USER_REWARD: "float" = -1.0
POSITIVE_MOVEMENT_REWARD: "float" = 1.5
NEGATIVE_MOVEMENT_REWARD: "float" = -0.5
POSITIVE_NEEDS_REWARD: "float" = 1.5
NEGATIVE_NEEDS_REWARD: "float" = -0.5
