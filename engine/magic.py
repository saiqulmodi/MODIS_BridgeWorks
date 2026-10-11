"""Magic hero tools in Campus World, earned by learning.

Players who study in Class 1-7 get a tool belt. Each tool unlocks after enough right
first-try answers to BridgeWorks Academy questions of certain classes (the Class 1-7 school
syllabus):
  * ZIP   - web-zip onto a roof        : Class 1-2 questions
  * BOOTS - super jump                 : Class 3-4 questions
  * CAPE  - glide down slowly          : Class 5-7 questions
The rope swing (WEB) is open to everyone, as before. Players in Class 8 and above (and NIT /
IIT) keep the plain rope swing.
"""

MAX_CLASS = 7
NEED = 5                    # right first-try answers that unlock a tool

TOOLS = [
    # key, classes, name (en, bn), what it does (en, bn)
    ("zip", (1, 2), ("ZIP", "জিপ"), ("Web-zip onto a roof", "জাল ছুড়ে ছাদে ওঠো")),
    ("boots", (3, 4), ("BOOTS", "বুট"), ("Super jump", "বিরাট লাফ")),
    ("cape", (5, 6, 7), ("CAPE", "কেপ"), ("Float down slowly", "ধীরে ভেসে নামো")),
]
BY_KEY = {t[0]: t for t in TOOLS}


def eligible(save):
    """Only players studying in Class 1-7 get the tool belt."""
    return 1 <= int(save.academy.get("class", 5)) <= MAX_CLASS


def right_answers(save, classes):
    """Right first-try answers to built-in Academy questions of these classes.
    Built-in ids are class * 10000 + subject * 1000 + n (Game-skills ids start at 900000)."""
    n = 0
    for key, right in save.academy["answered"].items():
        if right and key.isdigit() and int(key) // 10000 in classes:
            n += 1
    return n


def progress(save, key):
    """(right answers so far, needed) for one tool."""
    return min(NEED, right_answers(save, BY_KEY[key][1])), NEED


def unlocked(save, key):
    if not eligible(save):
        return False
    have, need = progress(save, key)
    return have >= need


def class_range(key):
    classes = BY_KEY[key][1]
    return f"{classes[0]}-{classes[-1]}"
