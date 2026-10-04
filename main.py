"""MODIS BridgeWorks - a hard-physics infrastructure sandbox.

Desktop:  venv\\Scripts\\python.exe main.py
Browser:  built with pygbag (see README) and served from docs/ on GitHub Pages.
"""
import asyncio

import numpy  # noqa: F401  (imported here so pygbag bundles it for the browser)
import pygame  # noqa: F401

from game.app import App


async def main():
    await App().run()


if __name__ == "__main__":
    asyncio.run(main())
