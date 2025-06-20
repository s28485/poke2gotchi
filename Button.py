"""
A module used for a custom button class
"""

from typing import Callable, Tuple, Optional
import pygame


class Button:
    """
    A class that represents a custom button
    """
    def __init__(self,
                 x: int,
                 y: int,
                 width: int,
                 height: int,
                 text: str,
                 color: Tuple[int, int, int],
                 hover_color: Tuple[int, int, int],
                 command: Optional[Callable] = None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.command = command
        self.font = pygame.font.SysFont('Arial', 24)

    def draw(self, screen: pygame.Surface) -> None:
        """
        A method used for drawing the button
        :param screen: A screen in which the button is drawn
        :return: None
        """
        mouse_pos = pygame.mouse.get_pos()
        is_hovering = self.rect.collidepoint(mouse_pos)

        # Draw button rectangle
        color = self.hover_color if is_hovering else self.color
        pygame.draw.rect(screen, color, self.rect)

        # Draw button text
        text_surface = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)


    def set_command(self, new_command: Callable) -> None:
        """
        A method used for setting the button command
        :param new_command: A new command to be set
        :return: None
        """
        self.command = new_command

    def is_pressed(self, mouse_pos: tuple[int, int]) -> bool:
        """
        A method for checking if the button is pressed
        :param mouse_pos: Mouse current position described in a tuple of x and y
        :return: True if the button is pressed, False otherwise
        """
        return self.rect.collidepoint(mouse_pos)
