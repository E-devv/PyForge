import pygame
import config

# Font for the button text
DEFAULT_FONT = pygame.font.SysFont('serif', 24)

class Button:
    """A clickable button with a border."""

    def __init__(self, surface, x, y, w, h, text='',
                 color=config.PANEL_COLOR,
                 border_color=config.GOLD,
                 text_color=config.WHITE):
        self.surface = surface
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color
        self.border_color = border_color
        self.text_color = text_color
        self.font = DEFAULT_FONT

    def draw(self):
        """Draws the button on the screen."""
        # Draw the button background
        pygame.draw.rect(self.surface, self.color, self.rect)
        # Draw the border
        pygame.draw.rect(self.surface, self.border_color, self.rect, 2)

        # Draw the text in the center of the button
        if self.text:
            text_surf = self.font.render(self.text, True, self.text_color)
            text_rect = text_surf.get_rect(center=self.rect.center)
            self.surface.blit(text_surf, text_rect)

    def is_clicked(self, event):
        """Checks if the button was clicked."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False

class ProgressBar:
    """A progress bar that can be updated."""

    def __init__(self, surface, x, y, w, h, max_value):
        self.surface = surface
        self.rect = pygame.Rect(x, y, w, h)
        self.max_value = max_value
        self.current_value = 0
        self.bg_color = config.BAR_EMPTY
        self.fill_color = config.BAR_FULL

    def update(self, current_value):
        """Updates the current value of the progress bar."""
        self.current_value = max(0, min(current_value, self.max_value))

    def draw(self):
        """Draws the progress bar on the screen."""
        # Draw the background
        pygame.draw.rect(self.surface, self.bg_color, self.rect)

        # Calculate the width of the fill
        fill_width = (self.current_value / self.max_value) * self.rect.width
        fill_rect = pygame.Rect(self.rect.x, self.rect.y,
                                fill_width, self.rect.height)

        # Draw the fill
        pygame.draw.rect(self.surface, self.fill_color, fill_rect)
