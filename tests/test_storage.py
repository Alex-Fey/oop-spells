from pathlib import Path
from unittest import TestCase

from oop_spells.spellcaster import Spellcaster
from oop_spells.spells import *
from oop_spells.storage import Storage, delete_csv_file


class TestStorage(TestCase):
    def test_add(self):
        s = Storage()
        s.add(Spellcaster("Xela", [MagicMissile(), Fireball(), LightningBolt()], 100, 100, 1))
        s.add(Spellcaster("Muggle", [], 1, 1, 0))
        s.add(Spellcaster("", [BlindingFlash()], 1000, 1000, 10))
        self.assertEqual(len(s), 3)
        self.assertEqual(str(s), "0 - Xela [HP: 100, MP: 100, DMG: 1]: Magic Missile, Fireball, Lightning Bolt\n" +
                                 "1 - Muggle [HP: 1, MP: 1, DMG: 0]: \n" +
                                 "2 -  [HP: 1000, MP: 1000, DMG: 10]: Blinding Flash")

    def test_get(self):
        s = Storage()
        m = Spellcaster("Muggle", [], 1, 1, 0)
        s.add(Spellcaster("Xela", [MagicMissile(), Fireball(), LightningBolt()], 100, 100, 1))
        s.add(m)
        s.add(Spellcaster("", [BlindingFlash()], 1000, 1000, 10))
        self.assertEqual(s.get(1), m)

    def test_insert(self):
        s = Storage()
        s.add(Spellcaster("Xela", [MagicMissile(), Fireball(), LightningBolt()], 100, 100, 1))
        s.add(Spellcaster("Muggle", [], 1, 1, 0))
        s.add(Spellcaster("", [BlindingFlash()], 1000, 1000, 10))
        s.insert(1, Spellcaster("Middle, Man", [Fireball(), BlindingFlash(), Earthquake()], 100, 150, 0.8))
        self.assertEqual(str(s), "0 - Xela [HP: 100, MP: 100, DMG: 1]: Magic Missile, Fireball, Lightning Bolt\n" +
                                 "1 - Middle, Man [HP: 100, MP: 150, DMG: 0.8]: Fireball, Blinding Flash, Earthquake\n" +
                                 "2 - Muggle [HP: 1, MP: 1, DMG: 0]: \n" +
                                 "3 -  [HP: 1000, MP: 1000, DMG: 10]: Blinding Flash")

    def test_remove(self):
        s = Storage()
        s.add(Spellcaster("Xela", [MagicMissile(), Fireball(), LightningBolt()], 100, 100, 1))
        mm = Spellcaster("Middle, Man", [Fireball(), BlindingFlash(), Earthquake()], 100, 150, 0.8)
        s.add(mm)
        s.add(Spellcaster("Muggle", [], 1, 1, 0))
        s.add(Spellcaster("", [BlindingFlash()], 1000, 1000, 10))
        self.assertEqual(s.remove(1), mm)
        self.assertEqual(s.remove(100), None)
        self.assertEqual(str(s), "0 - Xela [HP: 100, MP: 100, DMG: 1]: Magic Missile, Fireball, Lightning Bolt\n" +
                         "1 - Muggle [HP: 1, MP: 1, DMG: 0]: \n" +
                         "2 -  [HP: 1000, MP: 1000, DMG: 10]: Blinding Flash")

    def test_save_and_load(self):
        s1 = Storage()
        s1.add(Spellcaster("Xela", [MagicMissile(), Fireball(), LightningBolt()], 100, 100, 1))
        s1.add(Spellcaster("Middle, Man", [Fireball(), BlindingFlash(), Earthquake()], 100, 150, 0.8))
        s1.add(Spellcaster("Muggle", [], 1, 1, 0))
        s1.add(Spellcaster("", [BlindingFlash()], 1000, 1000, 10))

        script_directory = Path(__file__).parent
        file_path = script_directory / "test_storage.csv"
        s1.save(file_path)

        s2 = Storage()
        s2.load(file_path)
        self.assertEqual(str(s1), str(s2))

class TestDeleteCSVFile(TestCase):
    def test_delete_csv_file(self):
        script_directory = Path(__file__).parent
        file_path_1 = script_directory / "delete_this_1.csv"
        file_path_2 = script_directory / "delete_this_2.csv"
        file_path_3 = script_directory / "delete_this_3.csv"

        s = Storage()
        s.save(file_path_1)
        s.save(file_path_2)
        s.save(file_path_3)

        if not (delete_csv_file(file_path_1) and delete_csv_file(file_path_2) and delete_csv_file(file_path_3)):
            self.fail()