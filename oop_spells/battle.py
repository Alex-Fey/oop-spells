import random
from typing import List, Optional

from oop_spells.helpers import format_column_line, written_list
from oop_spells.spellcaster import Spellcaster
from oop_spells.spells import Spell, Heal


class Battle:
    """
    A battle between two teams of spellcasters.
    """
    def __init__(self, team_1: List[Spellcaster] = None, team_2: List[Spellcaster] = None, mana_per_round: int = 5) -> None:
        """
        Creates a battle between two groups of spellcasters.
        :param team_1: List of spellcasters on Team 1.
        :param team_2: List of spellcasters on Team 2.
        :param mana_per_round: Mana each spellcaster regenerates per round.
        """
        self.__team_1 = [] if team_1 is None else list(team_1) # Create a copy of the list to prevent mutation
        self.__team_2 = [] if team_2 is None else list(team_2) # Create a copy of the list to prevent mutation
        self.__mana_per_round = mana_per_round

    def __str__(self) -> str:
        """
        :return: Column-formatted string of every spellcaster's index+1, name, health percentage, and mana percentage.
            Team 1 is placed in the left column, and team 2 in the right.
        """
        battle_size = max(len(self.__team_1), len(self.__team_2))
        output = format_column_line(["-"*6 + " Team 1 " + "-"*6, "-"*6 + " Team 2 " + "-"*6], 20) + "\n"

        for i in range(battle_size):
            if i < len(self.__team_1):
                left_name = f"[{i}] " + self.__team_1[i].name()
                left_hp = self.__team_1[i].health_str()
                left_mp = self.__team_1[i].mana_str()
            else:
                left_name = ""
                left_hp = ""
                left_mp = ""

            if i < len(self.__team_2):
                right_name = f"[{i}] " + self.__team_2[i].name()
                right_hp = self.__team_2[i].health_str()
                right_mp = self.__team_2[i].mana_str()
            else:
                right_name = ""
                right_hp = ""
                right_mp = ""

            output += format_column_line([left_name, right_name], 20) + "\n"
            output += format_column_line([left_hp, right_hp], 20) + "\n"
            output += format_column_line([left_mp, right_mp], 20) + "\n"
            if i < battle_size - 1:
                output += format_column_line(["", ""], 20) + "\n"
        output += format_column_line(["-"*20, "-"*20], 20)
        return output

    def len(self, team: int) -> int:
        """
        :param team: Team to check (1 or 2).
        :return: Number of spellcasters in that team (0 if invalid team number entered)
        """
        if team == 1:
            return len(self.__team_1)
        elif team == 2:
            return len(self.__team_2)
        else:
            return 0

    def mana_per_round(self) -> float:
        """
        :return: Mana each spellcaster regenerates per round.
        """
        return self.__mana_per_round

    def set_mana_per_round(self, mana: float) -> None:
        """
        Sets the mana each spellcaster regenerates per round.
        :param mana: Amount of mana to regenerate.
        """
        self.__mana_per_round = mana

    def alive_indexes(self, team: int) -> List[int]:
        """
        :param team: Team to check.
        :return: A list of the indexes of the team's spellcasters who are not dead.
        """
        team_list = self.__team_1 if team == 1 else self.__team_2
        alive_list = []

        for i in range(len(team_list)):
            if team_list[i].health_percentage() > 0:
                alive_list.append(i)

        return alive_list

    def get_name(self, team: int, index: int) -> str:
        """
        Gets the name of the specified spellcaster.
        :param team: Team the spellcaster is on.
        :param index: Index of the spellcaster in that team.
        :return: Name of the spellcaster, or "" if that spellcaster wasn't found.
        """
        try:
            if team == 1:
                return self.__team_1[index].name()
            elif team == 2:
                return self.__team_2[index].name()
            return ""
        except IndexError:
            return ""

    def get_spells(self, team: int, index: int) -> List[Spell]:
        """
        Gets a list of the spells of the specified spellcaster.
        :param team: Team the spellcaster is on.
        :param index: Index of the spellcaster in that team.
        :return: List of the spellcaster's spells, or an empty list if that spellcaster wasn't found.
        """
        try:
            if team == 1:
                return self.__team_1[index].spells()
            elif team == 2:
                return self.__team_2[index].spells()
            return []
        except IndexError:
            return []

    def get_castable_spells(self, team: int, index: int) -> List[Spell]:
        """
        Gets a list of the castable spells of the specified spellcaster.
        :param team: Team the spellcaster is on.
        :param index: Index of the spellcaster in that team.
        :return: List of the spellcaster's spells that they have enough mana to cast, or an empty list if that spellcaster wasn't found.
        """
        try:
            if team == 1:
                return self.__team_1[index].castable_spells()
            elif team == 2:
                return self.__team_2[index].castable_spells()
            return []
        except IndexError:
            return []

    def add(self, team: int, spellcaster: Spellcaster) -> None:
        """
        Adds a spellcaster to the end of the specified team.
        :param team: Team to add the spellcaster to (1 or 2).
        :param spellcaster: Spellcaster to add.
        """
        if team == 2:
            self.__team_2.append(spellcaster)
        else:
            self.__team_1.append(spellcaster)

    def insert(self, team: int, index: int, spellcaster: Spellcaster) -> None:
        """
        Inserts a spellcaster at a specified index in the specified team.
        :param team: Team to add the spellcaster to (1 or 2).
        :param index: The index of the team to insert at.
        :param spellcaster: Spellcaster to add.
        """
        if team == 2:
            self.__team_2.insert(index, spellcaster)
        else:
            self.__team_1.insert(index, spellcaster)

    def remove(self, team: int, index: int) -> Optional[Spellcaster]:
        """
        Removes the spellcaster at a specified index in the specified team.
        :param team: Team to remove the spellcaster from (1 or 2).
        :param index: The index of the team to remove from.
        :return: The removed spellcaster, or None if no spellcaster was removed.
        """
        if team == 2 and 0 <= index < len(self.__team_2):
            return self.__team_2.pop(index)
        elif team == 1 and 0 <= index < len(self.__team_1):
            return self.__team_1.pop(index)
        else:
            return None

    def clear(self, team: int):
        """
        Removes all spellcasters from the specified team.
        :param team: Team to empty.
        """
        if team == 1:
            self.__team_1 = []
        elif team == 2:
            self.__team_2 = []

    def cast_spell(self, team: int, index: int, spell: Spell, target_team: int, target_index: int) -> List[str]:
        """
        Make the specified caster cast the specified spell to the specified target location.
        :param team: Team containing the caster of the spell (1 or 2).
        :param index: The caster's index its team.
        :param spell: The spell to cast.
        :param target_team: Number of the team being targeted (1 or 2).
        :param target_index: The spell's target index its team.
        :return: A list of the names of the spellcasters this spell killed, or an empty list otherwise.
        :raises UnknownSpellError: If the spellcaster doesn't know the spell.
        :raises NotEnoughManaError: If the spellcaster doesn't have enough mana to cast the spell.
        :raises DeadError: If the spellcaster is dead.
        """
        casting_team = self.__team_1 if team == 1 else self.__team_2
        targeted_team = self.__team_1 if target_team == 1 else self.__team_2
        dead_list = []

        casting_team[index].cast_spell(spell)

        for i in range(len(targeted_team)):
            if targeted_team[i].take_damage(spell.damage(i, target_index) * casting_team[index].damage_mod()):
                dead_list.append(targeted_team[i].name())

        return dead_list

    def cast_random_spell(self, team: int) -> str:
        """
        Make a random caster from the specified team cast a random spell on a random target in the opposing team, with
        spellcasters that have lower health being weighted higher.

        A spell is only chosen if its caster has enough mana to cast it, otherwise a different spell or caster is
        chosen. If no caster on the team has enough mana for any spell, no spell is cast.

        If the spell is a heal spell, the target is a random spellcaster on the caster's team, with spellcasters that
        have lower health being weighted higher.

        :param team: Team containing the caster of the spell (1 or 2).
        :return: A message stating the caster, the spell cast, and who the spell killed.
        """
        casting_team = self.__team_1 if team == 1 else self.__team_2
        can_cast_indexes = []
        for i in range(len(casting_team)):
            if len(casting_team[i].castable_spells()) != 0:
                can_cast_indexes.append(i)

        if len(can_cast_indexes) == 0:
            return f"Team {team} did absolutely nothing!"

        caster_index = random.choice(can_cast_indexes)
        spell = random.choice(casting_team[caster_index].castable_spells())

        # XOR operator ^: True if one of the two conditions is True, False otherwise
        if (team == 1) ^ (spell == Heal()):
            target_team = self.__team_2
            target_team_num = 2
        else:
            target_team = self.__team_1
            target_team_num = 1

        target_indexes = []
        target_weights = []
        for i in range(len(target_team)):
            if target_team[i].health_percentage() != 0:
                target_indexes.append(i)
                target_weights.append(1 / target_team[i].health_percentage())

        target_index = random.choices(target_indexes, weights=target_weights, k=1)[0]

        dead_list = self.cast_spell(team, caster_index, spell, target_team_num, target_index)

        if len(dead_list) == 0:
            return f"{casting_team[caster_index].name()} casts {spell.name()}!\nThe battle continues."
        else:
            return (f"{casting_team[caster_index].name()} casts {spell.name()}!\n" +
                      f"{casting_team[caster_index].name()} killed {written_list(dead_list)}!")

    def next_round(self) -> None:
        """
        Move to the next round, making all alive spellcasters regenerate mana.
        """
        for spellcaster in self.__team_1:
            if spellcaster.health_percentage() > 0:
                spellcaster.regen_mana(self.__mana_per_round)
        for spellcaster in self.__team_2:
            if spellcaster.health_percentage() > 0:
                spellcaster.regen_mana(self.__mana_per_round)

    def winner(self) -> int:
        """
        :return: 1 if Team 1 wins, 2 if Team 2 wins, 0 if there's a tie, or -1 if no teams are defeated.
        """
        team_1_defeated = True
        team_2_defeated = True

        for spellcaster in self.__team_1:
            if spellcaster.health_percentage() > 0:
                team_1_defeated = False

        for spellcaster in self.__team_2:
            if spellcaster.health_percentage() > 0:
                team_2_defeated = False

        if team_1_defeated and team_2_defeated:
            return 0
        elif team_1_defeated:
            return 2
        elif team_2_defeated:
            return 1
        else:
            return -1