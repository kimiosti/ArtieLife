"""Module containing attention lobe utilities."""
from typing import TYPE_CHECKING
from keras import Sequential
from keras import layers
from numpy import array, append
from numpy.linalg import norm
from utils.living.learning.commons import POSITIVE_MOVEMENT_REWARD, NEGATIVE_MOVEMENT_REWARD, \
    PRIMARY_REWARD_MULTIPLIER, SECONDARY_REWARD_MULTIPLIER, BATCH_SIZE
from utils.living.actions import EntityType
from utils.living.needs import Need

if TYPE_CHECKING:
    from typing import Dict, Tuple, List, Any
    from numpy.typing import NDArray
    from numpy import floating

MAX_INPUT_LENGTH: "int" = 8
INPUT_LAYER_DIM: "int" = MAX_INPUT_LENGTH + len(EntityType) - 2 + len(Need) - 1
OUTPUT_LAYER_DIM: "int" = len(EntityType) - 2

def compute_reward(user_reward: "float", needs_reward: "float",
                   last_perception: "Dict[EntityType, Tuple[float, float]]",
                   cur_perception: "Dict[EntityType, Tuple[float, float]]") -> "NDArray[floating]":
    """Computes the actual reward values for each possible focus choice.
    
    Positional arguments:  
     - `user_reward`: the user-defined reward.  
     - `needs_reward`: a self-determined reward derived from the living being's vital needs.  
     - `last_perception`: a `Dict` associating to each `EntityType` a `Tuple` representing \
    the bidimensional distance between the living being and the closest instance of \
    said `EntityType`.  
     - `cur_perception`: the current living being's perception value, represented in the same \
    way as `last_perception`.
    
    Return:  
    A `NDArray` of `floating` values representing the reward values for each possible \
    `EntityType` on wich the living being directs its focus."""
    rewards: "List[float]" = []
    for entity_type, last_distance in last_perception.items():
        if entity_type not in [EntityType.PLAYGROUND, EntityType.LIVING]:
            single_reward: "float" = 0.0
            if norm(last_distance) < norm(cur_perception[entity_type]):
                single_reward += NEGATIVE_MOVEMENT_REWARD * SECONDARY_REWARD_MULTIPLIER
            else:
                single_reward += POSITIVE_MOVEMENT_REWARD * SECONDARY_REWARD_MULTIPLIER
            single_reward += needs_reward * SECONDARY_REWARD_MULTIPLIER
            single_reward += user_reward * PRIMARY_REWARD_MULTIPLIER
            rewards.append(single_reward)
    return array(rewards)

def assemble_state(input_text: "str", perception: "Dict[EntityType, Tuple[float, float]]",
                   needs: "Dict[Need, float]") -> "NDArray[floating]":
    """Assemble a single state vector, used for model prediction.
    
    Positional arguments:  
     - `input_text`: the user-defined text input.  
     - `perception`: the current living being perception of the game world.  
     - `needs`: the current values of the living being's vital parameters."""
    state: "NDArray[floating]" = array(list(input_text.encode("ASCII")))
    if len(state) < MAX_INPUT_LENGTH:
        state = append(state, [0.0 for _ in range(MAX_INPUT_LENGTH - len(state))])
    for entity_type, distance in perception.items():
        if entity_type not in [EntityType.PLAYGROUND, EntityType.LIVING]:
            state = append(state, norm(distance))
    state = append(state, [value for _, value in needs.items()])
    return state

def create_attention_model() -> "Sequential":
    """Instantiates the model underlying the Attention lobe."""
    return Sequential([
        layers.Input(shape=(INPUT_LAYER_DIM,)),
        layers.Dense(16, activation="relu"),
        layers.Dense(8, activation="relu"),
        layers.Dense(4, activation="relu"),
        layers.Dense(OUTPUT_LAYER_DIM)
    ])
