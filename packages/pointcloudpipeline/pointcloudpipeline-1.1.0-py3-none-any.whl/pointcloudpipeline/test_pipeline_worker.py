from pipeline_worker import convertToLaz, convertFromLaz, convertLazToEPTLaz, convertLAZTo2D
import unittest
import shutil
import os

class TestWorker(unittest.TestCase):
    def test_view(self):
        self.assertEqual(convertLazToEPTLaz("la.laz", "le", "la/untwine"), "la.laz does not exist.", "Should be la.laz does not exist.")
        self.assertFalse(os.path.exists("le/la.laz"))
        self.assertTrue("--files=" in convertLazToEPTLaz("./test_data/from/test.laz", "./test_data/to", "./untwine/build/untwine"))
        self.assertTrue(os.path.exists("./test_data/to/test"))
        shutil.rmtree("./test_data/to/test")

    def test_convertLazToLaz(self):
        self.assertEqual(convertToLaz("la.laz", "le"), "la.laz does not exist.", "Should be la.laz does not exist.")
        self.assertFalse(os.path.exists("le/la.laz"))
        self.assertTrue("metadata" in convertToLaz("./test_data/from/test.laz", "./test_data/to"))
        self.assertTrue(os.path.exists("./test_data/to/test.laz"))
        os.remove("./test_data/to/test.laz")

    def test_convertE57ToLaz(self):
        self.assertEqual(convertToLaz("la.e57", "le"), "la.e57 does not exist.", "Should be la.e57 does not exist.")
        self.assertFalse(os.path.exists("le/la.laz"))
        self.assertTrue("metadata" in convertToLaz("./test_data/from/test.laz", "./test_data/to"))
        self.assertTrue(os.path.exists("./test_data/to/test.laz"))
        os.remove("./test_data/to/test.laz")

    def test_convertplyToLaz(self):
        self.assertEqual(convertToLaz("la.ply", "le"), "la.ply does not exist.", "Should be la.ply does not exist.")
        self.assertFalse(os.path.exists("le/la.laz"))
        self.assertTrue("metadata" in convertToLaz("./test_data/from/test.laz", "./test_data/to"))
        self.assertTrue(os.path.exists("./test_data/to/test.laz"))
        os.remove("./test_data/to/test.laz")

    def test_convertlasToLaz(self):
        self.assertEqual(convertToLaz("la.las", "le"), "la.las does not exist.", "Should be la.las does not exist.")
        self.assertFalse(os.path.exists("le/la.laz"))
        self.assertTrue("metadata" in convertToLaz("./test_data/from/test.laz", "./test_data/to"))
        self.assertTrue(os.path.exists("./test_data/to/test.laz"))
        os.remove("./test_data/to/test.laz")

    def test_generateLazFromLaz(self):
        self.assertEqual(convertFromLaz("la.laz", "le", "laz"), "la.laz does not exist.", "Should be la.laz does not exist.")
        self.assertFalse(os.path.exists("le/la.laz"))
        self.assertTrue("metadata" in convertFromLaz("./test_data/from/test.laz", "./test_data/to", "laz"))
        self.assertTrue(os.path.exists("./test_data/to/test.laz"))
        os.remove("./test_data/to/test.laz")

    def test_generateE57FromLaz(self):
        self.assertEqual(convertFromLaz("la.laz", "le", "e57"), "la.laz does not exist.", "Should be la.laz does not exist.")
        self.assertFalse(os.path.exists("le/la.e57"))
        self.assertTrue("metadata" in convertFromLaz("./test_data/from/test.laz", "./test_data/to", "e57"))
        self.assertTrue(os.path.exists("./test_data/to/test.e57"))
        os.remove("./test_data/to/test.e57")

    def test_generatePlyFromLaz(self):
        self.assertEqual(convertFromLaz("la.laz", "le", "ply"), "la.laz does not exist.", "Should be la.laz does not exist.")
        self.assertFalse(os.path.exists("le/la.ply"))
        self.assertTrue("metadata" in convertFromLaz("./test_data/from/test.laz", "./test_data/to", "ply"))
        self.assertTrue(os.path.exists("./test_data/to/test.ply"))
        os.remove("./test_data/to/test.ply")

    def test_generateLasFromLaz(self):
        self.assertEqual(convertFromLaz("la.laz", "le", "las"), "la.laz does not exist.", "Should be la.laz does not exist.")
        self.assertFalse(os.path.exists("le/la.las"))
        self.assertTrue("metadata" in convertFromLaz("./test_data/from/test.laz", "./test_data/to", "las"))
        self.assertTrue(os.path.exists("./test_data/to/test.las"))
        os.remove("./test_data/to/test.las")

    def test_get2d(self):
        self.assertEqual(convertLAZTo2D("la.laz", "le"), "la.laz does not exist.", "Should be la.laz does not exist.")
        self.assertFalse(os.path.exists("le/la.tif"))
        self.assertTrue("metadata" in convertLAZTo2D("./test_data/from/test.laz", "./test_data/to"))
        self.assertTrue(os.path.exists("./test_data/to/test.tif"))
        os.remove("./test_data/to/test.tif") 

if __name__ == '__main__':
    unittest.main()


