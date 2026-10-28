"""
MODIS BridgeWorks - Infrastructure Engineering Sandbox
Desktop: python main.py
Browser: built with pygbag and served from docs/
"""
import asyncio
import sys
import numpy  # noqa: F401
import pygame

from game.app import App

async def main():
    try:
        await App().run()
    except (asyncio.CancelledError, KeyboardInterrupt):
        pass

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        pass
    finally:
        pygame.quit()
        sys.exit(0)
