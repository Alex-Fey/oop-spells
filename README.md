# <img src="icon/oop_spells_icon.png" alt="Sample" height="40"> Object-Oriented Programming (OOP) Spells

Object-Oriented Programming (OOP Spells) is a small console-based battle game made to practice object-oriented
programming in Python. It allows you to assemble two teams of spellcasters (objects with a name, health, mana, a damage
modifier, and a list of spells) and battle them!

## Installation

> Just download `OOP Spells.exe`!<br>
> Note: this program is only guaranteed to work on Windows.

All spellcaster storage data is automatically saved in `AppData/Roaming`.

## Getting Started

1. Run `OOP Spells.exe`. You should see the main menu.


### Creating Spellcaster Storage Files

2. Type `1` and press `Enter` to access the storage menu.
3. Enter `0` to create a new storage file for Team 1.
4. Enter the name of the file (such as `Team 1`) and follow the instructions to create a spellcaster.

> A typical spellcaster has 100 health, 100 mana, a damage multiplier of 1, and a few spells.

5. If you want to add more spellcasters, enter `1` to access your Team 1 file and edit it.
6. Repeat steps 3-5 to create a storage file for Team 2.
7. Go back to the main menu.

### Assembling a Battle

8. Enter `0` to start assembling a battle.
9. Enter `0` again to load a storage file into a team.
10. Enter `1` for the `Team:` field and choose the Team 1 storage file you created earlier.
11. Repeat steps 9-10 for Team 2.
12. Enter `8` to fight!

## Snippets

### Main Menu

```
| -------------------- |
|      OOP Spells      |
|                      |
| 0: Assemble battle   |
| 1: Access storage    |
| 2: Exit              |
|                      |
| Enter a number.      |
| -------------------- |
```

### Storage Editing

```
----- Test Team 1 -----

Contents of "Test Team 1":
0 - Xela [HP: 100, MP: 100, DMG: 1]: Magic Missile, Fireball, Lightning Bolt
1 - Xela the Wise [HP: 80, MP: 150, DMG: 1.5]: Blinding Flash, Heal
2 - Xela the Ruthless [HP: 150, MP: 90, DMG: 1.5]: Fireball, Earthquake

Select an option.
0: Add a spellcaster
1: Insert a spellcaster
2: Remove a spellcaster
3: Delete this storage
4: Exit without saving
5: Save and exit
```

### Battle

```
| ------ Team 1 ------ | ------ Team 2 ------ |
| [0] Xela             | [0] The Missler      |
| HP: 92%              | HP: 96%              |
| MP: 65%              | MP: 100%             |
|                      |                      |
| [1] Xela the Wise    | [1] Mr. Mage         |
| HP: 70%              | HP: 88%              |
| MP: 100%             | MP: 100%             |
|                      |                      |
| [2] Xela the Ruthles | [2] Vance            |
| HP: 73%              | HP: 60%              |
| MP: 100%             | MP: 82%              |
|                      |                      |
|                      | [3] Cleric Onsonlony |
|                      | HP: 88%              |
|                      | MP: 100%             |
| -------------------- | -------------------- |

Vance casts Fireball!
The battle continues.

Mana regenerated!

Choose a spellcaster.
0: Xela
1: Xela the Wise
2: Xela the Ruthless
3: Skip turn
2

Choose a spell for Xela the Ruthless to cast.
0: Fireball       - Shoot a concentrated ball of fire which explodes for 20, 12, and 4 damage depending on distance from the blast (40 mana).
1: Earthquake     - Rumble the ground beneath the targeted team's feet, dealing 20 damage to members with an odd location and no damage to members with an even location (50 mana).
2: Back
0

Choose a team and spellcaster to target.
Team: 2
Target: 1

Press enter to cast Fireball!
```

## Clarification for Files in `oop_spells`

Object-oriented data and logic files:
- `battle.py`
- `spellcaster.py`
- `spells.py`
- `storage.py`

User I/O, helper, and logistics files:
- `__init__.py`
- `__main__.py`
- `helpers.py` (required for `battle.py`)
- `oop_spells_io.py`

## License

[MIT](https://choosealicense.com/licenses/mit/)