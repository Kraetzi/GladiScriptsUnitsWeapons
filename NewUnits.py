import xml.etree.ElementTree as ET
import os
import math

def adjust_model_count_and_hitpoints(xml_file):
    print(f"Start processing {xml_file}")
    try:
        # Parse the XML file
        tree = ET.parse(xml_file)
        root = tree.getroot()

        # Find relevant elements
        scale_element = root.find('./model/unit')
        group_element = root.find("./group")
        hitpoints_element = root.find('.//effects/hitpointsMax')

        # Skip files missing required elements
        if scale_element is None or hitpoints_element is None:
            print(f"Skipping {xml_file}: Missing required elements.")
            return

        try:
            scale = [float(i) for i in scale_element.get("scale", "1 1 1").split(" ")]
        except AttributeError:
            print(f"Skipping {xml_file}: 'scale' attribute missing or invalid.")
            return

        hitpoints_max = float(hitpoints_element.attrib.get("base", 0))
        print(f"Original scale: {scale}, hitpointsMax: {hitpoints_max}")

        if group_element is not None:
            try:
                group_size = int(group_element.get("size", "1"))
                #rows = int(group_element.get("rowSize", "1"))
            except ValueError:
                print(f"Skipping {xml_file}: Invalid 'size' or 'rowSize' attributes.")
                return

        # Processing group size
        if group_element is not None and group_size > 1:
            new_model_count = math.ceil(group_size/2)  # Halve, rounding up
            #new_rows = (rows + 1) // 2
            if group_size % 2 != 0:
                imagined_round_size = group_size + 1
                hitpoints_reduction_factor = group_size / imagined_round_size
                new_hitpoints_max = int(math.ceil(hitpoints_max*new_model_count *hitpoints_reduction_factor /new_model_count))
            else: new_hitpoints_max == hitpoints_max
        else:
            new_hitpoints_max = hitpoints_max // 2  # Single model, halve directly

        # Double the model scale
        new_scale = [i * 2 for i in scale]

        print(f"New scale: {new_scale}, Adjusted hitpointsMax: {new_hitpoints_max}")

        # Update XML elements
        scale_element.set('scale', ' '.join(map(str, new_scale)))
        hitpoints_element.set('base', str(new_hitpoints_max))

        if group_element is not None:
            group_element.set('size', str(new_model_count))
            #group_element.set('rowSize', str(new_rows))

        # Write changes back to the file
        tree.write(xml_file)
        print(f"Modified {xml_file}")

    except ET.ParseError as e:
        print(f"Skipping {xml_file} due to parse error: {e}")
    except Exception as e:
        print(f"Skipping {xml_file} due to unexpected error: {e}")


def process_all_units(base_directory):
    for dirpath, dirnames, filenames in os.walk(base_directory):  # Walk through all directories and files
        if "Units" in os.path.basename(dirpath):  # Process folders named "Units"
            for root_dir, _, files in os.walk(dirpath):  # Process subfolders and files inside "Units"
                for file in files:
                    if file.endswith('.xml'):  # Only process XML files
                        full_path = os.path.join(root_dir, file)
                        adjust_model_count_and_hitpoints(full_path)


# Main execution
if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the current script
    process_all_units(base_dir)
    print('All files processed.')
