import cadquery as cq
import gear_generator
from unittest import TestCase

class TestGearGenerator(TestCase):
    def test_make_bevel_gear(self):
        """
        Tests if the bevel gear has been created successfully 
        by checking if it's valid and it's resulting volume
        Numerical values volumes were obtained with the Volume() functions on a Windows 10 machine with python 3.8.8
        """
        m = 1.5
        z = 16
        b = 6
        delta = 40
        alpha = 20
        clearance = 6
        gear = cq.Workplane().make_bevel_gear(m, z, b, delta, alpha = alpha, clearance = clearance)
        self.assertTrue(gear.val().isValid())
        self.assertAlmostEqual(gear.val().Volume(),2226.028600964595)


    def test_make_bevel_gear_system(self):
        """
        Tests if the bevel gear system been created successfully 
        by checking if it's valid and it's resulting volume
        Numerical values volumes were obtained with the Volume() functions on a Windows 10 machine with python 3.8.8
        """
        m = 1
        z1 = 16
        z2 = 22
        b = 2
        alpha = 20
        clearance = 3

        frozen_gear_system = cq.Workplane().make_bevel_gear_system(m, z1, z2, b, alpha=alpha, clearance = clearance, compound = True)
        self.assertTrue(frozen_gear_system.val().isValid())
        self.assertAlmostEqual(frozen_gear_system.val().Volume(),1024.4382489861382)

        gear1, gear2 = cq.Workplane().make_bevel_gear_system(m, z1, z2, b, alpha=alpha, clearance = clearance, compound = False)
        self.assertTrue(gear1.val().isValid())
        self.assertAlmostEqual(gear1.val().Volume(),338.4940609342948)
        
        self.assertTrue(gear2.val().isValid())
        self.assertAlmostEqual(gear2.val().Volume(),685.9422647793748)


    def test_make_gear(self):
        """
        Tests if the gear has been created successfully 
        by checking if it's valid and it's resulting volume
        Numerical values volumes were obtained with the Volume() functions on a Windows 10 machine with python 3.8.8
        """
        m = 1.5
        z = 16
        b = 6
        alpha = 20
        clearance = 6
        helix_angle = 40

        gear1 = cq.Workplane().make_gear(m, z, b, alpha=alpha, raw = False)
        self.assertTrue(gear1.val().isValid())
        self.assertAlmostEqual(gear1.val().Volume(),2646.766251684174)

        gear2 = cq.Workplane().make_gear(m, z, b, alpha=alpha, helix_angle = helix_angle, raw = False)
        self.assertTrue(gear2.val().isValid())
        self.assertAlmostEqual(gear2.val().Volume(),2646.816968237718)


    def test_make_crown_gear(self):
        """
        Tests if the crown gear has been created successfully 
        by checking if it's valid and it's resulting volume
        Numerical values volumes were obtained with the Volume() functions on a Windows 10 machine with python 3.8.8
        """
        m = 1.5
        z = 16
        b = 6
        alpha = 20
        clearance = 6

        gear = cq.Workplane().make_crown_gear(m, z, b, alpha = alpha, clearance = clearance)
        self.assertTrue(gear.val().isValid())
        self.assertAlmostEqual(gear.val().Volume(),3352.5459114045543)

    def test_make_rack_gear(self):
        """
        Tests if the rack gear has been created successfully 
        by checking if it's valid and it's resulting volume
        Numerical values volumes were obtained with the Volume() functions on a Windows 10 machine with python 3.8.8
        """
        m = 1.5
        z = 16
        b = 6
        length = 40
        alpha = 20
        clearance = 6
        helix_angle = 45

        gear1 = cq.Workplane().make_rack_gear(m, b, length, clearance, alpha = alpha)
        self.assertTrue(gear1.val().isValid())
        self.assertAlmostEqual(gear1.val().Volume(),1381.355198257374)

        gear2 = cq.Workplane().make_rack_gear(m, b, length, clearance, alpha = alpha, helix_angle = helix_angle)
        self.assertTrue(gear2.val().isValid())
        self.assertAlmostEqual(gear2.val().Volume(),1369.2236732856904)
