import os
PACKDIR = os.path.abspath(os.path.dirname(__file__))

if "HOME" in os.environ:
    HOME = os.getenv("HOME")
elif "HOMEPATH" in os.environ:
    HOME = os.getenv("HOMEPATH")
else:
    HOME = ""
