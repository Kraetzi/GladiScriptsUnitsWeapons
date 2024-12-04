import os
import xml.etree.ElementTree as ET

# Dictionary of weapons and their desired rangeMax values for exact matches
weapon_ranges = {
    "pulserifle": 4,
    "bombastfieldgun": 6,
    "twinlinkedpulsecarbine": 2, 
    "fusionblaster": 2,
    "twinlinkedsmartmissilesystem": 4,
    "missilepod": 4,
    "twinlinkedmissilepod" : 4,
    "slugga": 1,
    "incendinecombustor":1,
    "pulseblaster":2,
    "twinlinkedfusionblaster": 2,
    # Add more weapons and their ranges here for exact matching
}

# Keywords for loose matching and their corresponding rangeMax values
loose_matches = {
    "pistol": 1,
    "flame": 1,
    "grenade": 1,
    # Add more keywords and their ranges here for loose matching
}

# Function to modify XML file for exact matches
def modify_xml_for_exact_match(file_path, weapon_ranges):
    try:
        # Get the weapon name from the filename (without extension)
        weapon_name = os.path.splitext(os.path.basename(file_path))[0].lower()

        # Check if the weapon name exists in the dictionary (exact match)
        if weapon_name in weapon_ranges:
            new_range_max = weapon_ranges[weapon_name]
            print(f"Found exact match for '{weapon_name}' in {os.path.basename(file_path)}.")

            # Parse the XML file
            tree = ET.parse(file_path)
            root = tree.getroot()

            # Find and update rangeMax
            target = root.find("target")
            if target is not None and target.get("rangeMax") is not None:
                print(f"Updating rangeMax for {weapon_name} to {new_range_max}.")
                target.set("rangeMax", str(new_range_max))

                # Save the changes to the file
                tree.write(file_path, encoding="utf-8", xml_declaration=True)
                print(f"Modified {os.path.basename(file_path)}.")
            else:
                print(f"rangeMax not found for {weapon_name} in {os.path.basename(file_path)}.")
        else:
            print(f"Weapon '{weapon_name}' is not in the exact match list, skipping.")

    except ET.ParseError as e:
        print(f"Skipping {os.path.basename(file_path)} due to parse error: {e}")

# Function to modify XML file for loose matches
def modify_xml_for_loose_match(file_path, loose_matches):
    try:
        # Get the weapon name from the filename (without extension)
        weapon_name = os.path.splitext(os.path.basename(file_path))[0].lower()

        # Check if any keyword in loose_matches is in the weapon name
        for keyword, new_range_max in loose_matches.items():
            if keyword.lower() in weapon_name:
                print(f"Found loose match for keyword '{keyword}' in {os.path.basename(file_path)}.")

                # Parse the XML file
                tree = ET.parse(file_path)
                root = tree.getroot()

                # Find and update rangeMax
                target = root.find("target")
                if target is not None and target.get("rangeMax") is not None:
                    print(f"Updating rangeMax for {weapon_name} (loose match) to {new_range_max}.")
                    target.set("rangeMax", str(new_range_max))

                    # Save the changes to the file
                    tree.write(file_path, encoding="utf-8", xml_declaration=True)
                    print(f"Modified {os.path.basename(file_path)}.")
                else:
                    print(f"rangeMax not found for {weapon_name} in {os.path.basename(file_path)}.")
                break  # Exit the loop after the first match
        else:
            print(f"Weapon '{weapon_name}' does not match any loose keywords, skipping.")

    except ET.ParseError as e:
        print(f"Skipping {os.path.basename(file_path)} due to parse error: {e}")

# Process all XML files in the folder where the script is located
def process_weapons_in_current_folder(base_directory, weapon_ranges, loose_matches):
    for dirpath, _, filenames in os.walk(base_directory):
        for file in filenames:
            if file.endswith('.xml'):  # Only process XML files
                file_path = os.path.join(dirpath, file)
                
                # First, try exact match
                modify_xml_for_exact_match(file_path, weapon_ranges)
                
                # Then, try loose match
                modify_xml_for_loose_match(file_path, loose_matches)

# Main Execution
if __name__ == "__main__":
    # Get the directory of the current script
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Process all XML files in the folder and subfolders
    process_weapons_in_current_folder(base_dir, weapon_ranges, loose_matches)
    print("Processing complete.")
