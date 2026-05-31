from oop_spells.oop_spells_io import OOPSpellsIO


if __name__ == "__main__":
    io = OOPSpellsIO()
    io.main()

# Command used to convert to EXE:
# pyinstaller --onefile --console --icon=icon/oop_spells_icon.ico oop_spells/__main__.py
# Note: build folder, dist folder, and __main__.spec were not kept.