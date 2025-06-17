import pygame
from typing import Callable, Tuple, Optional


class Button:
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
        """Draw the button on the screen"""
        mouse_pos = pygame.mouse.get_pos()
        is_hovering = self.rect.collidepoint(mouse_pos)

        # Draw button rectangle
        color = self.hover_color if is_hovering else self.color
        pygame.draw.rect(screen, color, self.rect)

        # Draw button text
        text_surface = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_event(self, event: pygame.event) -> bool:
        """Handle mouse click events and execute the command"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                if self.command:
                    self.command()
                return True
        return False

    def set_command(self, new_command: Callable) -> None:
        """Change the button's command to a new function"""
        self.command = new_command