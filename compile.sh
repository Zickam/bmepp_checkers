echo "Starting compilation..."
. venv/bin/activate
python -m nuitka --static-libpython=no --onefile --enable-console main.py --include-data-dir=data=data --include-onefile-external-data=gui
echo "Compilation finished!"
read -p "Press enter to continue"
