from abc import ABC, abstractmethod
from typing import Optional


class Spell(ABC): # ABC means Abstract Base Class
    """
    Abstract class for castable spells.
    """
    @abstractmethod
    def mana_cost(self) -> float:
        """
        :return: Mana cost for casting the spell.
        """
        pass

    @abstractmethod
    def damage(self, location: int, target: int) -> float:
        """
        Calculates the damage the spell deals to a spellcaster at a given location in a battle team.
        :param location: Location (list index) being queried.
        :param target: Location (list index) the spell is being targeted at.
        :return: Damage the spell deals to the spellcaster at that location.
        """
        pass

    @abstractmethod
    def __str__(self) -> str:
        """
        :return: The name and description of the spell.
        """
        pass

    @abstractmethod
    def name(self) -> str:
        """
        :return: The description of the spell.
        """
        pass

    @abstractmethod
    def desc(self) -> str:
        """
        :return: The description of the spell.
        """
        pass

    # Overriding ==
    def __eq__(self, other) -> bool:
        return isinstance(other, self.__class__)

    # Overriding !=
    def __ne__(self, other) -> bool:
        return not isinstance(other, self.__class__)

class MagicMissile(Spell):
    """
    Send a small burst of mana into a single target, dealing 20 damage (20 mana).
    """
    def __str__(self):
        return f"Magic Missile  - {self.desc()}"

    def name(self):
        return "Magic Missile"

    def desc(self):
        return "Send a small burst of mana into a single target, dealing 20 damage (20 mana)."

    def mana_cost(self) -> float:
        return 20

    def damage(self, location: int, target: int) -> float:
        if location == target:
            return 20
        else:
            return 0

class Fireball(Spell):
    """
    Shoot a concentrated ball of fire which explodes for 20, 12, and 4 damage depending on distance from the blast (40 mana).
    """
    def __str__(self):
        return f"Fireball       - {self.desc()}"

    def name(self):
        return "Fireball"

    def desc(self):
        return "Shoot a concentrated ball of fire which explodes for 20, 12, and 4 damage depending on distance from the blast (40 mana)."

    def mana_cost(self) -> float:
        return 40

    def damage(self, location: int, target: int) -> float:
        return max(-8 * abs(location - target) + 20, 0)

class LightningBolt(Spell):
    """
    Shoot a bolt of lightning into a single target, dealing 26 damage and arcing into the next two targets of greater location for 8 damage (30 mana).
    """
    def __str__(self):
        return f"Lightning Bolt - {self.desc()}"

    def name(self):
        return "Lightning Bolt"

    def desc(self):
        return "Shoot a bolt of lightning into a single target, dealing 26 damage and arcing into the next two targets of greater location for 8 damage (30 mana)."

    def mana_cost(self) -> float:
        return 30

    def damage(self, location: int, target: int) -> float:
        if location == target:
            return 26
        elif 0 < location - target <= 2:
            return 8
        else:
            return 0

class BlindingFlash(Spell):
    """
    Emit a burst of light which deals 8 damage to all members on the targeted team (40 mana).
    """
    def __str__(self):
        return f"Blinding Flash - {self.desc()}"

    def name(self):
        return "Blinding Flash"

    def desc(self):
        return "Emit a burst of light which deals 8 damage to all members on the targeted team (40 mana)."

    def mana_cost(self) -> float:
        return 40

    def damage(self, location: int, target: int) -> float:
        return 8

class Earthquake(Spell):
    """
    Rumble the ground beneath the targeted team's feet, dealing 20 damage to members with an odd location and no damage to members with an even location (50 mana).
    """
    def __str__(self):
        return f"Earthquake     - {self.desc()}"

    def name(self):
        return "Earthquake"

    def desc(self):
        return "Rumble the ground beneath the targeted team's feet, dealing 20 damage to members with an odd location and no damage to members with an even location (50 mana)."

    def mana_cost(self) -> float:
        return 50

    def damage(self, location: int, target: int) -> float:
        if location % 2 == 0:
            return 0
        else:
            return 20

class Heal(Spell):
    """
    Convert mana into life force to heal a specified target for 30 health (60 mana).
    """
    def __str__(self):
        return f"Heal           - {self.desc()}"

    def name(self):
        return "Heal"

    def desc(self):
        return "Convert mana into life force to heal a specified target for 30 health (60 mana)."

    def mana_cost(self) -> float:
        return 50

    def damage(self, location: int, target: int) -> float:
        if location == target:
            return -30
        else:
            return 0

def name_to_spell(string: str) -> Optional[Spell]:
    """
    Converts from a spell's name() result to a Spell object.
    :param string: Name of the spell.
    :return: Spell object.
    """
    match string:
        case "Magic Missile":
            return MagicMissile()
        case "Fireball":
            return Fireball()
        case "Lightning Bolt":
            return LightningBolt()
        case "Blinding Flash":
            return BlindingFlash()
        case "Earthquake":
            return Earthquake()
        case "Heal":
            return Heal()
    return None

def str_to_spell(string: str) -> Optional[Spell]:
    """
    Converts from a spell's str() result to a Spell object.
    :param string: String representation of the spell.
    :return: Spell object.
    """
    match string:
        case "Magic Missile  - Send a small burst of mana into a single target, dealing 20 damage (20 mana).":
            return MagicMissile()
        case "Fireball       - Shoot a concentrated ball of fire which explodes for 20, 12, and 4 damage depending on distance from the blast (40 mana).":
            return Fireball()
        case "Lightning Bolt - Shoot a bolt of lightning into a single target, dealing 26 damage and arcing into the next two targets of greater location for 8 damage (30 mana).":
            return LightningBolt()
        case "Blinding Flash - Emit a burst of light which deals 8 damage to all members on the targeted team (40 mana).":
            return BlindingFlash()
        case "Earthquake     - Rumble the ground beneath the targeted team's feet, dealing 20 damage to members with an odd location and no damage to members with an even location (50 mana).":
            return Earthquake()
        case "Heal           - Convert mana into life force to heal a specified target for 30 health (60 mana).":
            return Heal()
    return None