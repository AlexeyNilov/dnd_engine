import shutil
import subprocess

from fastlite import create_mod

from dnd_engine.data.fastlite_db import DB

create_mod(DB, "db_dataclasses")
shutil.move("db_dataclasses.py", "dnd_engine/data/db_dataclasses.py")
subprocess.run(["black", "dnd_engine/data/db_dataclasses.py"])
