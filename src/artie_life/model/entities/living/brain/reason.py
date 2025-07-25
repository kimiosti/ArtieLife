"""Module containing the implementation of the Reason lobe."""
from typing import TYPE_CHECKING
from numpy import array, zeros, float64, copy, max, argmax, inf
from numpy.random import uniform, choice
from keras.api.losses import Huber
from keras.api.optimizers import RMSprop
from tensorflow import GradientTape
from utils.living.genome import Gene
from utils.living.actions import Action, EntityType
from utils.living.learning.reason import REASON_MODEL, INPUT_LAYER_DIM

if TYPE_CHECKING:
    from typing import Dict, List
    from numpy.typing import NDArray
    from utils.living.needs import Need

def to_observation(focus: "EntityType", needs: "Dict[Need, float]") -> "NDArray[float64]":
    """Transforms the entity type's focus and the entity's needs into an observation.
    
    Arguments:  
    `focus`: the object of the living being's focus.  
    `needs`: the living being's needs."""
    res: "List[float]" = [ ]
    for entity_type in EntityType:
        if entity_type == focus:
            res.append(1)
        else:
            res.append(0)
    for value in needs.values():
        res.append(value)
    return array(res, dtype=float64).reshape((1, INPUT_LAYER_DIM))

class Reason:
    """Implementation of the Reason lobe."""
    def __init__(self, genome: "Dict[Gene, float]") -> "None":
        """Instantiates the Reason lobe.
        
        Arguments:  
        `genome`: the living being's genome."""
        self.model = REASON_MODEL
        self.genome = genome
        self.epsilon: "float" = self.genome[Gene.REASON_STARTING_EPSILON]
        self.prev_obs = zeros((1, INPUT_LAYER_DIM), dtype=float64)
        self.action: "Action" = Action.INTERACT
        self.focus: "EntityType" = EntityType.LIVING
        self.fitness: "float" = 100
        self.last_perception: "Dict[EntityType, float]" = {
            entity_type: 0 for entity_type in EntityType
        }
        self.user_reward: "float" = 0
        self.elapsed_time: "float" = 0

    def apply_user_reward(self, reward: "float") -> "None":
        """Actuates a user-defined reward on the living being.
        
        Arguments:  
        `reward`: the user-defined reward."""
        self.user_reward += reward * self.genome[Gene.REASON_USER_REWARD_MULTIPLIER]

    def update(self, focus: "EntityType", needs: "Dict[Need, float]", fitness: "float",
               perception: "Dict[EntityType, float]", elapsed_time: "float") -> "bool":
        """Performs a single step.
        
        Arguments:  
        `focus`: the object of the living being's focus.  
        `needs`: the current living being's needs.  
        `fitness`: the current value of the living being's fitness.  
        `perception`: the current living being's perception.  
        `elapsed_time`: the amount of time elapsed since last update.
        
        Returns:  
        a `bool` representing whether a new action was chosen."""
        self.elapsed_time += elapsed_time
        if self.elapsed_time >= self.genome[Gene.REASON_DECISION_PERIOD]:
            loss = Huber()
            optimizer = RMSprop(self.genome[Gene.REASON_ALPHA])
            observation = to_observation(focus, needs)
            next_action: "Action"
            if uniform() <= self.epsilon:
                next_action = choice(Action)
            else:
                next_action_pred = self.model(observation)
                action_idx = argmax(next_action_pred)
                for action in Action:
                    if action.value == action_idx:
                        next_action = action
            with GradientTape() as tape:
                prediction = self.model(self.prev_obs, training=True)
                rewards = copy(prediction)
                rewards[0, self.action.value] += (
                    self.genome[Gene.REASON_USER_REWARD_MULTIPLIER] * self.user_reward
                    + (
                        self.genome[Gene.REASON_FITNESS_REWARD_MULTIPLIER] * (
                            fitness - self.fitness
                        )
                    )
                    - (
                        self.genome[Gene.REASON_POSITIONAL_REWARD_MULTIPLIER] * (
                            perception[self.focus] - self.last_perception[self.focus]
                        )
                    )
                )
                error = loss(rewards, prediction)
            gradients = tape.gradient(error, self.model.trainable_weights)
            optimizer.apply_gradients(zip(gradients, self.model.trainable_weights))
            self.epsilon = max([
                self.epsilon * self.genome[Gene.REASON_EPSILON_DECAY],
                self.genome[Gene.REASON_MIN_EPSILON]
            ])
            self.prev_obs = observation
            self.action = next_action
            self.focus = focus
            self.fitness = fitness
            self.last_perception = perception
            self.user_reward = 0
            self.elapsed_time = 0
            return True
        return False
