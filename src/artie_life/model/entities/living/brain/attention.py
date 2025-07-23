"""Module containing the Attention lobe implementation."""
from typing import TYPE_CHECKING
from numpy import zeros, array, float64, argmax, copy
from keras.api.losses import Huber
from keras.api.optimizers import RMSprop
from tensorflow import GradientTape
from utils.living.genome import Gene
from utils.living.actions import EntityType
from utils.living.learning.attention import ATTENTION_MODEL, INPUT_LAYER_DIM, MAX_INPUT_LENGTH

if TYPE_CHECKING:
    from typing import List, Dict, Tuple
    from numpy.typing import NDArray

def to_observation(text: "str",
                   perception: "Dict[EntityType, Tuple[float, float]]") -> "NDArray[float64]":
    """Translates user input and living being's perceptions into a numpy array.
    
    Arguments:  
    `text`: user input.
    `perception`: the living being's perception of the environment."""
    res: "List[float]" = list(text.encode("utf-8"))
    while len(res) < MAX_INPUT_LENGTH:
        res.append(0)
    for x, y in perception.values():
        res.append(x)
        res.append(y)
    return array(res, dtype=float64).reshape((1, INPUT_LAYER_DIM))


class Attention:
    """Implementation of the Attention lobe."""
    def __init__(self, genome: "Dict[Gene, float]") -> "None":
        """Instantiates the Attention lobe.
        
        Arguments:  
        `genome`: the living being's genome."""
        self.genome = genome
        self.model = ATTENTION_MODEL
        self.prev_obs: "NDArray[float64]" = zeros((1, INPUT_LAYER_DIM), dtype=float64)
        self.focus: "EntityType" = EntityType.LIVING
        self.elapsed_time: "float" = 0
        self.reward: "float" = 0
        self.input: "str" = ""

    def apply_user_reward(self, reward: "float") -> "None":
        """Applies the desired reward to the living being.
        
        Arguments:  
        `reward`: the desired reward value to apply."""
        self.reward += reward * self.genome[Gene.ATTENTION_USER_REWARD_MULTIPLIER]

    def update(self, elapsed_time: "float",
               perception: "Dict[EntityType, Tuple[float, float]]") -> "None":
        """Performs a single update step.
        
        Arguments:  
        `elapsed_time`: the amount of time elapsed since last update step."""
        self.elapsed_time += elapsed_time
        if self.elapsed_time >= self.genome[Gene.ATTENTION_DECISION_PERIOD]:
            loss = Huber()
            optimizer = RMSprop(self.genome[Gene.ATTENTION_ALPHA])
            next_focus: "EntityType"
            observation = to_observation(self.input, perception)
            next_focus_prediction: "NDArray[float64]" = self.model.predict(observation)
            next_focus_idx = argmax(next_focus_prediction)
            for entity_type in EntityType:
                if entity_type.value == next_focus_idx:
                    next_focus = entity_type
            with GradientTape() as tape:
                prediction = self.model(self.prev_obs, training=True)
                rewards = copy(prediction)
                rewards[0, self.focus.value] = self.reward
                error = loss(rewards, prediction)
            gradients = tape.gradient(error, self.model.trainable_weights)
            optimizer.apply_gradients(zip(gradients, self.model.trainable_weights))
            self.elapsed_time = 0
            self.prev_obs = observation
            self.focus = next_focus
            self.input = ""
            self.reward = 0
