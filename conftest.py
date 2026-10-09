# Lets pytest import the `engine` package from the project root.
import os

# Tests check the built-in Academy only; big banks (banks/) are tested with their own temporary folder.
os.environ.setdefault("BRIDGEWORKS_NO_BANKS", "1")
