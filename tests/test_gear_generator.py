import cadquery as cq
from plugins.gear_generator.gear_generator import *
from unittest import TestCase
from math import sin, radians


class TestGearGenerator(TestCase):
    def test_bevel_gear(self):
        """
        Tests if the bevel gear has been created successfully 
        by checking if it's valid and it's resulting volume
        Numerical values volumes were obtained with the Volume() functions on a Windows 10 machine with python 3.9.2
        """
        m = 1.5
        z = 16
        b = 6
        delta = 45
        R = (m * z / 2) / sin(radians(delta))
        alpha = 20
        helix_angle = 20
        clearance = 6

        gear1 = BevelGear(m, z, b, delta, R, alpha=alpha, clearance=clearance).build()
        gear2 = BevelGear(
            m, z, b, delta, R, alpha=alpha, clearance=clearance, helix_angle=helix_angle
        ).build()

        self.assertTrue(gear1.val().isValid())
        self.assertAlmostEqual(gear1.val().Volume(), 2505.7966225157024, 1)

        self.assertTrue(gear2.val().isValid())
        self.assertAlmostEqual(gear1.val().Volume(), 2505.7531046471067, 1)

    def test_bevel_gear_system(self):
        """
        Tests if the bevel gear system been created successfully 
        by checking if it's valid and it's resulting volume
        Numerical values volumes were obtained with the Volume() functions on a Windows 10 machine with python 3.9.2
        """
        m = 1
        z1 = 16
        z2 = 22
        b = 2
        alpha = 20
        helix_angle = 20
        clearance = 3

        pinion1, gear1 = BevelGearSystem(
            m, z1, z2, b, clearance1=clearance, clearance2=clearance, alpha=alpha
        ).build()
        self.assertTrue(pinion1.val().isValid())
        self.assertTrue(gear1.val().isValid())
        self.assertAlmostEqual(pinion1.val().Volume(), 483.3443067836134, 1)
        self.assertAlmostEqual(gear1.val().Volume(), 1126.5921554741049, 1)

        pinion2, gear2 = BevelGearSystem(
            m,
            z1,
            z2,
            b,
            clearance1=clearance,
            clearance2=clearance,
            helix_angle=helix_angle,
            alpha=alpha,
        ).build()
        self.assertTrue(pinion2.val().isValid())
        self.assertTrue(gear2.val().isValid())
        self.assertAlmostEqual(pinion2.val().Volume(), 483.3523144907097, 1)
        self.assertAlmostEqual(gear2.val().Volume(), 1126.605502545581, 1)

    def test_gear(self):
        """
        Tests if the gear has been created successfully 
        by checking if it's valid and it's resulting volume
        Numerical values volumes were obtained with the Volume() functions on a Windows 10 machine with python 3.9.2
        """
        m = 1.5
        z = 22
        b = 12
        alpha = 14
        helix_angle = 35

        gear1 = Gear(m, z, b, alpha=alpha, raw=False).build()
        self.assertTrue(gear1.val().isValid())
        self.assertTrue(
            (gear1.val().Volume() > 10113 - 70 and gear1.val().Volume() < 10113 + 70)
        )

        gear2 = Gear(m, z, b, alpha=alpha, helix_angle=helix_angle, raw=True).build()
        self.assertTrue(gear2.val().isValid())
        self.assertAlmostEqual(gear2.val().Volume(), 10033.574314576623, 1)
