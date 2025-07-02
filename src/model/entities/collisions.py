"""Module containing collision handlers."""
from typing import Self, Tuple

class Hitbox:
    """Implementation for the entity's hitbox."""
    def __init__(self, x: float, y: float, width: float, height: float) -> None:
        """Instantiates an hitbox in the desired position, of the desired dimension.
        
        Arguments:  
        `x`: the starting x coordinate of the hitbox.  
        `y`: the starting y coordinate of the hitbox.  
        `width`: the width of the hitbox.  
        `height`: the height of the hitbox."""
        self.x: float = x
        self.y: float = y
        self.width: float = width
        self.height: float = height

    def is_colliding(self, hitbox: Self) -> bool:
        """Checks whether the hitbox is colliding with another hitbox.
        
        Arguments:  
        `pos`: the position to check.  
        `width`: the width of the hitbox to check.  
        `height`: the height of the hitbox to check."""
        return (
            (self.x + self.width) >= hitbox.x
            and self.x <= (hitbox.x + hitbox.width)
            and (self.y + self.height) <= hitbox.y
            and self.y >= (hitbox.y + hitbox.height)
        )

    def move(self, movement: Tuple[float, float]) -> None:
        """Moves the hitbox of the desired quantity.
        
        Arguments:  
        `movement`: a tuple representing the two movement coordinates."""
        self.x += movement[0]
        self.y += movement[1]
