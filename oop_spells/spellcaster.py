import csv
import math
import random
from pathlib import Path
from typing import List

from oop_spells.spells import Spell


class Spellcaster:
    """
    A spellcaster that can cast spells and receive damage in a battle.
    """
    def __init__(self,
                 name: str,
                 spells: List[Spell] = None,
                 max_health: float = 100.0,
                 max_mana: float = 100.0,
                 damage_mod: float = 1.0) -> None:
        """
        Creates a spellcaster at full health and full mana.
        :param name: Name of the spellcaster.
        :param spells: List of spells the spellcaster can cast.
        :param max_health: Max health of the spellcaster.
        :param max_mana: Max mana of the spellcaster.
        :param damage_mod: Damage multiplier on all spells the spellcaster casts.
        """
        self.__name = name
        self.__spells = [] if spells is None else list(spells) # Create a copy of the list to prevent mutation
        self.__max_health = max_health
        self.__max_mana = max_mana
        self.__health = self.__max_health
        self.__mana = self.__max_mana
        self.__damage_mod = damage_mod

        # self.var = ... creates a public field (accessible everywhere, may be used everywhere)
        # self._var = ... creates a protected field (accessible everywhere, only meant to be used by subclasses)
        # self.__var = ... creates a private field (accessible everywhere as _ClassName__var, not meant to be used by anything else)

    def __str__(self) -> str:
        """
        :return: A string representation of a spellcaster in the form of "{Name} [HP: {max HP}, MP: {max MP}, DMG: {damage modifier}]: {Spells}".
        """
        spells_str = ""
        for spell in self.__spells:
            spells_str += f"{spell.name()}, "
        spells_str = spells_str[:-2]
        return f"{self.__name} [HP: {self.__max_health:g}, MP: {self.__max_mana:g}, DMG: {self.__damage_mod:g}]: {spells_str}"
        # "g" is "general format" which prints the number as a fixed-point number, unless the number is too large,
        # in which case it switches to "e" exponent notation.

    def name(self) -> str:
        """
        :return: Name of the spellcaster.
        """
        return self.__name # Strings are immutable so this is okay

    def spells(self) -> List[Spell]:
        """
        :return: List of the spellcaster's spells.
        """
        return list(self.__spells) # Lists are mutable so we have to create a copy or a tuple

    def castable_spells(self) -> List[Spell]:
        """
        :return: List of the spellcaster's spells that they have enough mana to cast.
        """
        output = []
        for spell in self.__spells:
            if self.__mana >= spell.mana_cost():
                output.append(spell)
        return output

    def health_percentage(self) -> float:
        """
        :return: Percentage of the spellcaster's health from 0 to 1.
        """
        return self.__health / self.__max_health

    def health_str(self) -> str:
        """
        :return: "HP: {HP}%" where {HP} is the percentage of the spellcaster's health left, rounded down.
        """
        return f"HP: {math.floor(100 * self.__health / self.__max_health)}%"

    def mana_percentage(self) -> float:
        """
        :return: Percentage of the spellcaster's mana from 0 to 1.
        """
        return self.__mana / self.__max_mana

    def mana_str(self) -> str:
        """
        :return: "MP: {MP}%" where {MP} is the percentage of the spellcaster's mana left, rounded down.
        """
        return f"MP: {math.floor(100 * self.__mana / self.__max_mana)}%"

    def take_damage(self, damage: float) -> bool:
        """
        Makes the spellcaster take damage. If the spellcaster dies, their health and mana are set to 0.
        :param damage: Amount of damage to take.
        :return: True if this damage kills the spellcaster, False otherwise.
        """
        if self.__health == 0:
            return False

        self.__health -= damage
        if self.__health <= 0:
            self.__health = 0
            self.__mana = 0
            return True
        elif self.__health > self.__max_health:
            self.__health = self.__max_health
        return False

    def cast_spell(self, spell: Spell = None) -> None:
        """
        Makes the spellcaster use up the mana cost of a spell if they know that spell, have enough mana to cast it, and are alive.
        :param spell: Spell to cast. If empty, casts a random spell.
        :raises UnknownSpellError: If the spellcaster doesn't know the spell.
        :raises NotEnoughManaError: If the spellcaster doesn't have enough mana to cast the spell.
        :raises DeadError: If the spellcaster is dead.
        """
        if spell is None:
            self.cast_spell(self.__spells[random.randint(0,len(self.__spells)-1)])
            return

        if spell not in self.__spells:
            raise UnknownSpellError(self.__name, spell)

        if self.__health == 0:
            raise DeadError(self.__name, spell)

        if self.__mana < spell.mana_cost():
            raise NotEnoughManaError(self.__name, spell)

        self.__mana -= spell.mana_cost()

    def damage_mod(self) -> float:
        """
        :return: Spellcaster's damage modifier.
        """
        return self.__damage_mod

    def regen_mana(self, mana: float):
        """
        Makes the spellcaster regenerate mana if they're alive.
        :param mana: Amount of mana to regenerate.
        """
        if self.__health == 0:
            return

        self.__mana += mana
        if self.__mana > self.__max_mana:
            self.__mana = self.__max_mana

    def save(self, file_path: Path) -> None:
        """
        Saves the spellcaster as a new row in a csv file with the given path.
        """
        spell_name_list = []
        for spell in self.__spells:
            spell_name_list.append(spell.name())

        full_list = [self.__name,
                     self.__max_health,
                     self.__max_mana,
                     self.__damage_mod]
        full_list.extend(spell_name_list)

        with open(file_path, "a", newline="") as file: # Mode: "a" (append)
            writer = csv.writer(file)
            writer.writerow(full_list)


class UnknownSpellError(Exception):
    """
    Exception raised when a trying to cast a spell that the spellcaster doesn't know.
    """
    def __init__(self, name: str, spell: Spell):
        """
        Creates an UnknownSpellError.
        :param name: Name of the spellcaster.
        :param spell: Spell attempted to cast.
        """
        self.message = f"{name} does not know {spell}."
        super().__init__(self.message)

    def __str__(self):
        return self.message


class NotEnoughManaError(Exception):
    """
    Exception raised when a trying to cast a spell that the spellcaster does not have enough mana for.
    """
    def __init__(self, name: str, spell: Spell):
        """
        Creates a NotEnoughManaError.
        :param name: Name of the spellcaster.
        :param spell: Spell attempted to cast.
        """
        self.message = f"{name} does not have enough mana for {spell}."
        super().__init__(self.message)

    def __str__(self):
        return self.message

class DeadError(Exception):
    """
    Exception raised when a trying to cast a spell while the spellcaster is dead.
    """
    def __init__(self, name: str, spell: Spell):
        """
        Creates a DeadError.
        :param name: Name of the spellcaster.
        :param spell: Spell attempted to cast.
        """
        self.message = f"{name} cannot cast {spell} because they're dead."
        super().__init__(self.message)

    def __str__(self):
        return self.message