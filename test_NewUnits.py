import unittest
import os
import tempfile
import xml.etree.ElementTree as ET
from NewUnits import adjust_model_count_and_hitpoints  # Replace with the actual script name

class TestAdjustModelCountAndHitpoints(unittest.TestCase):

    def setUp(self):
        """Set up temporary directory and initialize common file paths."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_file = os.path.join(self.temp_dir.name, "test_unit.xml")

    def tearDown(self):
        """Clean up temporary directory after tests."""
        self.temp_dir.cleanup()

    def create_test_file(self, scale="1 1 1", group_size="5", hitpoints_base="100"):
        """Utility to create test XML files with configurable attributes."""
        root = ET.Element("root")
        model = ET.SubElement(root, "model")
        unit = ET.SubElement(model, "unit", scale=scale)
        group = ET.SubElement(root, "group", size=group_size)
        effects = ET.SubElement(root, "effects")
        ET.SubElement(effects, "hitpointsMax", base=hitpoints_base)

        tree = ET.ElementTree(root)
        tree.write(self.test_file)

    def test_standard_case(self):
        """Test normal behavior with valid elements."""
        self.create_test_file(scale="1 1 1", group_size="5", hitpoints_base="100")
        adjust_model_count_and_hitpoints(self.test_file)

        # Parse the updated XML
        tree = ET.parse(self.test_file)
        root = tree.getroot()

        # Check scale
        scale_element = root.find('./model/unit')
        self.assertEqual(scale_element.get("scale"), "2.0 2.0 2.0", "Scale was not doubled correctly.")

        # Check group size
        group_element = root.find('./group')
        self.assertEqual(group_element.get("size"), "3", "Group size was not halved and rounded up correctly.")

        # Check hitpoints
        hitpoints_element = root.find('.//effects/hitpointsMax')
        self.assertEqual(hitpoints_element.get("base"), "67", "Hitpoints were not adjusted correctly.")

    def test_single_model(self):
        """Test with a single model (group size = 1)."""
        self.create_test_file(scale="1 1 1", group_size="1", hitpoints_base="100")
        adjust_model_count_and_hitpoints(self.test_file)

        # Parse the updated XML
        tree = ET.parse(self.test_file)
        root = tree.getroot()

        # Check group size remains 1
        group_element = root.find('./group')
        self.assertEqual(group_element.get("size"), "1", "Group size should remain 1 for a single model.")

        # Check hitpoints halved
        hitpoints_element = root.find('.//effects/hitpointsMax')
        self.assertEqual(hitpoints_element.get("base"), "50", "Hitpoints were not halved for a single model.")

    def test_missing_group(self):
        """Test file without <group> element."""
        self.create_test_file(scale="1 1 1", hitpoints_base="100")
        os.remove(self.test_file)  # Remove the group element
        root = ET.Element("root")
        model = ET.SubElement(root, "model")
        ET.SubElement(model, "unit", scale="1 1 1")
        effects = ET.SubElement(root, "effects")
        ET.SubElement(effects, "hitpointsMax", base="100")

        tree = ET.ElementTree(root)
        tree.write(self.test_file)

        adjust_model_count_and_hitpoints(self.test_file)

        # Parse the updated XML
        tree = ET.parse(self.test_file)
        root = tree.getroot()

        # Check scale
        scale_element = root.find('./model/unit')
        self.assertEqual(scale_element.get("scale"), "2.0 2.0 2.0", "Scale was not doubled correctly.")

        # Check hitpoints halved
        hitpoints_element = root.find('.//effects/hitpointsMax')
        self.assertEqual(hitpoints_element.get("base"), "50", "Hitpoints were not halved without a group element.")

    def test_missing_scale(self):
        """Test file missing 'scale' attribute."""
        root = ET.Element("root")
        model = ET.SubElement(root, "model")
        ET.SubElement(model, "unit")  # No scale attribute
        group = ET.SubElement(root, "group", size="5")
        effects = ET.SubElement(root, "effects")
        ET.SubElement(effects, "hitpointsMax", base="100")

        tree = ET.ElementTree(root)
        tree.write(self.test_file)

        adjust_model_count_and_hitpoints(self.test_file)

        # File should remain unmodified
        with open(self.test_file, 'r') as f:
            content = f.read()
            self.assertIn('<unit />', content, "File should remain unmodified when 'scale' is missing.")

    def test_missing_hitpoints(self):
        """Test file missing hitpointsMax element."""
        root = ET.Element("root")
        model = ET.SubElement(root, "model")
        ET.SubElement(model, "unit", scale="1 1 1")
        group = ET.SubElement(root, "group", size="5")

        tree = ET.ElementTree(root)
        tree.write(self.test_file)

        adjust_model_count_and_hitpoints(self.test_file)

        # File should remain unmodified
        with open(self.test_file, 'r') as f:
            content = f.read()
            self.assertIn('<group size="5" />', content, "File should remain unmodified when 'hitpointsMax' is missing.")

    def test_invalid_values(self):
        """Test file with invalid values for attributes."""
        self.create_test_file(scale="invalid_scale", group_size="not_a_number", hitpoints_base="NaN")
        adjust_model_count_and_hitpoints(self.test_file)

        # File should remain unmodified due to invalid values
        with open(self.test_file, 'r') as f:
            content = f.read()
            self.assertIn('invalid_scale', content, "File should remain unmodified for invalid 'scale' values.")
            self.assertIn('not_a_number', content, "File should remain unmodified for invalid 'group size' values.")
            self.assertIn('NaN', content, "File should remain unmodified for invalid 'hitpointsMax' values.")

if __name__ == "__main__":
    unittest.main()
