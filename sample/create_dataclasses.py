import shutil
import subprocess

from fastlite import create_mod

from dnd_engine.data.fastlite_db import DB

name = "fastlite_dataclasses"
create_mod(DB, name)
shutil.move(f"{name}.py", f"dnd_engine/data/{name}.py")
subprocess.run(["black", f"dnd_engine/data/{name}.py"])
