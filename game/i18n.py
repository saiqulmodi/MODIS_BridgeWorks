"""Language support: English and Bengali (বাংলা).

Text is translated where it is drawn (game/ui.py), so the rest of the code keeps writing
plain English. Fixed strings are looked up whole; strings that contain changing numbers
are matched by the regular-expression patterns in lang_bn.py. Formulas and numbers stay
as they are.
"""
import re

LANGS = ("en", "bn")
_lang = "en"
_record = None          # set() while collecting strings for translation/coverage checks


def lang():
    return _lang


def set_lang(code):
    global _lang
    if code not in LANGS:
        raise ValueError(code)
    _lang = code


def toggle():
    set_lang("bn" if _lang == "en" else "en")
    return _lang


def has_bengali(s):
    return any("ঀ" <= ch <= "৿" for ch in s)


def start_recording():
    global _record
    _record = set()
    return _record


def stop_recording():
    global _record
    rec, _record = _record, None
    return rec


def tr(s):
    """Translate one displayed string into the current language."""
    if not isinstance(s, str):
        s = str(s)
    if _record is not None:
        _record.add(s)
    if _lang == "en" or not s or has_bengali(s):
        return s
    from . import lang_bn
    if "\n" in s and s not in lang_bn.EXACT:
        return "\n".join(tr(line) for line in s.split("\n"))
    hit = lang_bn.EXACT.get(s)
    if hit is not None:
        return hit
    stripped = s.strip()
    if stripped != s and stripped in lang_bn.EXACT:
        return s.replace(stripped, lang_bn.EXACT[stripped])
    for pattern, repl in lang_bn.COMPILED:
        m = pattern.fullmatch(s)
        if m:
            return repl(m) if callable(repl) else m.expand(repl)
    return s


def untranslated(s):
    """True if a string still shows English words in Bengali mode (used by the tests)."""
    from . import lang_bn
    out = tr(s) if _lang == "bn" else s
    if has_bengali(out):
        return False
    words = re.findall(r"[A-Za-z]{3,}", out)
    return any(w.lower() not in lang_bn.KEEP for w in words)
