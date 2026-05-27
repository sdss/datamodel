""" replace_me_with_values.py
    Created by Joel Brownstein on 5/21/26.
"""

import argparse
import os
from ruamel.yaml import YAML

def replace_me_with_values(input_filepath, output_filepath):
    # Initialize ruamel.yaml object configured to preserve formatting and quotes
    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.width = 4096  # Prevent line wrapping on long descriptions
    
    print(f"Loading {input_filepath}...")
    try:
        with open(input_filepath, 'r') as f:
            data = yaml.load(f)
    except FileNotFoundError:
        print(f"Error: The file '{input_filepath}' could not be found.")
        return
        
    # Traverse through releases -> [release_name] -> hdus
    releases = data.get('releases', {}) if data else {}
    for release_name, release_data in releases.items():
        if not isinstance(release_data, dict) or 'hdus' not in release_data:
            continue
            
        print(f"Processing release: {release_name}")
        for hdu_name, hdu_data in release_data['hdus'].items():
            tcomm_mapping = {}
            
            # 1. Extract mapping of TCOMMx keys to their descriptions
            if 'header' in hdu_data and isinstance(hdu_data['header'], list):
                for item in hdu_data['header']:
                    if isinstance(item, dict) and 'key' in item and str(item['key']).startswith('TCOMM'):
                        try:
                            # Extract the column index (e.g., TCOMM1 -> 1)
                            idx = int(str(item['key']).replace('TCOMM', ''))
                            tcomm_mapping[idx] = str(item.get('value', '')).strip()
                        except ValueError:
                            continue
            
            # 2. Iterate through columns in order and update 'replace me'
            if 'columns' in hdu_data and isinstance(hdu_data['columns'], dict):
                # ruamel.yaml preserves the order of columns as they appear in the file
                for i, (col_name, col_data) in enumerate(hdu_data['columns'].items(), start=1):
                    if i in tcomm_mapping:
                        if isinstance(col_data, dict):
                            current_desc = str(col_data.get('description', ''))
                            
                            # Update if description is missing or flags a placeholder replacement
                            if current_desc.startswith('replace me') or not current_desc:
                                col_data['description'] = tcomm_mapping[i]
                            
    # Save the updated datamodel
    print(f"Saving fixed file to {output_filepath}...")
    with open(output_filepath, 'w') as f:
        yaml.dump(data, f)
    
    print("Done!")

if __name__ == '__main__':
    # Set up argument parsing
    parser = argparse.ArgumentParser(
        description="Fix column descriptions in a datamodel YAML file using its TCOMM header keys."
    )
    parser.add_argument(
        'input_file', 
        help="Path to the input YAML file to be processed."
    )
    parser.add_argument(
        '-o', '--output', 
        help="Path to the output fixed YAML file. If omitted, defaults to '[input_filename].1.yaml'."
    )
    
    args = parser.parse_args()
    
    # If no output path is provided, automatically generate one based on the input name
    if args.output:
        output_file = args.output
    else:
        base, ext = os.path.splitext(args.input_file)
        output_file = f"{base}.1{ext}"
        
    replace_me_with_values(args.input_file, output_file)
