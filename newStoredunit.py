import os
import xml.etree.ElementTree as ET

# Define the unit-specific settings
unit_settings = {
    "firewarrior": {  # Unit name (case-insensitive match)
        "scale": "1.0 1.0 1.0",  # Fixed model size
        "group_size": 6,         # Fixed group size
        "hitpoints": 10          # Fixed hitpoints
    },
        "ghostkeelbattlesuit": {  # Unit name (case-insensitive match)
        "scale": "2.0 2.0 2.0",  # Fixed model size
        "group_size": 3,         # Fixed group size
        "hitpoints": 50          # Fixed hitpoints
    },
    # Add more units here if needed
}

# Function to modify a specific unit
def modify_unit(file_path, unit_name, settings):
    try:
        print(f"Processing: {file_path}")

        # Parse the XML file
        tree = ET.parse(file_path)
        root = tree.getroot()

        # Check if the unit matches the target unit
        unit_name_from_file = os.path.splitext(os.path.basename(file_path))[0].lower()
        if unit_name_from_file != unit_name.lower():
            print(f"Skipping {file_path}: Unit name does not match.")
            return

        # Locate the necessary XML elements
        unit_element = root.find('.//unit')
        group_element = root.find("./group")
        hitpoints_element = root.find('.//modifiers//effects//hitpointsMax')

        # Debugging output for unit_element
        print(f"Current unit element: {ET.tostring(unit_element, encoding='unicode', method='xml')}")

        # Access the 'scale' attribute from the 'unit' element
        scale_element = unit_element.get("scale")

        # Debugging output for scale_element
        print(f"Current scale element: {scale_element}")

        if scale_element is None or hitpoints_element is None:
            print(f"Skipping {file_path}: Missing required elements.")
            return

        # Modify the scale
        unit_element.set("scale", settings["scale"])
        print(f"New scale value set to: {settings['scale']}")

        # Modify the group size
        if group_element is not None:
            group_element.set("size", str(settings["group_size"]))
            print(f"Group size set to: {settings['group_size']}")

        # Modify the hitpoints
        hitpoints_element.set("base", str(settings["hitpoints"]))
        print(f"Hitpoints set to: {settings['hitpoints']}")

        # Save the changes
        tree.write(file_path, encoding="utf-8", xml_declaration=True)
        print(f"Modified {file_path} with settings for {unit_name}.")
    
    except ET.ParseError as e:
        print(f"Parse error in {file_path}: {e}")
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

# Function to process all XML files in the current folder
def process_units_in_folder(directory, unit_settings):
    for dirpath, _, filenames in os.walk(directory):
        for file in filenames:
            if file.endswith('.xml'):
                file_path = os.path.join(dirpath, file)
                for unit_name, settings in unit_settings.items():
                    modify_unit(file_path, unit_name, settings)

# Main Execution
if __name__ == "__main__":
    base_dir = os.getcwd()  # Current working directory
    process_units_in_folder(base_dir, unit_settings)
    print("Processing complete.")
