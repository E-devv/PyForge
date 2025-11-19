import pygame
import config
from components import Button, ProgressBar

# Initialize Pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
pygame.display.set_caption("The Forge")

# Default font
DEFAULT_FONT = pygame.font.SysFont('serif', 24)

def main():
    """Main game loop."""
    running = True
    iron_ingots = 0

    # UI Elements
    add_button = Button(screen, 50, 50, 220, 50, 'Añadir Hierro (+)')
    remove_button = Button(screen, 280, 50, 220, 50, 'Quitar Hierro (-)')
    quality_bar = ProgressBar(screen, 50, 120, 450, 40, 100)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if add_button.is_clicked(event):
                iron_ingots = min(100, iron_ingots + 1)
            if remove_button.is_clicked(event):
                iron_ingots = max(0, iron_ingots - 1)

        quality_bar.update(iron_ingots)

        # Drawing
        screen.fill(config.BG_COLOR)
        add_button.draw()
        remove_button.draw()
        quality_bar.draw()

        # Draw the iron ingots count
        ingot_text = DEFAULT_FONT.render(f'Lingotes de Hierro: {iron_ingots}', True, config.WHITE)
        screen.blit(ingot_text, (50, 180))

        # Update the display
        pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    main()
