echo "Starting compilation..."
. venv/bin/activate
python3 -m nuitka --static-libpython=no --onefile main.py
echo "Compilation finished!"
