import pygame
import config

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
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Drawing
        screen.fill(config.BG_COLOR)

        # Update the display
        pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    main()
