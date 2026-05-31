import csv
from pathlib import Path
from typing import Optional

from oop_spells.spellcaster import Spellcaster
from oop_spells.spells import name_to_spell


class Storage:
    """
    A storage container containing a list of spellcasters.
    """
    def __init__(self) -> None:
        """
        Create an empty spellcaster storage container.
        """
        self.__spellcasters = []

    def __str__(self) -> str:
        """
        :return: A line-separated string of each spellcaster and their index in the list.
        """
        output = ""
        for i in range(len(self.__spellcasters)):
            output += f"{i} - {str(self.__spellcasters[i])}"
            if i < len(self.__spellcasters) - 1:
                output += "\n"
        return output

    def __len__(self) -> int:
        """
        :return: The number of spellcasters in the storage.
        """
        return len(self.__spellcasters)

    def get(self, index: int) -> Optional[Spellcaster]:
        """
        Gets the spellcaster at the specified index.
        :param index: Index to check.
        :return: The spellcaster, or None if the index is out of range.
        """
        if 0 <= index < len(self.__spellcasters):
            return self.__spellcasters[index]
        return None

    def add(self, spellcaster: Spellcaster) -> None:
        """
        Adds a spellcaster to the end of the storage list.
        :param spellcaster: Spellcaster to add.
        """
        self.__spellcasters.append(spellcaster)

    def insert(self, index: int, spellcaster: Spellcaster) -> None:
        """
        Inserts a spellcaster at a specified index in the storage list.
        :param index: Index of the list to insert at.
        :param spellcaster: Spellcaster to add.
        """
        self.__spellcasters.insert(index, spellcaster)

    def remove(self, index: int) -> Optional[Spellcaster]:
        """
        Removes the spellcaster at a specified index in the storage list.
        :param index: Index of the list to remove from.
        :return: The removed spellcaster, or None if no spellcaster was removed.
        """
        if 0 <= index < len(self.__spellcasters):
            return self.__spellcasters.pop(index)
        return None

    def save(self, file_path: Path) -> None:
        """
        Saves the spellcaster storage list to a CSV file.
        :param file_path: Path of the CSV file to save to.
        """
        with open(file_path, "w", newline=""): # Mode: "w" (write)
            pass # Do nothing; clears the CSV file

        for spellcaster in self.__spellcasters:
            spellcaster.save(file_path)

    def load(self, file_path: Path) -> None:
        """
        Loads the spellcaster storage list from a CSV file.
        :param file_path: Path of the CSV file to load from.
        """
        self.__spellcasters = []

        with open(file_path, "r", newline="") as file: # Mode: "r" (read)
            reader = csv.reader(file)
            for row in reader:
                spell_list = []
                for i in range(4, len(row)):
                    spell_list.append(name_to_spell(row[i]))
                self.__spellcasters.append(Spellcaster(row[0],
                                                       spell_list,
                                                       float(row[1]),
                                                       float(row[2]),
                                                       float(row[3])))

def delete_csv_file(file_path: Path) -> bool:
    """
    Deletes the CSV file at the specified path.
    :param file_path: Path of the CSV file to delete.
    :return: True if the file was successfully deleted, otherwise False.
    """
    try:
        if (not file_path.exists()) or file_path.suffix.lower() != ".csv":
            return False
        file_path.unlink()
        return True
    except Exception:
        return False