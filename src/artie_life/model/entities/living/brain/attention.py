"""Module containing attention lobe implementations."""
from typing import TYPE_CHECKING
from random import choice
from numpy import array
from numpy.random import uniform, choice as np_choice
from tensorflow import GradientTape
from keras.api.ops import argmax as keras_argmax
from keras.api.losses import huber as loss
from keras.api.optimizers import Adam
from utils.living.genome import Gene
from utils.living.actions import EntityType
from utils.living.learning.commons import BATCH_SIZE, REPLAY_BUFFER_SIZE
from utils.living.learning.attention import create_attention_model

if TYPE_CHECKING:
    from typing import Dict, List
    from numpy.typing import NDArray
    from numpy import floating

def pick_random_focus() -> "EntityType":
    """Randomly computes a new acceptable value for the entity's focus."""
    next_focus: "EntityType" = choice(list(EntityType))
    while next_focus in [EntityType.LIVING, EntityType.PLAYGROUND]:
        next_focus = choice(list(EntityType))
    return next_focus

class Attention:
    """Implementation of a random-behaving attention lobe."""

    def __init__(self, genome: "Dict[Gene, float]") -> "None":
        """Instantiates the attention lobe.
        
        Positional arguments:  
         - `genome`: the living being's genome."""
        self.genome = genome
        self.focus = pick_random_focus()

    def update(self) -> "None":
        """Performs a single random-behaving attention step."""
        self.focus = pick_random_focus()


class LearningAttention(Attention):
    """Implementation of a learning attention lobe."""

    def __init__(self, genome: "Dict[Gene, float]") -> "None":
        """Instantiates the attention lobe.
        
        Positional arguments:  
         - `genome`: the living being's genome."""
        super().__init__(genome)
        self.first_frame = True
        self.model = create_attention_model()
        self.target_model = create_attention_model()
        self.optimizer = Adam(self.genome[Gene.ATTENTION_LEARNING_RATE])
        self.elapsed_time: "float" = 0.0
        self.elapsed_time_target: "float" = 0.0
        self.epsilon = self.genome[Gene.ATTENTION_STARTING_EPSILON]
        self.state_hist: "List[NDArray[floating]]" = []
        self.reward_hist: "List[NDArray[floating]]" = []
        self.next_state_hist: "List[NDArray[floating]]" = []

    def update_and_learn(self, state: "NDArray[floating]", reward: "NDArray[floating]",
               elapsed_time: "float") -> "None":
        """Performs a single update step for the Attention lobe.
        
        Positional arguments:  
         - `state`: the current environment observation. Must be normalized by the \
        central lobe, if necessary.  
         - `reward`: the actual reward values for each possible lobe decision.  
         - `elapsed_time`: the amount of time since last lobe update, in seconds."""
        if not self.first_frame:
            self.reward_hist.append(reward)
            self.next_state_hist.append(state)
        else:
            self.first_frame = False

        self.elapsed_time += elapsed_time
        self.elapsed_time_target += elapsed_time

        q_values = self.model(state.reshape(1, len(state)), training=False)
        if self.epsilon > uniform():
            self.focus = pick_random_focus()
        else:
            for entity_type in EntityType:
                if entity_type.value == keras_argmax(q_values, axis=1):
                    self.focus = entity_type
        self.epsilon = max(
            self.genome[Gene.ATTENTION_MIN_EPSILON],
            self.epsilon * self.genome[Gene.ATTENTION_EPSILON_DECAY]
        )

        if self.elapsed_time > self.genome[Gene.ATTENTION_UPDATE_PERIOD] \
                and len(self.reward_hist) > BATCH_SIZE:
            self.elapsed_time = 0.0
            indices = np_choice(len(self.reward_hist), BATCH_SIZE)

            state_samples = array([self.state_hist[i] for i in indices])
            reward_samples = array([self.reward_hist[i] for i in indices])
            next_state_samples = array([self.next_state_hist[i] for i in indices])

            next_reward_predictions = self.target_model.predict(next_state_samples)

            updated_q_values = reward_samples + self.genome[Gene.ATTENTION_GAMMA] \
                * next_reward_predictions

            with GradientTape() as tape:
                pred_q_values = self.model(state_samples)
                loss_values = loss(updated_q_values, pred_q_values)
            grads = tape.gradient(loss_values, self.model.trainable_variables)
            self.optimizer.apply_gradients(zip(
                grads,
                self.model.trainable_variables
            ))

        if self.elapsed_time_target > self.genome[Gene.ATTENTION_TARGET_UPDATE_PERIOD]:
            self.elapsed_time_target = 0.0
            self.target_model.set_weights(self.model.get_weights())

        if len(self.reward_hist) > REPLAY_BUFFER_SIZE:
            self.state_hist.clear()
            self.reward_hist.clear()
            self.next_state_hist.clear()
            self.first_frame = True

        self.state_hist.append(state)
