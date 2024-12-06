import os
import xml.etree.ElementTree as ET

# Dictionaries for weapon modifications
weapon_ranges = {
    "pulserifle": 4,
    "bombastfieldgun": 6,
    "twinlinkedpulsecarbine": 2,
    "fusionblaster": 2,
    "twinlinkedsmartmissilesystem": 4,
    "missilepod": 4,
    "twinlinkedmissilepod": 4,
    "slugga": 1,
    "incendinecombustor": 1,
    "pulseblaster": 2,
    "twinlinkedfusionblaster": 2,
}

loose_matches = {
    "pistol": 1,
    "flame": 1,
    "grenade": 1,
}

# Additional dictionaries for fixed attack and damage values
weapon_attacks = {
    "pulserifle": 2,
    "bombastfieldgun": 2,
    "twinlinkedpulsecarbine": 4,
    "fusionblaster": 1,
    "missilepod": 2,
}

weapon_damage = {
    "pulserifle": 2,
    "bombastfieldgun": 4,
    "twinlinkedpulsecarbine": 2,
    "fusionblaster": 5,
    "missilepod": 3,
}

# Function to modify rangeMax, attacks, and damage
def modify_weapon_attributes(file_path):
    try:
        weapon_name = os.path.splitext(os.path.basename(file_path))[0].lower()

        # Parse the XML file
        tree = ET.parse(file_path)
        root = tree.getroot()

        # Modify rangeMax
        target = root.find("target")
        if weapon_name in weapon_ranges and target is not None:
            target.set("rangeMax", str(weapon_ranges[weapon_name]))
            print(f"Updated rangeMax for {weapon_name} to {weapon_ranges[weapon_name]}.")

        # Modify attacks and damage
        effects = root.find(".//effects")
        if effects is not None:
            # Set attacks
            attacks = effects.find("attacks")
            if weapon_name in weapon_attacks:
                if attacks is None:
                    attacks = ET.SubElement(effects, "attacks")
                attacks.set("add", str(weapon_attacks[weapon_name]))
                print(f"Updated attacks for {weapon_name} to {weapon_attacks[weapon_name]}.")

            # Set damage
            damage = effects.find("rangedDamage")
            if weapon_name in weapon_damage:
                if damage is None:
                    damage = ET.SubElement(effects, "rangedDamage")
                damage.set("add", str(weapon_damage[weapon_name]))
                print(f"Updated damage for {weapon_name} to {weapon_damage[weapon_name]}.")

        # Save the modified file
        tree.write(file_path, encoding="utf-8", xml_declaration=True)
        print(f"Processed {weapon_name} successfully.")

    except ET.ParseError as e:
        print(f"Skipping {file_path} due to parse error: {e}")
    except Exception as e:
        print(f"An error occurred while processing {file_path}: {e}")

# Process all XML files in the folder
def process_weapons_in_current_folder(base_directory):
    for dirpath, _, filenames in os.walk(base_directory):
        for file in filenames:
            if file.endswith(".xml"):
                file_path = os.path.join(dirpath, file)
                modify_weapon_attributes(file_path)

# Main Execution
if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    process_weapons_in_current_folder(base_dir)
    print("Processing complete.")
