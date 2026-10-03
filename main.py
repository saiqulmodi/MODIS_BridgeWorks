"""MODIS_BridgeWorks - a hard-physics bridge & transport sandbox.

Phase 1: window, background grid, and the first level's terrain
(two cliffs with a river between them).
"""
import math

import pygame

from engine.materials import STEEL
from engine.truss import FAILED, GREEN, RED, YELLOW, Member, Node, TrussSolver

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
STATUS_COLOURS = {GREEN: (60, 200, 90), YELLOW: (240, 200, 40),
                  RED: (230, 60, 50), FAILED: (230, 0, 0)}

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


def world_to_screen(x, y):
    """Physics coordinates (metres, y UP from the cliff top) -> screen pixels."""
    return m2px(x), m2px(CLIFF_TOP_M - y)


def build_demo_bridge(load_kn):
    """A steel Warren truss across the gap, with the deck load on the bottom joints."""
    span = RIGHT_CLIFF_START_M - LEFT_CLIFF_END_M
    panels, height = 4, 3.0
    w = span / panels
    x0 = LEFT_CLIFF_END_M
    nodes = []
    for k in range(panels + 1):                      # bottom joints 0..4
        if k == 0:
            nodes.append(Node.pinned(x0, 0))
        elif k == panels:
            nodes.append(Node.roller(x0 + span, 0))
        else:
            nodes.append(Node(x0 + k * w, 0, fy=-load_kn * 1e3))
    for k in range(panels):                          # top joints 5..8
        nodes.append(Node(x0 + (k + 0.5) * w, height))
    A, I = 0.002, 2e-6
    members = []
    for k in range(panels):
        top = panels + 1 + k
        members += [Member(k, k + 1, STEEL, A, I),
                    Member(k, top, STEEL, A, I),
                    Member(top, k + 1, STEEL, A, I)]
        if k < panels - 1:
            members.append(Member(top, top + 1, STEEL, A, I))
    return nodes, members


def point_segment_distance(p, a, b):
    ax, ay = a
    bx, by = b
    px, py = p
    dx, dy = bx - ax, by - ay
    seg2 = dx * dx + dy * dy
    t = 0 if seg2 == 0 else max(0, min(1, ((px - ax) * dx + (py - ay) * dy) / seg2))
    return math.hypot(px - (ax + t * dx), py - (ay + t * dy))


def draw_truss(screen, nodes, members, result, tick):
    hovered = None
    mouse = pygame.mouse.get_pos()
    for k, (m, r) in enumerate(zip(members, result.members)):
        a = world_to_screen(nodes[m.i].x, nodes[m.i].y)
        b = world_to_screen(nodes[m.j].x, nodes[m.j].y)
        colour = STATUS_COLOURS[r.status]
        if r.status == FAILED and (tick // 8) % 2:   # flashing red
            colour = (255, 255, 255)
        width = 7 if point_segment_distance(mouse, a, b) < 7 else 5
        if width == 7:
            hovered = k
        pygame.draw.line(screen, colour, a, b, width)
    for nd in nodes:
        pos = world_to_screen(nd.x, nd.y)
        pygame.draw.circle(screen, (40, 40, 50), pos, 6)
        if nd.fix_y:
            pygame.draw.polygon(screen, (60, 60, 70),
                                [pos, (pos[0] - 9, pos[1] + 14), (pos[0] + 9, pos[1] + 14)])
    return hovered


def draw_hud(screen, font, load_kn, result, hovered):
    gap_m = RIGHT_CLIFF_START_M - LEFT_CLIFF_END_M
    worst = max(result.members, key=lambda r: r.ratio)
    lines = [
        "Level 1 - Small River Crossing   (engine demo: steel Warren truss)",
        f"Gap: {gap_m} m   |   Load on each deck joint: {load_kn:.0f} kN   (UP / DOWN to change)",
        f"Most stressed member: {worst.ratio * 100:.0f}% of its limit",
        "Hover a beam to see its maths.   Green <50%  Yellow 50-80%  Red 80-100%  Flashing = failed",
        "ESC to quit",
    ]
    for i, line in enumerate(lines):
        screen.blit(font.render(line, True, TEXT), (16, 12 + i * 24))
    if hovered is not None:
        r = result.members[hovered]
        kind = "TENSION (pulled)" if r.N > 0 else "COMPRESSION (pushed)" if r.N < 0 else "no load"
        info = [f"Beam {hovered}:  N = {r.N / 1e3:+.1f} kN  {kind}   load {r.ratio * 100:.0f}%",
                r.explanation]
        for i, line in enumerate(info):
            screen.blit(font.render(line, True, (255, 255, 255)), (16, HEIGHT - 60 + i * 24))


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("segoeui", 20)

    sky = make_sky()
    grid = make_grid()
    load_kn = 20.0
    nodes, members = build_demo_bridge(load_kn)
    result = TrussSolver(nodes, members).solve()
    tick = 0
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key in (pygame.K_UP, pygame.K_DOWN):
                    step = 10 if event.key == pygame.K_UP else -10
                    load_kn = max(0.0, load_kn + step)
                    nodes, members = build_demo_bridge(load_kn)
                    result = TrussSolver(nodes, members).solve()

        screen.blit(sky, (0, 0))
        screen.blit(grid, (0, 0))
        draw_terrain(screen, tick)
        hovered = draw_truss(screen, nodes, members, result, tick)
        draw_hud(screen, font, load_kn, result, hovered)
        pygame.display.flip()
        clock.tick(FPS)
        tick += 1

    pygame.quit()


if __name__ == "__main__":
    main()
