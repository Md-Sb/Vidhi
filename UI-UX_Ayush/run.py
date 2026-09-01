"""
run.py — VIDI Launcher
=======================
Use this instead of `streamlit run app.py` if your system
blocks Streamlit from writing to the default home directory.

Run with:
    python run.py
"""
import os
import sys

# Redirect Streamlit's home to THIS folder (e:\Vidhi UI)
# so it uses .streamlit\config.toml and credentials.toml here
# instead of C:\Users\<you>\.streamlit
project_dir = os.path.dirname(os.path.abspath(__file__))
os.environ["USERPROFILE"] = project_dir
os.environ["HOME"] = project_dir

# Launch Streamlit programmatically
from streamlit.web import cli as stcli

sys.argv = [
    "streamlit", "run", "app.py",
    "--server.headless", "false",
    "--browser.serverAddress", "localhost",
]
sys.exit(stcli.main())
