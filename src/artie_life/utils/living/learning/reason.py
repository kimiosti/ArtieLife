"""Module containing utilities for the Reason lobe."""
from typing import TYPE_CHECKING
from numpy import array
from numpy.linalg import norm
from keras import Sequential
from keras import layers
from utils.living.actions import Action, EntityType
from utils.living.learning.commons import POSITIVE_MOVEMENT_REWARD, NEGATIVE_MOVEMENT_REWARD, \
    PRIMARY_REWARD_MULTIPLIER, SECONDARY_REWARD_MULTIPLIER, POSITIVE_NEEDS_REWARD

if TYPE_CHECKING:
    from typing import Dict, Tuple, List
    from numpy import floating
    from numpy.typing import NDArray

INPUT_LAYER_DIM: "int" = len(EntityType) - 2 + ((len(EntityType) - 2) * 2)
OUTPUT_LAYER_DIM: "int" = len(Action)

def compute_reward(user_reward: "float", needs_reward: "float",
                   last_perception: "Dict[EntityType, Tuple[float, float]]",
                   last_focus: "EntityType") -> "NDArray[floating]":
    """Computes the reward values for each decision step of the Reason lobe.
    
    Positional arguments:  
     - `user_reward`: the user-defined reward.  
     - `needs_reward`: the self-derived reward depending on the living being's vital \
    parameters.  
     - `last_perception`: the last frame's bidimensional distance from the closest \
        instance of each type of entity, grouped by `EntityType`.  
     - `last_focus`: the last focus object of the living being.
    
    Return:  
    A `NDArray` of `floating` values representing the reward values for each possible action \
    of the Reason lobe."""
    reward: "List[float]" = []
    for action in Action:
        single_reward = SECONDARY_REWARD_MULTIPLIER * user_reward \
            + PRIMARY_REWARD_MULTIPLIER * (
                POSITIVE_NEEDS_REWARD
                if norm(last_perception[last_focus]) == 0 and action == Action.INTERACT
                else needs_reward
        ) + PRIMARY_REWARD_MULTIPLIER * (
                POSITIVE_MOVEMENT_REWARD
                if last_perception[last_focus][0] * action.get_direction()[0] > 0
                or last_perception[last_focus][0] * action.get_direction()[0] > 0
                else (0 if action == Action.INTERACT else NEGATIVE_MOVEMENT_REWARD)
        )
        reward.append(single_reward)
    return array(reward)

def assemble_state(focus: "EntityType",
                   perception: "Dict[EntityType, Tuple[float, float]]") -> "NDArray":
    """Assembles a state vector for the Reason lobe predictor.
    
    Positional arguments:  
     - `focus`: the type of the entity on which the living being has posed its attention.  
     - `perception`: the distance from the closest instance of each type of entity, \
    grouped by `EntityType` and represented as a bidimensional `Tuple`.
    
    Return:  
    A `NDArray` of `floating` values suitable for the Reason lobe predictor."""
    state: "List[float]" = []
    for entity_type in EntityType:
        if entity_type not in [EntityType.PLAYGROUND, EntityType.LIVING]:
            state.append(1.0 if entity_type == focus else 0.0)
    for entity_type, coordinates in perception.items():
        if entity_type not in [EntityType.PLAYGROUND, EntityType.LIVING]:
            state += [coordinates[0], coordinates[1]]
    return array(state)

def create_reason_model() -> "Sequential":
    """Instantiates the model underlying the Reason lobe."""
    return Sequential([
        layers.Input(shape=(INPUT_LAYER_DIM,)),
        layers.Dense(8, activation="relu"),
        layers.Dense(OUTPUT_LAYER_DIM)
    ])
