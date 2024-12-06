import xml.etree.ElementTree as ET
import os

# Dictionary for exact matches: specify unit names and their desired adjustments
unit_modifications = {
    "terminator": {"scale_multiplier": 2, "group_size_divisor": 2, "hitpoints_divisor": 2},
    "dreadnought": {"scale_multiplier": 2, "group_size_divisor": 1, "hitpoints_divisor": 1.5},
    "firewarrior": {"scale_multiplier": 3, "group_size_divisor": 2, "hitpoints_divisor": 1.5},
    # Add more units here with their specific modifications
}

# Keywords for loose matching and their default adjustments
loose_matches = {
    #"marine": {"scale_multiplier": 1.5, "group_size_divisor": 2, "hitpoints_divisor": 2},
    #"tank": {"scale_multiplier": 2, "group_size_divisor": 1, "hitpoints_divisor": 1.25},
    # Add more keywords and default adjustments here
}

# Function to modify unit based on exact match
def modify_unit_exact_match(file_path, unit_modifications):
    try:
        unit_name = os.path.splitext(os.path.basename(file_path))[0].lower()

        # Check for exact match
        if unit_name in unit_modifications:
            modifications = unit_modifications[unit_name]
            print(f"Found exact match for unit '{unit_name}' in {os.path.basename(file_path)}.")

            # Parse the XML file
            tree = ET.parse(file_path)
            root = tree.getroot()

            # Find relevant XML elements
            scale_element = root.find('./model/unit')
            group_element = root.find("./group")
            hitpoints_element = root.find('.//effects/hitpointsMax')

            if not scale_element or not hitpoints_element:
                print(f"Skipping {file_path}: Missing required elements.")
                return

            # Get current values
            scale = [float(i) for i in scale_element.get("scale", "1 1 1").split(" ")]
            group_size = int(group_element.get("size", "1")) if group_element else 1
            hitpoints_max = float(hitpoints_element.attrib.get("base", 0))

            print(f"Original scale: {scale}, group size: {group_size}, hitpointsMax: {hitpoints_max}")

            # Apply modifications
            new_scale = [s * modifications["scale_multiplier"] for s in scale]
            new_group_size = max(1, (group_size + modifications["group_size_divisor"] - 1) // modifications["group_size_divisor"])
            new_hitpoints = int(hitpoints_max / modifications["hitpoints_divisor"])

            # Update XML elements
            scale_element.set("scale", " ".join(map(str, new_scale)))
            hitpoints_element.set("base", str(new_hitpoints))
            if group_element:
                group_element.set("size", str(new_group_size))

            # Save changes
            tree.write(file_path, encoding="utf-8", xml_declaration=True)
            print(f"Modified {os.path.basename(file_path)}.")
        else:
            print(f"Unit '{unit_name}' is not in the exact match list, skipping.")

    except ET.ParseError as e:
        print(f"Skipping {os.path.basename(file_path)} due to parse error: {e}")
    except Exception as e:
        print(f"Error processing {os.path.basename(file_path)}: {e}")

# Function to modify unit based on loose match
def modify_unit_loose_match(file_path, loose_matches):
    try:
        unit_name = os.path.splitext(os.path.basename(file_path))[0].lower()

        # Check for loose match
        for keyword, adjustments in loose_matches.items():
            if keyword in unit_name:
                print(f"Found loose match for keyword '{keyword}' in {os.path.basename(file_path)}.")

                # Parse the XML file
                tree = ET.parse(file_path)
                root = tree.getroot()

                # Find relevant XML elements
                scale_element = root.find('./model/unit')
                group_element = root.find("./group")
                hitpoints_element = root.find('.//effects/hitpointsMax')

                if not scale_element or not hitpoints_element:
                    print(f"Skipping {file_path}: Missing required elements.")
                    return

                # Get current values
                scale = [float(i) for i in scale_element.get("scale", "1 1 1").split(" ")]
                group_size = int(group_element.get("size", "1")) if group_element else 1
                hitpoints_max = float(hitpoints_element.attrib.get("base", 0))

                print(f"Original scale: {scale}, group size: {group_size}, hitpointsMax: {hitpoints_max}")

                # Apply adjustments
                new_scale = [s * adjustments["scale_multiplier"] for s in scale]
                new_group_size = max(1, (group_size + adjustments["group_size_divisor"] - 1) // adjustments["group_size_divisor"])
                new_hitpoints = int(hitpoints_max / adjustments["hitpoints_divisor"])

                # Update XML elements
                scale_element.set("scale", " ".join(map(str, new_scale)))
                hitpoints_element.set("base", str(new_hitpoints))
                if group_element:
                    group_element.set("size", str(new_group_size))

                # Save changes
                tree.write(file_path, encoding="utf-8", xml_declaration=True)
                print(f"Modified {os.path.basename(file_path)}.")
                break  # Exit loop after first match
        else:
            print(f"Unit '{unit_name}' does not match any loose keywords, skipping.")

    except ET.ParseError as e:
        print(f"Skipping {os.path.basename(file_path)} due to parse error: {e}")
    except Exception as e:
        print(f"Error processing {os.path.basename(file_path)}: {e}")

# Process all XML files in the folder where the script is located
def process_units_in_current_folder(base_directory, unit_modifications, loose_matches):
    for dirpath, _, filenames in os.walk(base_directory):
        for file in filenames:
            if file.endswith('.xml'):  # Only process XML files
                file_path = os.path.join(dirpath, file)
                
                # First, try exact match
                modify_unit_exact_match(file_path, unit_modifications)
                
                # Then, try loose match
                modify_unit_loose_match(file_path, loose_matches)

# Main Execution
if __name__ == "__main__":
    # Get the directory of the current script
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Process all XML files in the folder and subfolders
    process_units_in_current_folder(base_dir, unit_modifications, loose_matches)
    print("Processing complete.")
