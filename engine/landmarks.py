"""
Procedural Landmark Renderer.
Renders Mumbai Bandra-Worli Sea Link twin diamond towers, stay-cables, and marine swell.
Uses pure vector math (Zero external texture memory overhead).
"""
import math
import pygame

class BandraWorliSeaLink:
    def __init__(self, surface_width, surface_height):
        self.w = surface_width
        self.h = surface_height
        self.water_level = int(surface_height * 0.78)
        self.pylon_height = int(surface_height * 0.52)
        self.pylon_x = surface_width // 2
        self.pylon_top_y = self.water_level - self.pylon_height

    def render_sea(self, surface, tick):
        sea_color = (25, 48, 82)
        wave_color = (40, 80, 130)
        pts = [(0, self.h)]
        for x in range(0, self.w + 10, 15):
            y = self.water_level + math.sin(x * 0.025 + tick * 0.06) * 5
            pts.append((x, int(y)))
        pts.append((self.w, self.h))
        pygame.draw.polygon(surface, sea_color, pts)

    def render_diamond_pylon(self, surface):
        cx = self.pylon_x
        top = (cx, self.pylon_top_y)
        mid_left = (cx - 50, self.water_level - self.pylon_height // 2)
        mid_right = (cx + 50, self.water_level - self.pylon_height // 2)
        deck_cross = (cx, self.water_level - 55)
        base_left = (cx - 35, self.water_level + 20)
        base_right = (cx + 35, self.water_level + 20)

        concrete_tone = (210, 215, 220)
        shadow_tone = (150, 155, 165)

        # Upper diamond apex
        pygame.draw.polygon(surface, concrete_tone, [top, mid_left, deck_cross, mid_right])
        pygame.draw.polygon(surface, shadow_tone, [top, mid_right, deck_cross], 2)

        # Lower foundation legs
        pygame.draw.polygon(surface, concrete_tone, [mid_left, deck_cross, base_left])
        pygame.draw.polygon(surface, shadow_tone, [mid_right, deck_cross, base_right])

    def render_stay_cables(self, surface, deck_nodes):
        top_anchor = (self.pylon_x, self.pylon_top_y + 12)
        cable_color = (240, 240, 245)
        for node in deck_nodes:
            dx = abs(node[0] - self.pylon_x)
            if 25 < dx < 360:
                pygame.draw.line(surface, cable_color, top_anchor, (int(node[0]), int(node[1])), 1)
