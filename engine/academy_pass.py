"""Scholarship Pass hook - where a paid subscription would plug in later.

Today the Academy is free for everyone: has_access() always returns True and no payment,
account or personal data is collected anywhere in the game. To sell a pass later, replace
has_access() with a check against a real payment provider's verified receipt (stored
server-side, never typed into the game) and keep FREE_PREVIEW_CLASSES open as a sample.
"""

PASS_REQUIRED = False            # flip only together with a real, verified payment check
FREE_PREVIEW_CLASSES = (1, 2, 3)


def has_access(save, class_level):
    if not PASS_REQUIRED or class_level in FREE_PREVIEW_CLASSES:
        return True
    return bool(save.data.get("academy", {}).get("pass_verified"))
