import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from lib import write
import hero
TARGETS = {"hero-online.svg": hero.build}
for mod in ["loop", "terminal", "reactions", "architecture", "hardware", "panels"]:
    try:
        m = __import__(mod)
        TARGETS.update(m.TARGETS)
    except ModuleNotFoundError as e:
        if e.name != mod: raise
only = sys.argv[1:]
for name, fn in TARGETS.items():
    if only and name not in only: continue
    p, n = write(name, fn())
    print(f"{name:32s} {n/1024:7.1f} KB")
