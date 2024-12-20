import pygame
import random
import math
import sys

# Initialize Pygame
pygame.init()

# Set up the screen with transparency and no frame
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA | pygame.NOFRAME)
pygame.display.set_caption("Pulsing Circular Particle Effect")

# Particle colour
PARTICLE_COLOR = (42, 32, 135)  # Deep purple-blue particles (RGBA without alpha)

# Particle properties
NUM_PARTICLES = 100  # Number of particles
particles = []

# Center of the circle
CENTER_X = SCREEN_WIDTH // 2
CENTER_Y = SCREEN_HEIGHT // 2
BASE_RADIUS = 200  # Base radius of the circle
PULSE_SPEED = 0.01  # Speed of the pulsing effect
pulse_offset = 0  # Tracks the current pulse offset

# Function to create particles in a circular formation
def create_particles():
    for _ in range(NUM_PARTICLES):
        angle = random.uniform(0, 2 * math.pi)  # Random angle around the circle
        distance = BASE_RADIUS + random.uniform(-10, 10)  # Slight variation in radius
        size = random.randint(5, 8)  # Particle size for better resolution
        speed = random.uniform(-0.01, 0.01)  # Very slow movement
        particles.append([angle, distance, size, speed])

# Function to create a smoother particle (anti-aliased)
def draw_smooth_particle(surface, color, pos, size):
    # Create a temporary surface with alpha (transparency) for smooth edges
    particle_surface = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
    pygame.draw.circle(particle_surface, color + (255,), (size, size), size)
    # Blit the smooth particle onto the main screen
    surface.blit(particle_surface, (pos[0] - size, pos[1] - size), special_flags=pygame.BLEND_RGBA_ADD)

# Function to update and draw particles
def update_and_draw_particles():
    global pulse_offset
    pulse_offset += PULSE_SPEED

    # Calculate the current pulsing radius
    pulse_radius = BASE_RADIUS + 20 * math.sin(pulse_offset)

    # Redraw the particles
    for particle in particles:
        # Slightly adjust particle's angle for smooth movement
        particle[0] += particle[3]

        # Calculate particle's position based on pulsing radius
        x = CENTER_X + (pulse_radius + random.uniform(-5, 5)) * math.cos(particle[0])
        y = CENTER_Y + (pulse_radius + random.uniform(-5, 5)) * math.sin(particle[0])

        # Draw the smooth particle
        draw_smooth_particle(screen, PARTICLE_COLOR, (int(x), int(y)), particle[2])

    # Clear the surface by drawing a transparent rectangle (erases old frames without a visible background)
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 10))  # Slight opacity to "fade" previous particles
    screen.blit(overlay, (0, 0))

# Main loop
def main():
    clock = pygame.time.Clock()
    create_particles()

    while True:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Update and draw particles
        update_and_draw_particles()

        # Refresh the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)

# Run the program
if __name__ == "__main__":
    main()
