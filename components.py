import pygame
import config
import random # <--- IMPORTANTE: Necesario para las chispas

# Inicializamos el módulo de fuentes
pygame.font.init() 

# Fuente por defecto
DEFAULT_FONT = pygame.font.SysFont('serif', 20, bold=True)

def lerp(start, end, amount):
    """Interpolación lineal para animaciones suaves."""
    return start + (end - start) * amount

class Button:
    """Botón con estados de Hover y Click."""
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
        self.hovered = False

    def draw(self):
        mouse_pos = pygame.mouse.get_pos()
        self.hovered = self.rect.collidepoint(mouse_pos)
        
        current_border = config.WHITE if self.hovered else self.border_color
        
        pygame.draw.rect(self.surface, self.color, self.rect)
        width = 3 if self.hovered else 1
        pygame.draw.rect(self.surface, current_border, self.rect, width)

        if self.text:
            text_surf = self.font.render(self.text, True, self.text_color)
            text_rect = text_surf.get_rect(center=self.rect.center)
            self.surface.blit(text_surf, text_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False

class ProgressBar:
    """Barra de progreso con animación."""
    def __init__(self, surface, x, y, w, h, max_value):
        self.surface = surface
        self.rect = pygame.Rect(x, y, w, h)
        self.max_value = max_value
        self.target_value = 0  
        self.current_value = 0 
        self.bg_color = config.BAR_EMPTY
        self.fill_color = config.BAR_FULL

    def set_value(self, value):
        self.target_value = max(0, min(value, self.max_value))

    def update(self):
        self.current_value = lerp(self.current_value, self.target_value, 0.1)

    def draw(self):
        pygame.draw.rect(self.surface, self.bg_color, self.rect)
        fill_width = (self.current_value / self.max_value) * self.rect.width
        if fill_width > 0:
            fill_rect = pygame.Rect(self.rect.x, self.rect.y, fill_width, self.rect.height)
            pygame.draw.rect(self.surface, self.fill_color, fill_rect)
        pygame.draw.rect(self.surface, config.GOLD, self.rect, 2)

class Spark:
    """Una partícula simple que sale disparada y desaparece."""
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        # Velocidad aleatoria
        self.vx = random.uniform(-3, 3)
        self.vy = random.uniform(-5, -1) 
        self.radius = random.randint(2, 4)
        self.life = 255 # Vida inicial

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.2 # Gravedad
        self.life -= 10 # Desvanecimiento

    def draw(self, surface):
        if self.life > 0:
            s = pygame.Surface((self.radius*2, self.radius*2), pygame.SRCALPHA)
            final_color = (*self.color, max(0, int(self.life)))
            pygame.draw.circle(s, final_color, (self.radius, self.radius), self.radius)
            surface.blit(s, (int(self.x), int(self.y)))

    def is_alive(self):
        return self.life > 0
        
class ScreenFlash:
    """Un destello blanco que cubre toda la pantalla y se desvanece."""
    def __init__(self, width, height):
        self.image = pygame.Surface((width, height))
        self.image.fill(config.WHITE)
        self.alpha = 0 # Empieza invisible

    def trigger(self):
        self.alpha = 255 # Se vuelve totalmente opaco (blanco brillante)

    def update(self):
        if self.alpha > 0:
            self.alpha -= 10 # Se desvanece rápidamente
            if self.alpha < 0: self.alpha = 0

    def draw(self, surface):
        if self.alpha > 0:
            self.image.set_alpha(self.alpha)
            surface.blit(self.image, (0, 0))