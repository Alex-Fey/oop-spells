from unittest import TestCase

from oop_spells.spells import *


class TestMagicMissile(TestCase):
    def test_mana_cost(self):
        mm = MagicMissile()
        self.assertEqual(mm.mana_cost(), 20)

    def test_damage(self):
        mm = MagicMissile()
        self.assertEqual(mm.damage(0, 2), 0)
        self.assertEqual(mm.damage(1, 2), 0)
        self.assertEqual(mm.damage(2, 2), 20)
        self.assertEqual(mm.damage(3, 2), 0)
        self.assertEqual(mm.damage(4, 2), 0)

class TestFireball(TestCase):
    def test_mana_cost(self):
        fb = Fireball()
        self.assertEqual(fb.mana_cost(), 40)

    def test_damage(self):
        fb = Fireball()
        self.assertEqual(fb.damage(0, 3), 0)
        self.assertEqual(fb.damage(1, 3), 4)
        self.assertEqual(fb.damage(2, 3), 12)
        self.assertEqual(fb.damage(3, 3), 20)
        self.assertEqual(fb.damage(4, 3), 12)
        self.assertEqual(fb.damage(5, 3), 4)
        self.assertEqual(fb.damage(6, 3), 0)

class TestLightningBolt(TestCase):
    def test_mana_cost(self):
        lb = LightningBolt()
        self.assertEqual(lb.mana_cost(), 30)

    def test_damage(self):
        lb = LightningBolt()
        self.assertEqual(lb.damage(0, 1), 0)
        self.assertEqual(lb.damage(1, 1), 26)
        self.assertEqual(lb.damage(2, 1), 8)
        self.assertEqual(lb.damage(3, 1), 8)
        self.assertEqual(lb.damage(4, 1), 0)

class TestBlindingFlash(TestCase):
    def test_mana_cost(self):
        bf = BlindingFlash()
        self.assertEqual(bf.mana_cost(), 40)

    def test_damage(self):
        bf = BlindingFlash()
        self.assertEqual(bf.damage(0, 0), 8)
        self.assertEqual(bf.damage(1, 0), 8)
        self.assertEqual(bf.damage(2, 0), 8)
        self.assertEqual(bf.damage(3, 0), 8)
        self.assertEqual(bf.damage(4, 0), 8)

class TestEarthquake(TestCase):
    def test_mana_cost(self):
        eq = Earthquake()
        self.assertEqual(eq.mana_cost(), 50)

    def test_damage(self):
        eq = Earthquake()
        self.assertEqual(eq.damage(0, 0), 0)
        self.assertEqual(eq.damage(1, 0), 20)
        self.assertEqual(eq.damage(2, 0), 0)
        self.assertEqual(eq.damage(3, 0), 20)
        self.assertEqual(eq.damage(4, 0), 0)

class TestHeal(TestCase):
    def test_mana_cost(self):
        h = Heal()
        self.assertEqual(h.mana_cost(), 50)

    def test_damage(self):
        h = Heal()
        self.assertEqual(h.damage(0, 2), 0)
        self.assertEqual(h.damage(1, 2), 0)
        self.assertEqual(h.damage(2, 2), -30)
        self.assertEqual(h.damage(3, 2), 0)
        self.assertEqual(h.damage(4, 2), 0)