import pygame
import random
import math
import threading
import sys
import os

# Initialize Pygame
pygame.init()

# Set up the screen with transparency and no frame
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA | pygame.NOFRAME)
pygame.display.set_caption("Pulsing Circular Particle Effect")

# Particle colour
PARTICLE_COLOR = (42, 32, 135)

# Particle properties
NUM_PARTICLES = 100
particles = []

# Center of the circle
CENTER_X = SCREEN_WIDTH // 2
CENTER_Y = SCREEN_HEIGHT // 2
BASE_RADIUS = 200
PULSE_SPEED = 0.01
pulse_offset = 0

# Graphic state
graphic_active = False

# Function to set the window always on top using wmctrl
def set_window_always_on_top():
    # Get the window ID from Pygame
    window_id = pygame.display.get_wm_info()['window']
    # Use wmctrl to set the window to always be on top
    os.system(f'wmctrl -i -r {window_id} -b add,above')

def create_particles():
    for _ in range(NUM_PARTICLES):
        angle = random.uniform(0, 2 * math.pi)
        distance = BASE_RADIUS + random.uniform(-10, 10)
        size = random.randint(5, 8)
        speed = random.uniform(-0.01, 0.01)
        particles.append([angle, distance, size, speed])

def draw_smooth_particle(surface, color, pos, size):
    particle_surface = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
    pygame.draw.circle(particle_surface, color + (255,), (size, size), size)
    surface.blit(particle_surface, (pos[0] - size, pos[1] - size), special_flags=pygame.BLEND_RGBA_ADD)

def update_and_draw_particles():
    global pulse_offset
    pulse_offset += PULSE_SPEED
    pulse_radius = BASE_RADIUS + 20 * math.sin(pulse_offset)

    for particle in particles:
        particle[0] += particle[3]
        x = CENTER_X + (pulse_radius + random.uniform(-5, 5)) * math.cos(particle[0])
        y = CENTER_Y + (pulse_radius + random.uniform(-5, 5)) * math.sin(particle[0])
        draw_smooth_particle(screen, PARTICLE_COLOR, (int(x), int(y)), particle[2])

    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 10))
    screen.blit(overlay, (0, 0))

def dynamic_graphic():
    global graphic_active
    create_particles()
    clock = pygame.time.Clock()

    # Set the window always on top as soon as it starts
    set_window_always_on_top()

    while graphic_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        update_and_draw_particles()
        pygame.display.flip()
        clock.tick(60)
    else:
        screen.fill((0, 0, 0))  # Black screen, or use (0, 0, 0, 0) for transparency
        pygame.display.flip()

def start_graphic():
    global graphic_active
    if not graphic_active:
        graphic_active = True
        threading.Thread(target=dynamic_graphic, daemon=True).start()

def stop_graphic():
    global graphic_active
    graphic_active = False
