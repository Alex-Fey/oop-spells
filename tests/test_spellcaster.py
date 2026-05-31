from unittest import TestCase

from oop_spells.spellcaster import *
from oop_spells.spells import *


class TestSpellcaster(TestCase):
    def test_str_methods(self):
        sp = Spellcaster("Xela", [MagicMissile(), Fireball(), LightningBolt()])
        self.assertEqual(sp.name(), "Xela")
        self.assertEqual(sp.health_str(), "HP: 100%")
        self.assertEqual(sp.mana_str(), "MP: 100%")
        self.assertEqual(str(sp), "Xela [HP: 100, MP: 100, DMG: 1]: Magic Missile, Fireball, Lightning Bolt")

    def test_spells(self):
        sp = Spellcaster("Xela", [MagicMissile(), Fireball(), LightningBolt()], 100, 30, 1)
        self.assertEqual(sp.spells(), [MagicMissile(), Fireball(), LightningBolt()])
        self.assertEqual(sp.castable_spells(), [MagicMissile(), LightningBolt()])
        sp.take_damage(100)
        self.assertEqual(sp.castable_spells(), [])

    def test_take_damage(self):
        sp = Spellcaster("Xela", [], 100, 100, 1)
        self.assertEqual(sp.health_percentage(), 1)
        self.assertFalse(sp.take_damage(60))
        self.assertEqual(sp.health_percentage(), 0.4)
        self.assertEqual(sp.health_str(), "HP: 40%")
        self.assertTrue(sp.take_damage(60))
        self.assertEqual(sp.health_percentage(), 0)
        self.assertEqual(sp.mana_percentage(), 0)

    def test_cast_spell_success(self):
        sp = Spellcaster("Xela", [MagicMissile(), Fireball(), LightningBolt()], 100, 100, 1)
        self.assertEqual(sp.mana_percentage(), 1)
        sp.cast_spell(Fireball())
        self.assertEqual(sp.mana_percentage(), 0.6)
        self.assertEqual(sp.mana_str(), "MP: 60%")
        sp.cast_spell(LightningBolt())
        self.assertEqual(sp.mana_percentage(), 0.3)

    def test_cast_spell_unknown_error(self):
        sp = Spellcaster("Xela", [MagicMissile(), Fireball(), LightningBolt()], 100, 100, 1)
        sp.cast_spell(Fireball())
        with self.assertRaises(UnknownSpellError):
            sp.cast_spell(BlindingFlash())
        self.assertEqual(sp.mana_percentage(), 0.6)

    def test_cast_spell_mana_error(self):
        sp = Spellcaster("Xela", [MagicMissile(), Fireball(), LightningBolt()], 100, 100, 1)
        sp.cast_spell(Fireball())
        sp.cast_spell(LightningBolt())
        self.assertEqual(sp.mana_percentage(), 0.3)
        with self.assertRaises(NotEnoughManaError):
            sp.cast_spell(Fireball())
        self.assertEqual(sp.mana_percentage(), 0.3)

    def test_cast_spell_dead_error(self):
        sp = Spellcaster("Xela", [MagicMissile(), Fireball(), LightningBolt()], 100, 100, 1)
        sp.take_damage(100)
        with self.assertRaises(DeadError):
            sp.cast_spell(Fireball())
        self.assertEqual(sp.mana_percentage(), 0)

    def test_regen_mana(self):
        sp = Spellcaster("Xela", [Fireball()], 100, 100, 1)
        sp.cast_spell(Fireball())
        sp.regen_mana(20)
        self.assertEqual(sp.mana_percentage(), 0.8)
        sp.regen_mana(100)
        self.assertEqual(sp.mana_percentage(), 1)