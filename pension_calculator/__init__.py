__version__ = "0.1.0"
import os
from pathlib import Path
import datetime
import toml

ROOT = Path(os.path.dirname(os.path.abspath(__file__)))
PLOT_DIR = ROOT / "plot" / "figures"
CONFIG = toml.load(f"{ROOT}/app.config.toml")
CURRENT_YEAR = datetime.date.today().year
