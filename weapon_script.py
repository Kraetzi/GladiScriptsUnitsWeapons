import os
import xml.etree.ElementTree as ET

# Folder containing XML files
#folder_path = r"D:\Documents\Proxy Studios\Gladius\Mods\MegaMod WeaponsRange\Data\World\Weapons\NightLords"

# Function to determine custom range multiplier based on army list
def get_custom_range_multiplier(weapon_name):
    # Placeholder for custom logic based on army list
    army_list_modifiers = {
        "example_weapon_name": 1.8,  # Custom multiplier for specific weapons
    }
    return army_list_modifiers.get(weapon_name, 2)  # Default to approx 2 if not in list

# Function to process and modify XML files
def modify_xml_file(file_path):
    try:
        # Parse the XML file
        tree = ET.parse(file_path)
        root = tree.getroot()

        # Extract weapon name for conditional logic
        weapon_name_element = root.find(".//trait[@name]")
        weapon_name = weapon_name_element.attrib['name'] if weapon_name_element is not None else ""

        # Convert weapon name to lowercase for case-insensitive checks
        is_pistol_or_flame = "pistol" in weapon_name.lower() or "flame" in weapon_name.lower()

        # Modify weapon range and strength based on conditions
        target = root.find("target")
        if target is not None:
            range_attr = target.get("rangeMax")
            
            if range_attr is not None:
                # Current range value
                range_value = float(range_attr)
                multiplier = get_custom_range_multiplier(weapon_name)
                new_range = round(range_value * multiplier - 1)  # Calculate new range

                # If the calculated range is the same as the current range
                if new_range == range_value:
                    if is_pistol_or_flame:
                        # If "pistol" or "flame" is in the name, increase rangedDamage by 1
                        ranged_damage = root.find(".//modifier/effects/rangedDamage")
                        if ranged_damage is not None:
                            current_damage = float(ranged_damage.get("add", "0"))
                            ranged_damage.set("add", str(current_damage + 1))
                    else:
                        # Otherwise, increase range by 1
                        target.set("rangeMax", str(int(range_value) + 1))
                else:
                    # Set the calculated range if it changes
                    target.set("rangeMax", str(int(new_range)))

            else:
                # For close combat weapon, adjust strength
                strength = root.find(".//modifier/effects/strengthDamage")
                if strength is not None:
                    base_value = float(strength.get("base", "0"))
                    new_strength = base_value + (base_value * 0.5)
                    strength.set("base", str(int(round(new_strength))))  # Ensure integer value for strength

        # Save the modified XML back to the file
        tree.write(file_path, encoding="utf-8", xml_declaration=True)
        print(f"Modified {os.path.basename(file_path)}")

    except ET.ParseError as e:
        print(f"Skipping {os.path.basename(file_path)} due to parse error: {e}")

def process_all_weapons(base_directory):
    for dirpath, dirnames, filenames in os.walk(base_directory):  # Walk through all directories and files
        if "Weapons" in os.path.basename(dirpath):  # Process folders named "Units"
            for root_dir, _, files in os.walk(dirpath):  # Process subfolders and files inside "Units"
                for file in files:
                    if file.endswith('.xml'):  # Only process XML files
                        full_path = os.path.join(root_dir, file)
                        modify_xml_file(full_path)

# Loop over each file in the folder and modify XML files
if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the current script
    process_all_weapons(base_dir)
    print('All files processed.')
print("Processing complete.")
