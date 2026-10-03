"""Procedurally generated sound effects (no copyrighted audio files).

Sounds play only when something happens: a beam starts creaking past 80% load, a beam
snaps, a design beats its budget target, or a button is pressed.
"""
import math

import numpy as np
import pygame

RATE = 22050
_sounds = {}
_ok = False


def _to_sound(wave, volume=0.5):
    wave = np.clip(wave * volume, -1, 1)
    data = (wave * 32767).astype(np.int16)
    stereo = np.column_stack([data, data])
    return pygame.sndarray.make_sound(stereo.copy(order="C"))


def _env(n, attack=0.01, release=0.2):
    t = np.arange(n) / RATE
    a = np.clip(t / attack, 0, 1)
    r = np.clip((t[-1] - t) / release, 0, 1)
    return a * r


def init():
    global _ok
    try:
        if not pygame.mixer.get_init():
            pygame.mixer.init(frequency=RATE, size=-16, channels=2)
        rng = np.random.default_rng(3)
        t = np.arange(int(RATE * 0.9)) / RATE
        # Wood creak: slowly modulated scratchy noise
        noise = rng.standard_normal(len(t))
        creak = np.sin(2 * math.pi * (90 + 40 * np.sin(2 * math.pi * 3 * t)) * t)
        creak = creak * (0.5 + 0.5 * np.sign(np.sin(2 * math.pi * 23 * t))) + 0.15 * noise
        _sounds["creak"] = _to_sound(creak * _env(len(t), 0.05, 0.4), 0.35)
        # Steel groan: low sliding tone
        f = 55 + 25 * t
        groan = np.sin(2 * math.pi * np.cumsum(f) / RATE) + 0.3 * np.sin(2 * math.pi * np.cumsum(2.01 * f) / RATE)
        _sounds["groan"] = _to_sound(groan * _env(len(t), 0.08, 0.5), 0.4)
        # Snap: sharp noise burst
        ts = np.arange(int(RATE * 0.35)) / RATE
        snap = rng.standard_normal(len(ts)) * np.exp(-ts * 18)
        _sounds["snap"] = _to_sound(snap, 0.6)
        # Ka-ching: two bright bells
        tk = np.arange(int(RATE * 0.8)) / RATE
        bell = lambda f0, d: np.sin(2 * math.pi * f0 * (tk - d)) * np.exp(-np.clip(tk - d, 0, None) * 6) * (tk >= d)
        _sounds["kaching"] = _to_sound(bell(1318, 0) + 0.8 * bell(1760, 0.12) + 0.4 * bell(2637, 0.12), 0.35)
        # Click
        tc = np.arange(int(RATE * 0.04)) / RATE
        _sounds["click"] = _to_sound(np.sin(2 * math.pi * 1200 * tc) * np.exp(-tc * 120), 0.25)
        # Whoosh (wind / train passing)
        tw = np.arange(int(RATE * 0.6)) / RATE
        _sounds["whoosh"] = _to_sound(rng.standard_normal(len(tw)) * np.sin(math.pi * tw / tw[-1]) ** 2, 0.15)
        # Alarm (SPAD / emergency)
        ta = np.arange(int(RATE * 0.5)) / RATE
        _sounds["alarm"] = _to_sound(np.sign(np.sin(2 * math.pi * 660 * ta)) * 0.5 * _env(len(ta), 0.01, 0.1), 0.2)
        _ok = True
    except Exception:
        _ok = False


def play(name):
    if _ok and name in _sounds:
        try:
            _sounds[name].play()
        except Exception:
            pass
