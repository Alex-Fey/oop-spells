import copy
from math import inf

from oop_spells.battle import Battle
from oop_spells.helpers import *
from oop_spells.spellcaster import Spellcaster
from oop_spells.spells import *
from oop_spells.storage import Storage, delete_csv_file


class OOPSpellsIO:
    """
    Handles user interactions with OOP Spells via the console.
    """
    def __init__(self) -> None:
        """
        Creates a new BattleIO object.
        """
        # Get a list of the paths of all files (assumed to be CSV storage files) in AppData / PolarisMagic / OOPSpells / storage
        self.__storage_paths = []
        self.__storage_folder_path = create_or_get_appdata_path(Path("PolarisMagic/OOPSpells/storage"))
        self.__update_storage_paths()

        self.__ba = Battle()
        self.__pvp = False
        self.__team_1_first = True

    def __update_storage_paths(self) -> None:
        """
        Sets self.__storage_paths to a list of the paths of all files storage folder.
        """
        self.__storage_paths = []
        for file in self.__storage_folder_path.iterdir():
            self.__storage_paths.append(file)

    def main(self) -> None:
        """
        Main user I/O controller for OOP Spells, where storage is accessed and battles can be initiated.
        """
        # ----- MENU -----
        m_action = None
        while m_action != 2:
            print()
            print(format_column_line(["-"*20], 20))
            print(format_column_line([" "*5 + "OOP Spells"], 20))
            print(format_column_line([""], 20))
            print(format_column_line(["0: Assemble battle"], 20))
            print(format_column_line(["1: Access storage"], 20))
            print(format_column_line(["2: Exit"], 20))
            print(format_column_line([""], 20))
            print(format_column_line(["Enter a number."], 20))
            print(format_column_line(["-"*20], 20))

            m_action = input_valid_int(0, 2)
            if m_action == 0:
                self.assemble_battle()
            elif m_action == 1:
                self.access_storage()
            elif m_action == 2:
                print("\nBye.")

    def access_storage(self) -> None:
        """
        User I/O controller for accessing and manipulating spellcaster storages.
        """
        # ----- STORAGE SELECTION -----
        ss_action = None
        ss_exit = False
        while not ss_exit:
            print("\n----- Storage -----")
            print("\nSelect an option.")
            print("0: Create a new storage file")
            for i in range(len(self.__storage_paths)):
                print(f'{i + 1}: Access "{self.__storage_paths[i].stem}"')
            print(f"{len(self.__storage_paths) + 1}: Back")
            ss_action = input_valid_int(0, len(self.__storage_paths) + 1)

            if ss_action == 0:

                # ----- STORAGE CREATION -----
                print("Name this storage file.")
                storage_name = input()
                while not is_valid_file_name(storage_name):
                    print("File name invalid. Please enter a different one.")
                    storage_name = input()
                s = Storage()
                spellcaster = self.create_spellcaster()
                s.add(spellcaster)
                s.save(self.__storage_folder_path / f"{storage_name}.csv")
                self.__update_storage_paths()
                print(f"\n{storage_name} created! Currently contains {spellcaster.name()}.")

            elif 0 < ss_action <= len(self.__storage_paths):

                # ----- STORAGE -----
                index = ss_action - 1
                s = Storage()
                s.load(self.__storage_paths[index])

                s_action = None
                while s_action != 3 and s_action != 4 and s_action != 5:
                    print(f"\n----- {self.__storage_paths[index].stem} -----")
                    print(f'\nContents of "{self.__storage_paths[index].stem}":\n{str(s)}')
                    print(f"\nSelect an option.\n" +
                          "0: Add a spellcaster\n" +
                          "1: Insert a spellcaster\n" +
                          "2: Remove a spellcaster\n" +
                          "3: Delete this storage\n" +
                          "4: Exit without saving\n" +
                          "5: Save and exit")

                    s_action = input_valid_int(0, 5)
                    if s_action == 0:

                        # ----- STORAGE ADD -----
                        spellcaster = self.create_spellcaster()
                        s.add(spellcaster)
                        print(f"\n{spellcaster.name()} added!")

                    elif s_action == 1:

                        # ----- STORAGE INSERT -----
                        spellcaster = self.create_spellcaster()
                        print(f"\nWhere to place the spellcaster? (Spellcasters in that location and on will be pushed forward.)")
                        print(str(s))
                        si_action = input_valid_int(0, len(s))
                        s.insert(si_action, spellcaster)
                        print(f"\n{spellcaster.name()} inserted!")

                    elif s_action == 2:

                        # ----- STORAGE REMOVE -----
                        print("\nWhich spellcaster to remove? Enter a number to remove, or anything else to cancel.")
                        print(str(s))
                        sr_action = input()
                        if can_be_int(sr_action) and 0 <= int(sr_action) < len(s):
                            print(f"\n{s.get(int(sr_action)).name()} removed!")
                            s.remove(int(sr_action))
                        else:
                            print("\nCancelled.")

                    elif s_action == 3:

                        # ----- STORAGE DELETE -----
                        print(f'\nAre you sure you want to delete "{self.__storage_paths[index].stem}"?\n' +
                              "0: Delete\n" +
                              "1: Cancel")
                        sd_action = input()
                        if sd_action == "0":
                            file_name = self.__storage_paths[index].stem
                            if delete_csv_file(self.__storage_paths[index]):
                                self.__update_storage_paths()
                                print(f'\n"{file_name}" deleted!')
                            else:
                                print("\nFailed to delete.")
                        else:
                            print("\nCancelled.")

                    elif s_action == 5:

                        # ----- STORAGE SAVE -----
                        s.save(self.__storage_paths[index])
                        print(f'\n"{self.__storage_paths[index].stem}" saved!')

            else:
                ss_exit = True

    def create_spellcaster(self) -> Spellcaster:
        """
        User I/O controller for creating a spellcaster.
        :return: Spellcaster that the user creates.
        """
        print("\nCreate a spellcaster.")
        name = input("Name: ")

        max_health = input_valid_float(0, inf, False, False, "Max health: ")
        max_mana = input_valid_float(0, inf, False, False, "Max mana: ")
        damage_mod = input_valid_float(-inf, inf, False, False, "Damage modifier: ")

        spells = []
        spells_names = []
        remaining_spells_str = [str(MagicMissile()), str(Fireball()), str(LightningBolt()), str(BlindingFlash()), str(Earthquake()), str(Heal())]
        while len(remaining_spells_str) > 0:
            print()
            if len(spells) > 0:
                print(f"Selected spells: {', '.join(spells_names)}")
            print("Select spell(s):")
            for i in range(len(remaining_spells_str)):
                print(f"{i}: {remaining_spells_str[i]}")
            print(f"{len(remaining_spells_str)}: Finish spellcaster creation")
            spell_input = input_valid_int(0, len(remaining_spells_str))
            if spell_input < len(remaining_spells_str):
                spell = str_to_spell(remaining_spells_str[spell_input])
                spells.append(spell)
                spells_names.append(spell.name())
                remaining_spells_str.pop(spell_input)
            elif spell_input == len(remaining_spells_str):
                break

        print(f"\n{name} created!\n" +
              f"| {max_health:g} HP, {max_mana:g} MP, {damage_mod:g} damage modifier")
        if len(spells) > 0:
            print(f"| Knows {', '.join(spells_names)}")
        else:
            print("| Knows nothing; skill issue")

        return Spellcaster(name, spells, max_health, max_mana, damage_mod)

    def create_or_load_spellcaster(self) -> Spellcaster:
        """
        User I/O controller for creating a spellcaster or loading it from storage.
        :return: Spellcaster that the user creates or loads.
        """
        print("\nCreate or load a spellcaster.\n" +
              "0: Create a new spellcaster")
        for i in range(len(self.__storage_paths)):
            print(f'{i + 1}: Load from "{self.__storage_paths[i].stem}"')

        choice = input_valid_int(0, len(self.__storage_paths))
        if choice == 0:
            return self.create_spellcaster()

        index = choice - 1
        storage = Storage()
        storage.load(self.__storage_paths[index])
        print(f'\nContents of "{self.__storage_paths[index].stem}":\n{str(storage)}')
        print("Choose a spellcaster.")
        choice = input_valid_int(0, len(storage) - 1)
        return storage.get(choice)


    def assemble_battle(self) -> None:
        """
        User IO controller for assembling a battle.
        """
        # ----- BATTLE ASSEMBLY -----
        ba_action = None
        selected_team = 1
        while ba_action != 8 and ba_action != 9:
            print("\n----- Battle Assembly -----\n")
            print(str(self.__ba))
            print(f"Mana regen per round: {self.__ba.mana_per_round():g}")
            print("** PVP: Each player controls a team" if self.__pvp else "*- PVE: You control Team 1")
            print("First turn: Team 1" if self.__team_1_first else "First turn: Team 2")
            print("\nSelect an option.\n" +
                  "0: Load storage into a team\n" +
                  "1: Add a spellcaster\n" +
                  "2: Insert a spellcaster\n" +
                  "3: Remove a spellcaster\n" +
                  "4: Clear team\n" +
                  "5: Change mana per round\n" +
                  "6: Toggle PVP\n" +
                  "7: Toggle who starts first\n" +
                  "8: Fight!\n" +
                  "9: Back")

            ba_action = input_valid_int(0, 9)
            if 0 <= ba_action <= 3:
                selected_team = input_valid_int(1, 2, True, True, "\nTeam: ")

            if ba_action == 0:

                # ----- BATTLE ASSEMBLY LOAD -----
                print(f"\nWhich storage to load? (Enter {len(self.__storage_paths)} to cancel.)")
                for i in range(len(self.__storage_paths)):
                    print(f'{i}: "{self.__storage_paths[i].stem}"')
                print(f"{len(self.__storage_paths)}: Cancel")
                bal_action = input()
                if can_be_int(bal_action) and 0 <= int(bal_action) < len(self.__storage_paths):
                    self.__ba.clear(selected_team)
                    s = Storage()
                    s.load(self.__storage_paths[int(bal_action)])
                    for i in range(len(s)):
                        self.__ba.add(selected_team, s.get(i))
                    print(f'\n"{self.__storage_paths[int(bal_action)].stem}" loaded into Team {selected_team}!')
                else:
                    print("\nCancelled.")

            elif ba_action == 1:

                # ----- BATTLE ASSEMBLY ADD -----

                spellcaster = self.create_or_load_spellcaster()
                self.__ba.add(selected_team, spellcaster)
                print(f"\n{spellcaster.name()} added to Team {selected_team}!")

            elif ba_action == 2:

                # ----- BATTLE ASSEMBLY INSERT -----
                spellcaster = self.create_or_load_spellcaster()
                print(str(self.__ba))
                print(f"\nWhere to place the spellcaster in Team {selected_team}? " +
                      "(Spellcasters in that location and on will be pushed forward.)")
                bai_action = input_valid_int(0, self.__ba.len(selected_team))
                self.__ba.insert(selected_team, bai_action, spellcaster)
                print(f"\n{spellcaster.name()} inserted into Team {selected_team}!")

            elif ba_action == 3:

                # ----- BATTLE ASSEMBLY REMOVE -----
                print(str(self.__ba))
                print(f"\nWhich spellcaster to remove from Team {selected_team}? Enter a number to remove, or anything else to cancel.")
                bar_action = input()
                if can_be_int(bar_action) and 0 <= int(bar_action) < self.__ba.len(selected_team):
                    removed_spellcaster = self.__ba.remove(selected_team, int(bar_action))
                    print(f"\n{removed_spellcaster.name()} removed from Team {selected_team}!")
                else:
                    print("\nCancelled.")

            elif ba_action == 4:

                # ----- BATTLE ASSEMBLY CLEAR -----
                print(f"\nWhich team to clear? Enter a number to clear, or anything else to cancel.")
                bac_action = input()
                if can_be_int(bac_action) and (int(bac_action) == 1 or int(bac_action) == 2):
                    self.__ba.clear(int(bac_action))
                    print(f"Team {bac_action} cleared!")
                else:
                    print("\nCancelled.")

            elif ba_action == 5:

                # ----- BATTLE ASSEMBLY MANA -----
                print()
                self.__ba.set_mana_per_round(input_valid_float(-inf, inf, False, False, "Mana per round: "))

            elif ba_action == 6:

                # ----- BATTLE ASSEMBLY PVP -----
                if self.__pvp:
                    self.__pvp = False
                    print("\nPVP is now off.")
                else:
                    self.__pvp = True
                    print("\nPVP is now on.")

            elif ba_action == 7:

                # ----- BATTLE ASSEMBLY FIRST TURN -----
                if self.__team_1_first:
                    self.__team_1_first = False
                    print("\nTeam 2 now starts first.")
                else:
                    self.__team_1_first = True
                    print("\nTeam 1 now starts first.")

            elif ba_action == 8:

                # ----- FIGHT! -----
                self.battle(self.__ba)

    def battle(self, battle_setup: Battle) -> None:
        """
        User I/O controller for conducting 1 or 2-player battle.
        :param battle_setup: A battle containing the lineup of spellcasters on each team.
        """
        b = copy.deepcopy(battle_setup)
        print("\n-*-*- BATTLE! -*-*-")
        winner = -1
        turn = 1 if self.__team_1_first else 2
        turn_result = ""
        while winner == -1:
            print()
            print(str(b))
            if turn_result != "":
                print(f"\n{turn_result}")
            if turn_result != "" and ((turn == 1 and self.__team_1_first) or (turn == 2 and not self.__team_1_first)):
                print("\nMana regenerated!")

            if turn == 1:
                # ----- PLAYER 1 TURN -----
                turn_result = self.battle_turn(b, 1)
                turn = 2
            elif turn == 2 and self.__pvp:
                # ----- PLAYER 2 TURN -----
                turn_result = self.battle_turn(b, 2)
                turn = 1
            else:
                # ----- TEAM 2 RANDOM TURN -----
                input("\nPress enter for Team 2 to take its turn.")
                turn_result = b.cast_random_spell(2)
                turn = 1

            winner = b.winner()
            if turn_result != "" and ((turn == 1 and self.__team_1_first) or (turn == 2 and not self.__team_1_first)):
                b.next_round()

        print("\n-*-*- BATTLE OVER! -*-*-")
        print()
        print(str(b))
        if turn_result != "":
            print(f"\n{turn_result}")
        print("\nBATTLE OVER!")
        print()

        if winner == 1:
            print(random_win_message(1, 2))
        elif winner == 2:
            print(random_win_message(2, 1))
        elif winner == 0 and b.len(1) == 0 and b.len(2) == 0:
            print("The battle was empty!")
        elif winner == 0:
            print(random_tie_message(1, 2))

        input("\nPress enter to finish.")

    def battle_turn(self, b: Battle, team: int) -> str:
        """
        User I/O controller for taking a turn to cast a spell in battle.
        :param b: A battle in progress.
        :param team: The team/player taking the turn (1 or 2).
        :return: A message stating the caster, the spell cast, and who the spell killed.
        """
        result = ""
        while result == "":
            print(f"\nPlayer {team}, choose a spellcaster." if self.__pvp else "\nChoose a spellcaster.")
            alive_indexes = b.alive_indexes(team)
            for i in range(len(alive_indexes)):
                print(f"{i}: {b.get_name(team, alive_indexes[i])}")
            print(f"{len(alive_indexes)}: Skip turn")

            ai_choice = input_valid_int(0, len(alive_indexes))
            if ai_choice == len(alive_indexes):
                result = f"Team {team} did absolutely nothing!"
            else:
                caster = alive_indexes[ai_choice]

                print(f"\nChoose a spell for {b.get_name(team, caster)} to cast.")
                spells = b.get_spells(team, caster)
                castable_spells = b.get_castable_spells(team, caster)
                for i in range(len(spells)):
                    print((f"{i}: " if spells[i] in castable_spells else f"Not enough mana: ") + f"{str(spells[i])}")
                print(f"{len(spells)}: Back")

                spell = input_valid_int(0, len(spells))
                while spell != len(spells) and spells[spell] not in castable_spells:
                    print(f"{b.get_name(team, caster)} does not have enough mana for that spell. Choose a different spell.")
                    spell = input_valid_int(0, len(spells))

                if spell != len(spells):
                    print("\nChoose a team and spellcaster to target.")
                    target_team = input_valid_int(1, 2, True, True, "Team: ")
                    target_caster = input_valid_int(0, b.len(target_team) - 1, True, True, "Target: ")

                    dead_list = b.cast_spell(team, caster, spells[spell], target_team, target_caster)
                    if len(dead_list) == 0:
                        result = f"{b.get_name(team, caster)} casts {spells[spell].name()}!\nThe battle continues."
                    else:
                        result = (f"{b.get_name(team, caster)} casts {spells[spell].name()}!\n" +
                                  f"{b.get_name(team, caster)} killed {written_list(dead_list)}!")
                    input(f"\nPress enter to cast {spells[spell].name()}!")
        return result