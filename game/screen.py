"""Window / full-screen handling for desktop and browser.

Desktop: the 1280x720 game is drawn into a SCALED window, so it can be resized, maximised
or made full screen (F11) and stays sharp with black bars where the shape differs.
Browser (pygbag): the canvas is stretched to fill the browser window, and a small
"Full screen" button on the page switches the browser to real full screen (a browser only
allows that from a real click, so the button lives in the page itself).
"""
import sys

import pygame

from .ui import HEIGHT, WIDTH

WEB = sys.platform == "emscripten"
_last_fit = None


def create_window(headless=False):
    if WEB or headless:
        return pygame.display.set_mode((WIDTH, HEIGHT))
    try:
        return pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED | pygame.RESIZABLE)
    except pygame.error:
        return pygame.display.set_mode((WIDTH, HEIGHT))


def toggle_fullscreen():
    if WEB:
        try:
            import platform
            doc = platform.window.document
            if doc.fullscreenElement:
                doc.exitFullscreen()
            else:
                doc.documentElement.requestFullscreen()
        except Exception:
            pass
        return
    try:
        pygame.display.toggle_fullscreen()
    except pygame.error:
        pass


def is_fullscreen():
    if WEB:
        try:
            import platform
            return bool(platform.window.document.fullscreenElement)
        except Exception:
            return False
    try:
        return pygame.display.is_fullscreen()
    except (AttributeError, pygame.error):
        return False


# ASCII only, with \u escapes: non-ASCII text gets garbled on its way into the page.
_BUTTON_JS = r"""
(function () {
  if (document.getElementById('bw-fullscreen')) return;
  var b = document.createElement('button');
  b.id = 'bw-fullscreen';
  b.textContent = '\u26F6';
  b.title = 'Full screen / \u09AA\u09C2\u09B0\u09CD\u09A3 \u09AA\u09B0\u09CD\u09A6\u09BE';
  b.style.cssText = 'position:fixed;right:10px;bottom:10px;z-index:9999;width:44px;height:44px;' +
    'font-size:24px;border-radius:8px;border:1px solid #4670a5;background:#16304f;color:#e6eefa;' +
    'cursor:pointer;opacity:0.85';
  b.onclick = function () {
    if (document.fullscreenElement) { document.exitFullscreen(); }
    else { document.documentElement.requestFullscreen(); }
    var c = document.getElementById('canvas'); if (c) c.focus();
  };
  document.body.appendChild(b);
})();
"""


def fit_browser():
    """Browser only: scale the canvas to fill the window, keeping 16:9 (bars fill the rest).
    Called regularly because the pygbag loader resizes the canvas itself."""
    global _last_fit
    if not WEB:
        return
    try:
        import platform
        win = platform.window
        vw, vh = int(win.innerWidth), int(win.innerHeight)
        scale = min(vw / WIDTH, vh / HEIGHT)
        w, h = int(WIDTH * scale), int(HEIGHT * scale)
        style = win.canvas.style
        if _last_fit == (vw, vh) and style.width == f"{w}px" and style.height == f"{h}px":
            return
        _last_fit = (vw, vh)
        body = win.document.body.style
        body.margin = "0"
        body.padding = "0"
        body.overflow = "hidden"
        body.backgroundColor = "#090f1c"
        style.position = "fixed"
        style.margin = "0"
        style.padding = "0"
        style.border = "none"
        style.display = "block"
        style.left = f"{(vw - w) // 2}px"
        style.top = f"{(vh - h) // 2}px"
        style.width = f"{w}px"
        style.height = f"{h}px"
        win.eval(_BUTTON_JS)
    except Exception:
        pass
