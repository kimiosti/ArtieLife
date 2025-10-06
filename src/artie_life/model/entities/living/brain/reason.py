"""Module containing implementations for the reason lobes."""
from typing import TYPE_CHECKING
from random import choice
from numpy import array
from numpy.random import uniform, choice as np_choice
from keras.api.optimizers import Adam
from keras.api.losses import huber as loss
from keras.api.ops import argmax as keras_argmax
from tensorflow import GradientTape
from utils.living.genome import Gene
from utils.living.actions import Action
from utils.living.learning.reason import create_reason_model
from utils.living.learning.commons import BATCH_SIZE, REPLAY_BUFFER_SIZE

if TYPE_CHECKING:
    from typing import Dict, List
    from numpy import floating
    from numpy.typing import NDArray

class Reason:
    """Implementation of a random-acting reason lobe."""

    def __init__(self, genome: "Dict[Gene, float]") -> "None":
        """Instantiates the reason lobe.
        
        Positional arguments:  
         - `genome`: the living being's genome."""
        self.genome = genome
        self.action: "Action" = choice(list(Action))

    def update(self) -> "None":
        """Performs a single decision step."""
        self.action = choice(list(Action))


class LearningReason(Reason):
    """Implementation of a learning reason lobe."""

    def __init__(self, genome: "Dict[Gene, float]") -> "None":
        super().__init__(genome)
        self.first_frame = True
        self.model = create_reason_model()
        self.target_model = create_reason_model()
        self.optimizer = Adam(self.genome[Gene.REASON_LEARNING_RATE])
        self.epsilon = self.genome[Gene.REASON_STARTING_EPSILON]
        self.elapsed_time: "float" = 0
        self.elapsed_time_target: "float" = 0
        self.state_hist: "List[NDArray[floating]]" = []
        self.reward_hist: "List[NDArray[floating]]" = []
        self.next_state_hist: "List[NDArray[floating]]" = []

    def update_and_learn(self, state: "NDArray[floating]",
                         reward: "NDArray[floating]",
                         elapsed_time: "float") -> "None":
        """Performs a single update and learning step.
        
        Positional arguments:  
         - `state`: the input values for the update step.  
         - `reward`: the reward values for the last performed action.  
         - `elapsed_time`: the amount of time since last update step, in \
        seconds."""
        if not self.first_frame:
            self.reward_hist.append(reward)
            self.next_state_hist.append(state)
        else:
            self.first_frame = False

        self.elapsed_time += elapsed_time
        self.elapsed_time_target += elapsed_time

        q_values = self.model(state.reshape(1, len(state)), training=False)
        if self.epsilon > uniform():
            self.action = choice(list(Action))
        else:
            action_idx = keras_argmax(q_values)
            for action in Action:
                if action.value == action_idx:
                    self.action = action
        self.epsilon = max(
            self.genome[Gene.REASON_MIN_EPSILON],
            self.epsilon * self.genome[Gene.REASON_EPSILON_DECAY]
        )

        if self.elapsed_time > self.genome[Gene.REASON_UPDATE_PERIOD] \
                and len(self.reward_hist) > BATCH_SIZE:
            self.elapsed_time = 0
            indices = np_choice(range(len(self.reward_hist)), BATCH_SIZE)

            state_sample = array([self.state_hist[i] for i in indices])
            reward_sample = array([self.reward_hist[i] for i in indices])
            next_state_sample = array([self.next_state_hist[i] for i in indices])

            next_reward_predictions = self.target_model.predict(next_state_sample)

            updated_q_values = reward_sample + (
                self.genome[Gene.REASON_GAMMA]
                * next_reward_predictions
            )

            with GradientTape() as tape:
                preds = self.model(state_sample)
                loss_values = loss(updated_q_values, preds)
            grads = tape.gradient(loss_values, self.model.trainable_variables)
            self.optimizer.apply_gradients(zip(
                grads,
                self.model.trainable_variables
            ))

        if self.elapsed_time_target > self.genome[Gene.REASON_TARGET_UPDATE_PERIOD]:
            self.elapsed_time_target = 0
            self.target_model.set_weights(self.model.get_weights())

        if len(self.reward_hist) > REPLAY_BUFFER_SIZE:
            self.state_hist.clear()
            self.reward_hist.clear()
            self.next_state_hist.clear()
            self.first_frame = True

        self.state_hist.append(state)
