"""MODIS_BridgeWorks - a hard-physics bridge & transport sandbox.

Phase 1: window, background grid, and the first level's terrain
(two cliffs with a river between them).
"""
import pygame

# --- Window -------------------------------------------------------------
WIDTH, HEIGHT = 1280, 720
FPS = 60
TITLE = "MODIS BridgeWorks"

# --- World scale --------------------------------------------------------
# 1 grid cell = 1 metre. Everything the physics uses later is in metres.
PIXELS_PER_METRE = 32
GRID = PIXELS_PER_METRE

# --- Colours ------------------------------------------------------------
SKY_TOP = (110, 170, 230)
SKY_BOTTOM = (190, 225, 250)
GRID_LINE = (255, 255, 255, 40)
GROUND = (120, 90, 60)
GRASS = (90, 170, 80)
WATER = (40, 110, 190)
WATER_SHINE = (120, 180, 240)
TEXT = (20, 30, 40)

# --- Level 1 terrain (in metres, origin at top-left of the world) -------
LEFT_CLIFF_END_M = 12     # left bank ends 12 m from the left edge
RIGHT_CLIFF_START_M = 28  # right bank starts at 28 m -> a 16 m gap
CLIFF_TOP_M = 12          # ground surface is 12 m down from the top
WATER_LEVEL_M = 18        # river surface


def m2px(metres):
    """Convert metres to screen pixels."""
    return int(metres * PIXELS_PER_METRE)


def make_sky():
    """Pre-draw a vertical gradient sky once, so each frame just blits it."""
    sky = pygame.Surface((WIDTH, HEIGHT))
    for y in range(HEIGHT):
        t = y / HEIGHT
        colour = [int(SKY_TOP[i] + (SKY_BOTTOM[i] - SKY_TOP[i]) * t) for i in range(3)]
        pygame.draw.line(sky, colour, (0, y), (WIDTH, y))
    return sky


def make_grid():
    """Faint 1-metre grid the player will snap joints to in Phase 2."""
    grid = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    for x in range(0, WIDTH, GRID):
        pygame.draw.line(grid, GRID_LINE, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, GRID):
        pygame.draw.line(grid, GRID_LINE, (0, y), (WIDTH, y))
    return grid


def draw_terrain(screen, tick):
    left_end = m2px(LEFT_CLIFF_END_M)
    right_start = m2px(RIGHT_CLIFF_START_M)
    top = m2px(CLIFF_TOP_M)
    water_y = m2px(WATER_LEVEL_M)

    # River, with a gently moving shine line
    pygame.draw.rect(screen, WATER, (left_end, water_y, right_start - left_end, HEIGHT - water_y))
    shine_offset = (tick // 4) % 40
    for x in range(left_end - 40 + shine_offset, right_start, 40):
        x0, x1 = max(x, left_end), min(x + 18, right_start)
        if x1 > x0:
            pygame.draw.line(screen, WATER_SHINE, (x0, water_y + 6), (x1, water_y + 6), 2)

    # Cliffs
    pygame.draw.rect(screen, GROUND, (0, top, left_end, HEIGHT - top))
    pygame.draw.rect(screen, GROUND, (right_start, top, WIDTH - right_start, HEIGHT - top))
    pygame.draw.rect(screen, GRASS, (0, top, left_end, 8))
    pygame.draw.rect(screen, GRASS, (right_start, top, WIDTH - right_start, 8))


def draw_hud(screen, font):
    gap_m = RIGHT_CLIFF_START_M - LEFT_CLIFF_END_M
    lines = [
        "Level 1 - Small River Crossing",
        f"Gap to span: {gap_m} m   |   Grid: 1 square = 1 m",
        "ESC to quit",
    ]
    for i, line in enumerate(lines):
        screen.blit(font.render(line, True, TEXT), (16, 12 + i * 24))


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("segoeui", 20)

    sky = make_sky()
    grid = make_grid()
    tick = 0
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        screen.blit(sky, (0, 0))
        screen.blit(grid, (0, 0))
        draw_terrain(screen, tick)
        draw_hud(screen, font)
        pygame.display.flip()
        clock.tick(FPS)
        tick += 1

    pygame.quit()


if __name__ == "__main__":
    main()
