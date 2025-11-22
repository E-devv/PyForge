import pygame
import os
import config
from components import Button, ProgressBar, Spark, ScreenFlash

pygame.init()
# Inicializar el mezclador de sonido
pygame.mixer.init()

screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
pygame.display.set_caption("The Forge - Prototipo")

# Fuentes
TITLE_FONT = pygame.font.SysFont('serif', 40, bold=True)
INFO_FONT = pygame.font.SysFont('serif', 18)
SUCCESS_FONT = pygame.font.SysFont('serif', 60, bold=True)

def load_and_scale_image(filename, max_size):
    path = os.path.join('assets', filename)
    try:
        image = pygame.image.load(path)
        width, height = image.get_size()
        scale_factor = min(max_size[0]/width, max_size[1]/height)
        new_size = (int(width * scale_factor), int(height * scale_factor))
        return pygame.transform.smoothscale(image, new_size)
    except FileNotFoundError:
        return None

# Función para cargar sonidos de forma segura
def load_sound(filename):
    path = os.path.join('assets', filename)
    try:
        return pygame.mixer.Sound(path)
    except FileNotFoundError:
        print(f"Advertencia: No se encontró el sonido {filename}")
        return None

def main():
    running = True
    clock = pygame.time.Clock()
    
    # --- CARGAR ASSETS ---
    preview_size = (200, 200)
    sword_img = load_and_scale_image('sword.png', preview_size)
    shield_img = load_and_scale_image('shield.png', preview_size)
    
    # Cargar Sonidos
    hammer_sfx = load_sound('hammer.wav')
    success_sfx = load_sound('success.wav')
    
    # Bajar un poco el volumen (opcional, 0.5 es 50%)
    if hammer_sfx: hammer_sfx.set_volume(0.4)
    if success_sfx: success_sfx.set_volume(0.6)

    # Estado
    iron_ingots = 0
    max_capacity = 50
    current_item_img = sword_img
    current_name = "Espada de Hierro"
    
    # Efectos
    sparks = []
    flash = ScreenFlash(config.SCREEN_WIDTH, config.SCREEN_HEIGHT)
    item_completed = False 
    completion_timer = 0   

    # UI
    btn_select_sword = Button(screen, 150, 70, 120, 30, 'Espada')
    btn_select_shield = Button(screen, 280, 70, 120, 30, 'Escudo')
    
    btn_y = 500
    add_button = Button(screen, 250, btn_y, 50, 50, '+')
    remove_button = Button(screen, 180, btn_y, 50, 50, '-')
    quality_bar = ProgressBar(screen, 180, 450, 440, 30, max_capacity)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if not item_completed:
                if add_button.is_clicked(event):
                    iron_ingots += 5
                    
                    # REPRODUCIR SONIDO MARTILLO
                    if hammer_sfx: hammer_sfx.play()

                    # Chispas
                    for _ in range(15):
                        color = (255, 200, 0) if _ % 2 == 0 else (255, 100, 0)
                        s = Spark(add_button.rect.centerx, add_button.rect.centery, color)
                        sparks.append(s)

                if remove_button.is_clicked(event):
                    iron_ingots -= 5

                if btn_select_sword.is_clicked(event):
                    current_item_img = sword_img
                    current_name = "Espada de Hierro"
                    iron_ingots = 0 
                if btn_select_shield.is_clicked(event):
                    current_item_img = shield_img
                    current_name = "Escudo de Roble"
                    iron_ingots = 0 

        # Lógica
        iron_ingots = max(0, min(iron_ingots, max_capacity))
        quality_bar.set_value(iron_ingots)
        quality_bar.update()
        flash.update()

        # --- DETECTAR VICTORIA ---
        if iron_ingots >= max_capacity and not item_completed:
            item_completed = True
            
            # REPRODUCIR SONIDO VICTORIA
            if success_sfx: success_sfx.play()
            
            flash.trigger()
            completion_timer = 120

        if item_completed:
            completion_timer -= 1
            if completion_timer <= 0:
                item_completed = False
                iron_ingots = 0
                sparks = []

        # --- DIBUJAR ---
        screen.fill(config.BG_COLOR)

        title_surf = TITLE_FONT.render("La Gran Forja", True, config.GOLD)
        title_rect = title_surf.get_rect(center=(config.SCREEN_WIDTH // 2, 40))
        screen.blit(title_surf, title_rect)

        work_area = pygame.Rect(150, 110, 500, 300)
        border_color = config.BAR_FULL if item_completed else config.PANEL_COLOR
        pygame.draw.rect(screen, (30, 30, 35), work_area, border_radius=10)
        pygame.draw.rect(screen, border_color, work_area, 3, border_radius=10)
        
        if current_item_img:
            img_rect = current_item_img.get_rect(center=work_area.center)
            screen.blit(current_item_img, img_rect)
            
            if item_completed:
                success_text = SUCCESS_FONT.render("¡FORJADO!", True, config.GOLD)
                shadow_text = SUCCESS_FONT.render("¡FORJADO!", True, (0,0,0))
                success_rect = success_text.get_rect(center=work_area.center)
                shadow_rect = shadow_text.get_rect(center=(work_area.centerx + 3, work_area.centery + 3))
                screen.blit(shadow_text, shadow_rect)
                screen.blit(success_text, success_rect)
            else:
                name_surf = INFO_FONT.render(current_name, True, (150, 150, 150))
                name_rect = name_surf.get_rect(center=(work_area.centerx, work_area.bottom - 30))
                screen.blit(name_surf, name_rect)

        resource_text = INFO_FONT.render(f"Recursos: {iron_ingots} / {max_capacity}", True, config.WHITE)
        screen.blit(resource_text, (180, 420))

        add_button.draw()
        remove_button.draw()
        btn_select_sword.draw()
        btn_select_shield.draw()
        quality_bar.draw()

        for spark in sparks[:]:
            spark.update()
            spark.draw(screen)
            if not spark.is_alive():
                sparks.remove(spark)
        
        flash.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == '__main__':
    main()