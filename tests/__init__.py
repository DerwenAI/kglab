from os.path import abspath, dirname
import sys
from pathlib import Path

sys.path.insert(0, str(Path(dirname(dirname(abspath(__file__))))))

DAT_FILES_DIR = Path(dirname(abspath(__file__))) / "dat"
