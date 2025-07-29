"""Module containing the Attention lobe implementation."""
from typing import TYPE_CHECKING
from numpy import zeros, array, float64, argmax, copy
from numpy.linalg import norm
from keras.api.losses import Huber
from keras.api.optimizers import RMSprop
from tensorflow import GradientTape
from controller.log import AttentionLogger
from utils.living.genome import Gene
from utils.living.needs import Need
from utils.living.actions import EntityType
from utils.living.learning.attention import create_attention_model, INPUT_LAYER_DIM, \
        MAX_INPUT_LENGTH, POSITIVE_DISTANCE_REWARD, NEGATIVE_DISTANCE_REWARD, \
        POSITIVE_NEEDS_REWARD, NEGATIVE_NEEDS_REWARD

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
    def __init__(self, genome: "Dict[Gene, float]", living_id: "int") -> "None":
        """Instantiates the Attention lobe.
        
        Arguments:  
        `genome`: the living being's genome.  
        `living_id`: the living being's in-game ID."""
        self.genome = genome
        self.model = create_attention_model()
        self.prev_obs: "NDArray[float64]" = zeros((1, INPUT_LAYER_DIM), dtype=float64)
        self.prev_needs: "Dict[Need, float]" = {
            need: 0 for need in Need
        }
        self.focus: "EntityType" = EntityType.HEALING
        self.elapsed_time: "float" = 0
        self.user_reward: "float" = 0
        self.input: "str" = ""
        self.logger = AttentionLogger(living_id)

    def apply_user_reward(self, reward: "float") -> "None":
        """Applies the desired reward to the living being.
        
        Arguments:  
        `reward`: the desired reward value to apply."""
        self.user_reward += reward * self.genome[Gene.ATTENTION_USER_REWARD_MULTIPLIER]

    def compute_needs_reward(self, needs: "Dict[Need, float]") -> "float":
        """Computes the self-derived reward from a needs observation.
        
        Arguments:  
        `needs`: the actual needs observation.
        
        Returns:  
        A `float` representing the reward value."""
        if needs[Need.LIFE] >= self.prev_needs[Need.LIFE]:
            return NEGATIVE_NEEDS_REWARD * self.genome[Gene.ATTENTION_NEEDS_REWARD_MULTIPLIER]
        for need, value in needs.items():
            if value < self.prev_needs[need]:
                return POSITIVE_NEEDS_REWARD \
                        * self.genome[Gene.ATTENTION_NEEDS_REWARD_MULTIPLIER]
        return NEGATIVE_NEEDS_REWARD * self.genome[Gene.ATTENTION_NEEDS_REWARD_MULTIPLIER]

    def delta_distance(self, observation: "NDArray[float64]") -> "float":
        """Computes the delta distance since last observation, in the direction of  
        the object of the living being's focus.
        
        Arguments:  
        `observation`: the actual observation, used to compute the difference  
        in distance since last observation."""
        idx_x = MAX_INPUT_LENGTH + self.focus.value * 2
        idx_y = idx_x + 1
        return float(norm([self.prev_obs[0, idx_x], self.prev_obs[0, idx_y]]) \
                - norm([observation[0, idx_x], observation[0, idx_y]]))

    def update(self, elapsed_time: "float", needs: "Dict[Need, float]",
               perception: "Dict[EntityType, Tuple[float, float]]") -> "bool":
        """Performs a single update step.
        
        Arguments:  
        `elapsed_time`: the amount of time elapsed since last update step.
        
        Returns:  
        True if a new focus object is computed, false otherwise."""
        self.elapsed_time += elapsed_time
        if self.elapsed_time >= self.genome[Gene.ATTENTION_DECISION_PERIOD]:
            loss = Huber()
            optimizer = RMSprop(self.genome[Gene.ATTENTION_ALPHA])
            next_focus: "EntityType"
            observation = to_observation(self.input, perception)
            next_focus_prediction: "NDArray[float64]" = self.model(observation)
            next_focus_idx = argmax(next_focus_prediction)
            for entity_type in EntityType:
                if entity_type.value == next_focus_idx:
                    next_focus = entity_type
            with GradientTape() as tape:
                prediction = self.model(self.prev_obs, training=True)
                rewards = copy(prediction)
                distance_reward = self.genome[Gene.ATTENTION_POSITIONAL_REWARD_MULTIPLIER] \
                        * (POSITIVE_DISTANCE_REWARD \
                        if self.delta_distance(observation) > 0 \
                        else NEGATIVE_DISTANCE_REWARD)
                needs_reward = self.compute_needs_reward(needs)
                rewards[0, self.focus.value] = self.user_reward \
                            + distance_reward \
                            + needs_reward
                error = loss(rewards, prediction)
            gradients = tape.gradient(error, self.model.trainable_weights)
            optimizer.apply_gradients(zip(gradients, self.model.trainable_weights))
            self.logger.log_step(
                self.user_reward,
                needs_reward,
                self.genome[Gene.ATTENTION_POSITIONAL_REWARD_MULTIPLIER] * distance_reward,
                perception,
                self.input,
                next_focus
            )
            self.elapsed_time = 0
            self.prev_obs = observation
            self.focus = next_focus
            self.input = ""
            self.user_reward = 0
            return True
        return False
