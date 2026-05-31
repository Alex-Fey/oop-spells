from unittest import TestCase

from oop_spells.battle import Battle
from oop_spells.spellcaster import *
from oop_spells.spells import *


class TestBattle(TestCase):
    def test_battle_creation(self):
        xa = Spellcaster("Xela's Evil Twin", [MagicMissile(), Fireball(), LightningBolt()], 100, 100, 1)

        b = Battle([Spellcaster("Xela", [MagicMissile(), Fireball(), LightningBolt()], 100, 100, 1),
                    Spellcaster("Xela the Wise", [BlindingFlash(), Heal()], 60, 150, 1)],
                   [xa,
                    Spellcaster("The Missler", [MagicMissile()], 100, 100, 3),
                    Spellcaster("Vance", [Fireball()], 50, 200, 2),
                    Spellcaster("Cleric Onsonlonyaloongyulo", [Heal()], 100, 100, 1)])

        b.add(1, Spellcaster("Xela the Ruthless", [Fireball(), Earthquake()], 150, 90, 1.5))
        self.assertEqual(b.remove(2, 0), xa)
        b.insert(2, 1, Spellcaster("Mr. Mage", [Heal(), Earthquake(), BlindingFlash(), LightningBolt(), Fireball(), MagicMissile()], 100, 100, 1))

        print(str(b))

        self.assertEqual(str(b), "" +
                         "| ------ Team 1 ------ | ------ Team 2 ------ |\n" +
                         "| [0] Xela             | [0] The Missler      |\n" +
                         "| HP: 100%             | HP: 100%             |\n" +
                         "| MP: 100%             | MP: 100%             |\n" +
                         "|                      |                      |\n" +
                         "| [1] Xela the Wise    | [1] Mr. Mage         |\n" +
                         "| HP: 100%             | HP: 100%             |\n" +
                         "| MP: 100%             | MP: 100%             |\n" +
                         "|                      |                      |\n" +
                         "| [2] Xela the Ruthles | [2] Vance            |\n" +
                         "| HP: 100%             | HP: 100%             |\n" +
                         "| MP: 100%             | MP: 100%             |\n" +
                         "|                      |                      |\n" +
                         "|                      | [3] Cleric Onsonlony |\n" +
                         "|                      | HP: 100%             |\n" +
                         "|                      | MP: 100%             |\n" +
                         "| -------------------- | -------------------- |")

    def test_battle_query(self):
        b = Battle([Spellcaster("Xela", [MagicMissile(), Fireball(), LightningBolt()], 100, 100, 1),
                    Spellcaster("Xela the Wise", [BlindingFlash(), Heal()], 60, 150, 1),
                    Spellcaster("Xela the Ruthless", [Fireball(), Earthquake()], 150, 90, 1.5)],
                   [Spellcaster("The Missler", [MagicMissile()], 100, 100, 3),
                    Spellcaster("PROTO Mr. Mage", [Heal(), Earthquake(), BlindingFlash(), LightningBolt(), Fireball(), MagicMissile()], 30, 30, 0.3),
                    Spellcaster("Vance", [Fireball()], 50, 200, 2),
                    Spellcaster("Cleric Onsonlonyaloongyulo", [Heal()], 100, 100, 1)])

        self.assertEqual(b.alive_indexes(1), [0, 1, 2])
        self.assertEqual(b.alive_indexes(2), [0, 1, 2, 3])

        self.assertEqual(b.get_name(1, 1), "Xela the Wise")
        self.assertEqual(b.get_name(2, 3), "Cleric Onsonlonyaloongyulo")
        self.assertEqual(b.get_name(1, 3), "")

        self.assertEqual(b.get_spells(2, 1), [Heal(), Earthquake(), BlindingFlash(), LightningBolt(), Fireball(), MagicMissile()])
        self.assertEqual(b.get_castable_spells(2, 1), [LightningBolt(), MagicMissile()])

        self.assertEqual(b.len(1), 3)
        self.assertEqual(b.len(2), 4)
        self.assertEqual(b.len(3), 0)

        self.assertEqual(b.mana_per_round(), 5)
        b.set_mana_per_round(9.9)
        self.assertEqual(b.mana_per_round(), 9.9)

        b.clear(1)
        b.clear(2)
        self.assertEqual(str(b), "" +
                         "| ------ Team 1 ------ | ------ Team 2 ------ |\n" +
                         "| -------------------- | -------------------- |")

    def test_battle_cast_spell(self):
        b = Battle([Spellcaster("Xela", [MagicMissile(), Fireball(), LightningBolt()], 100, 100, 1),
                    Spellcaster("Xela the Wise", [BlindingFlash(), Heal()], 60, 150, 1),
                    Spellcaster("Xela the Ruthless", [Fireball(), Earthquake()], 150, 90, 1.5)],
                   [Spellcaster("The Missler", [MagicMissile()], 100, 100, 3),
                    Spellcaster("Mr. Mage", [Heal(), Earthquake(), BlindingFlash(), LightningBolt(), Fireball(), MagicMissile()], 100, 100, 1),
                    Spellcaster("Vance", [Fireball()], 50, 200, 2),
                    Spellcaster("Cleric Onsonlonyaloongyulo", [Heal()], 100, 100, 1)])

        b.cast_spell(1, 0, Fireball(), 2, 1)

        self.assertEqual(str(b), "" +
                         "| ------ Team 1 ------ | ------ Team 2 ------ |\n" +
                         "| [0] Xela             | [0] The Missler      |\n" +
                         "| HP: 100%             | HP: 88%              |\n" +
                         "| MP: 60%              | MP: 100%             |\n" +
                         "|                      |                      |\n" +
                         "| [1] Xela the Wise    | [1] Mr. Mage         |\n" +
                         "| HP: 100%             | HP: 80%              |\n" +
                         "| MP: 100%             | MP: 100%             |\n" +
                         "|                      |                      |\n" +
                         "| [2] Xela the Ruthles | [2] Vance            |\n" +
                         "| HP: 100%             | HP: 76%              |\n" +
                         "| MP: 100%             | MP: 100%             |\n" +
                         "|                      |                      |\n" +
                         "|                      | [3] Cleric Onsonlony |\n" +
                         "|                      | HP: 96%              |\n" +
                         "|                      | MP: 100%             |\n" +
                         "| -------------------- | -------------------- |")

    def test_battle_cast_spell_unknown_error(self):
        b = Battle([Spellcaster("Xela", [MagicMissile(), Fireball(), LightningBolt()], 100, 100, 1),
                    Spellcaster("Xela the Wise", [BlindingFlash(), Heal()], 60, 150, 1),
                    Spellcaster("Xela the Ruthless", [Fireball(), Earthquake()], 150, 90, 1.5)],
                   [Spellcaster("The Missler", [MagicMissile()], 100, 100, 3),
                    Spellcaster("Mr. Mage", [Heal(), Earthquake(), BlindingFlash(), LightningBolt(), Fireball(), MagicMissile()], 100, 100, 1),
                    Spellcaster("Vance", [Fireball()], 50, 200, 2),
                    Spellcaster("Cleric Onsonlonyaloongyulo", [Heal()], 100, 100, 1)])

        with self.assertRaises(UnknownSpellError):
            b.cast_spell(1, 0, BlindingFlash(), 2, 1)

    def test_battle_cast_spell_mana_error(self):
        b = Battle([Spellcaster("Xela", [MagicMissile(), Fireball(), LightningBolt()], 100, 100, 1),
                    Spellcaster("Xela the Wise", [BlindingFlash(), Heal()], 60, 150, 1),
                    Spellcaster("Xela the Ruthless", [Fireball(), Earthquake()], 150, 90, 1.5)],
                   [Spellcaster("The Missler", [MagicMissile()], 100, 100, 3),
                    Spellcaster("Mr. Mage", [Heal(), Earthquake(), BlindingFlash(), LightningBolt(), Fireball(), MagicMissile()], 100, 100, 1),
                    Spellcaster("Vance", [Fireball()], 50, 200, 2),
                    Spellcaster("Cleric Onsonlonyaloongyulo", [Heal()], 100, 100, 1)])

        b.cast_spell(1, 0, Fireball(), 2, 1)
        b.cast_spell(1, 0, Fireball(), 2, 1)

        with self.assertRaises(NotEnoughManaError):
            b.cast_spell(1, 0, Fireball(), 2, 1)

    def test_battle_cast_spell_dead_error(self):
        b = Battle([Spellcaster("Xela", [MagicMissile(), Fireball(), LightningBolt()], 100, 100, 1),
                    Spellcaster("Xela the Wise", [BlindingFlash(), Heal()], 60, 150, 1),
                    Spellcaster("Xela the Ruthless", [Fireball(), Earthquake()], 150, 90, 1.5)],
                   [Spellcaster("The Missler", [MagicMissile()], 100, 100, 3),
                    Spellcaster("Mr. Mage", [Heal(), Earthquake(), BlindingFlash(), LightningBolt(), Fireball(), MagicMissile()], 100, 100, 1),
                    Spellcaster("Vance", [Fireball()], 50, 200, 2),
                    Spellcaster("Cleric Onsonlonyaloongyulo", [Heal()], 100, 100, 1)])

        b.cast_spell(1, 0, LightningBolt(), 2, 2)
        b.cast_spell(1, 1, BlindingFlash(), 2, 2)
        self.assertEqual(b.cast_spell(1, 2, Fireball(), 2, 2), ["Vance"]) # Fireball kills Vance

        with self.assertRaises(DeadError):
            b.cast_spell(2, 2, Fireball(), 1, 1)
        self.assertEqual(b.alive_indexes(2), [0, 1, 3])

    def test_battle_round_1(self):
        b = Battle([Spellcaster("Xela", [MagicMissile(), Fireball(), LightningBolt()], 100, 100, 1),
                    Spellcaster("Xela the Wise", [BlindingFlash(), Heal()], 60, 150, 1),
                    Spellcaster("Xela the Ruthless", [Fireball(), Earthquake()], 150, 90, 1.5)],
                   [Spellcaster("The Missler", [MagicMissile()], 100, 100, 3),
                    Spellcaster("Mr. Mage", [Heal(), Earthquake(), BlindingFlash(), LightningBolt(), Fireball(), MagicMissile()], 100, 100, 1),
                    Spellcaster("Vance", [Fireball()], 50, 200, 2),
                    Spellcaster("Cleric Onsonlonyaloongyulo", [Heal()], 100, 100, 1)],
                   10)

        # Team 1
        b.cast_spell(1, 0, LightningBolt(), 2, 1)
        b.cast_spell(1, 1, BlindingFlash(), 2, 1)
        b.cast_spell(1, 2, Fireball(), 2, 1)
        self.assertEqual(str(b), "" +
                         "| ------ Team 1 ------ | ------ Team 2 ------ |\n" +
                         "| [0] Xela             | [0] The Missler      |\n" +
                         "| HP: 100%             | HP: 74%              |\n" +
                         "| MP: 70%              | MP: 100%             |\n" +
                         "|                      |                      |\n" +
                         "| [1] Xela the Wise    | [1] Mr. Mage         |\n" +
                         "| HP: 100%             | HP: 36%              |\n" +
                         "| MP: 73%              | MP: 100%             |\n" +
                         "|                      |                      |\n" +
                         "| [2] Xela the Ruthles | [2] Vance            |\n" +
                         "| HP: 100%             | HP: 32%              |\n" +
                         "| MP: 55%              | MP: 100%             |\n" +
                         "|                      |                      |\n" +
                         "|                      | [3] Cleric Onsonlony |\n" +
                         "|                      | HP: 78%              |\n" +
                         "|                      | MP: 100%             |\n" +
                         "| -------------------- | -------------------- |")

        # Team 2
        b.cast_spell(2, 0, MagicMissile(), 1, 1)
        b.cast_spell(2, 1, Heal(), 2, 1)
        b.cast_spell(2, 2, Fireball(), 1, 0)
        b.cast_spell(2, 3, Heal(), 2, 2)
        self.assertEqual(str(b), "" +
                         "| ------ Team 1 ------ | ------ Team 2 ------ |\n" +
                         "| [0] Xela             | [0] The Missler      |\n" +
                         "| HP: 60%              | HP: 74%              |\n" +
                         "| MP: 70%              | MP: 80%              |\n" +
                         "|                      |                      |\n" +
                         "| [1] Xela the Wise    | [1] Mr. Mage         |\n" +
                         "| HP: 0%               | HP: 66%              |\n" +
                         "| MP: 0%               | MP: 50%              |\n" +
                         "|                      |                      |\n" +
                         "| [2] Xela the Ruthles | [2] Vance            |\n" +
                         "| HP: 94%              | HP: 92%              |\n" +
                         "| MP: 55%              | MP: 80%              |\n" +
                         "|                      |                      |\n" +
                         "|                      | [3] Cleric Onsonlony |\n" +
                         "|                      | HP: 78%              |\n" +
                         "|                      | MP: 50%              |\n" +
                         "| -------------------- | -------------------- |")

        # Round end
        b.next_round()
        self.assertEqual(str(b), "" +
                         "| ------ Team 1 ------ | ------ Team 2 ------ |\n" +
                         "| [0] Xela             | [0] The Missler      |\n" +
                         "| HP: 60%              | HP: 74%              |\n" +
                         "| MP: 80%              | MP: 90%              |\n" +
                         "|                      |                      |\n" +
                         "| [1] Xela the Wise    | [1] Mr. Mage         |\n" +
                         "| HP: 0%               | HP: 66%              |\n" +
                         "| MP: 0%               | MP: 60%              |\n" +
                         "|                      |                      |\n" +
                         "| [2] Xela the Ruthles | [2] Vance            |\n" +
                         "| HP: 94%              | HP: 92%              |\n" +
                         "| MP: 66%              | MP: 85%              |\n" +
                         "|                      |                      |\n" +
                         "|                      | [3] Cleric Onsonlony |\n" +
                         "|                      | HP: 78%              |\n" +
                         "|                      | MP: 60%              |\n" +
                         "| -------------------- | -------------------- |")
        self.assertEqual(b.winner(), -1)
        self.assertEqual(b.alive_indexes(1), [0, 2])

    def test_battle_team_1_wins(self):
        b = Battle([Spellcaster("Xela", [MagicMissile(), Fireball(), LightningBolt()], 100, 100, 1),
                    Spellcaster("Xela the Wise", [BlindingFlash(), Heal()], 60, 150, 1),
                    Spellcaster("EXO Xela the Ruthless", [Fireball(), Earthquake()], 1500, 900, 15)],
                   [Spellcaster("The Missler", [MagicMissile()], 100, 100, 3),
                    Spellcaster("Mr. Mage", [Heal(), Earthquake(), BlindingFlash(), LightningBolt(), Fireball(), MagicMissile()], 100, 100, 1),
                    Spellcaster("Vance", [Fireball()], 50, 200, 2),
                    Spellcaster("Cleric Onsonlonyaloongyulo", [Heal()], 100, 100, 1)])

        b.cast_spell(1, 2, Fireball(), 2, 1)
        b.cast_spell(1, 2, Earthquake(), 2, 3)
        self.assertEqual(b.winner(), 1)

    def test_battle_team_2_wins(self):
        b = Battle([Spellcaster("Xela", [MagicMissile(), Fireball(), LightningBolt()], 100, 100, 1),
                    Spellcaster("Xela the Wise", [BlindingFlash(), Heal()], 60, 150, 1),
                    Spellcaster("Xela the Ruthless", [Fireball(), Earthquake()], 150, 90, 1.5)],
                   [Spellcaster("EXO The Missler", [MagicMissile()], 1000, 1000, 30),
                    Spellcaster("Mr. Mage", [Heal(), Earthquake(), BlindingFlash(), LightningBolt(), Fireball(), MagicMissile()], 100, 100, 1),
                    Spellcaster("Vance", [Fireball()], 50, 200, 2),
                    Spellcaster("Cleric Onsonlonyaloongyulo", [Heal()], 100, 100, 1)])

        b.cast_spell(2, 0, MagicMissile(), 1, 0)
        b.cast_spell(2, 0, MagicMissile(), 1, 1)
        b.cast_spell(2, 0, MagicMissile(), 1, 2)
        self.assertEqual(b.winner(), 2)

    def test_battle_tie(self):
        b = Battle([Spellcaster("Xela", [MagicMissile(), Fireball(), LightningBolt()], 100, 100, 1),
                    Spellcaster("Xela the Wise", [BlindingFlash(), Heal()], 60, 150, 1),
                    Spellcaster("EXO Xela the Ruthless", [Fireball(), Earthquake()], 1500, 900, 15)],
                   [Spellcaster("The Missler", [MagicMissile()], 100, 100, 3),
                    Spellcaster("Mr. Mage", [Heal(), Earthquake(), BlindingFlash(), LightningBolt(), Fireball(), MagicMissile()], 100, 100, 1),
                    Spellcaster("Vance", [Fireball()], 50, 200, 2),
                    Spellcaster("Cleric Onsonlonyaloongyulo", [Heal()], 100, 100, 1)])

        b.cast_spell(1, 2, Fireball(), 2, 0)
        b.cast_spell(1, 2, Fireball(), 2, 4)
        b.cast_spell(1, 2, Fireball(), 1, 1)
        b.cast_spell(1, 2, Fireball(), 1, 2)
        b.cast_spell(1, 2, Fireball(), 1, 2)
        b.cast_spell(1, 2, Fireball(), 1, 2)
        b.cast_spell(1, 2, Fireball(), 1, 2)
        b.cast_spell(1, 2, Fireball(), 1, 2)
        self.assertEqual(b.winner(), 0)