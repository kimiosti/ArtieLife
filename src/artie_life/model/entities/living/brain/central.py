"""Module containing the brain implementation."""
from typing import TYPE_CHECKING
from utils.living.learning.commons import USER_INTERACTION_PERIOD, \
    POSITIVE_NEEDS_REWARD, NEGATIVE_NEEDS_REWARD
from utils.living.learning.attention import compute_reward as compute_attention_reward, \
    assemble_state as assemble_attention_state
from utils.living.learning.reason import compute_reward as compute_reason_reward, \
    assemble_state as assemble_reason_state
from model.entities.living.needs import NeedsTracker, PerceptionTracker
from model.entities.living.brain.attention import Attention, LearningAttention
from model.entities.living.brain.reason import Reason, LearningReason
from controller.log import log_genome

if TYPE_CHECKING:
    from typing import Dict
    from pygame.rect import Rect
    from controller.world.world_controllers import DistanceController
    from utils.living.genome import Gene
    from utils.living.actions import InteractionType
    from utils.living.actions import Need

def compute_needs_reward(last_needs: "Dict[Need, float]",
                         cur_needs: "Dict[Need, float]") -> "float":
    """Computes the auto-determined reward component related to needs' decay or
    restoration.
    
    Positional arguments:  
     - `last_needs`: the last previously recorded value for each need.
     - `cur_needs`: the current value for each need.
    
    Return:  
    The computed reward value."""
    for need, value in cur_needs.items():
        if value <= last_needs[need] and value < need.get_threshold():
            return POSITIVE_NEEDS_REWARD
    return NEGATIVE_NEEDS_REWARD

class Brain:
    """Implementation for the living being's central brain lobe. Its function is to
    coordinate the behavior of the `Attention` and `Reason` lobes."""

    # pylint: disable=too-many-instance-attributes
    # Warning disabled since all attributes are needed, and are used to avoid
    # larger issues in the single learning lobes.

    def __init__(self, distance_controller: "DistanceController", living_id: "int",
                 genome: "Dict[Gene, float]", learning_enable: "bool") -> "None":
        """Instantiates the living being's central lobe.
        
        Positional arguments:  
         - `distance_controller`: the `DistanceController` tracking the living being's \
        perception of the world's space.
         - `living_id`: the living being's in-game ID.
         - `genome`: the living being's genome.
         - `learning_enable`: a `bool` representing if the living being should learn \
        or act randomly."""
        log_genome(living_id, genome)
        self.perception_tracker = PerceptionTracker(distance_controller)
        self.needs_tracker = NeedsTracker(genome)
        self.attention: "Attention" = \
            LearningAttention(genome) if learning_enable else Attention(genome)
        self.reason: "Reason" = \
            LearningReason(genome) if learning_enable else Reason(genome)
        self.user_reward: "float" = 0.0
        self.user_input: "str" = ""
        self.user_interaction_length: "float" = 0.0
        self.first_frame = True

    def update(self, elapsed_time: "float", hitbox: "Rect") -> "bool":
        """Updates the brain, decaying vital parameters.

        Positional arguments:  
         - `elapsed_time`: the amount of time since last brain update, in seconds.
         - `hitbox`: the current position of the living being.

        Return:  
        `True` if the living being is still alive after the update, `False` otherwise."""
        if self.first_frame:
            self.attention.update()
            self.reason.update()
            self.first_frame = False
            self.perception_tracker.record(hitbox)
            return self.needs_tracker.decay(elapsed_time)

        self.user_interaction_length += elapsed_time
        if self.user_interaction_length > USER_INTERACTION_PERIOD:
            self.user_input = ""
            self.user_reward = 0.0
            self.user_interaction_length = 0.0

        last_perception = self.perception_tracker.perception
        last_needs = self.needs_tracker.needs

        self.perception_tracker.record(hitbox)
        is_alive = self.needs_tracker.decay(elapsed_time)

        needs_reward = compute_needs_reward(
            last_needs,
            self.needs_tracker.needs
        )

        if not is_alive:
            return is_alive

        if isinstance(self.attention, LearningAttention) \
                and isinstance(self.reason, LearningReason):
            last_focus = self.attention.focus
            self.attention.update_and_learn(
                assemble_attention_state(
                    self.user_input,
                    self.perception_tracker.perception,
                    self.needs_tracker.needs
                ),
                compute_attention_reward(
                    self.user_reward,
                    needs_reward,
                    last_perception,
                    self.perception_tracker.perception
                ),
                elapsed_time
            )
            self.reason.update_and_learn(
                assemble_reason_state(
                    self.attention.focus,
                    self.perception_tracker.perception
                ),
                compute_reason_reward(
                    self.user_reward,
                    needs_reward,
                    last_perception,
                    last_focus
                ),
                elapsed_time
            )
        else:
            self.attention.update()
            self.reason.update()

        return is_alive

    def actuate(self, interaction: "InteractionType") -> "None":
        """Actuates the effect of a given interaction on the living being's needs.
        
        Positional arguments:  
         - `interaction`: the type of the interaction to be made effective."""
        self.needs_tracker.actuate(interaction.get_corresponding_need())

    def apply_user_reward(self, reward: "float") -> "None":
        """Applies the desired user-defined reward to the living being.
        
        Positional arguments:  
         - `reward`: the value of the user-defined reward to be applied to the \
        living being."""
        self.user_reward = reward

    def record_input(self, input_text: "str") -> "None":
        """Records the desired user input.
        
        Positional arguments:  
         - `input_text`: the user-defined input string."""
        self.user_input = input_text
