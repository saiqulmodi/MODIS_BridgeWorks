"""Confetti and other little celebrations."""
import random

import pygame

COLOURS = [(255, 196, 64), (90, 210, 240), (70, 210, 110), (235, 90, 160), (255, 255, 255)]


class Confetti:
    def __init__(self):
        self.parts = []

    def burst(self, x, y, n=140):
        for _ in range(n):
            self.parts.append([x, y, random.uniform(-260, 260), random.uniform(-520, -120),
                               random.choice(COLOURS), random.uniform(1.6, 3.2)])

    def update(self, dt):
        for p in self.parts:
            p[0] += p[2] * dt
            p[1] += p[3] * dt
            p[3] += 600 * dt
            p[2] *= 0.99
            p[5] -= dt
        self.parts = [p for p in self.parts if p[5] > 0]

    def draw(self, surface):
        for x, y, _, _, c, life in self.parts:
            pygame.draw.rect(surface, c, (int(x), int(y), 6, 4))

    @property
    def active(self):
        return bool(self.parts)
