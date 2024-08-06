# python3 extractions/test_cases/generate_simple_extraction_test_cases_txt_files.py

import os
import yaml

def create_test_case_files(file_path, output_dir):
    # Read the contents of the test case data file
    with open(file_path, 'r') as file:
        test_data_contents = file.read()
    
    # Parse the YAML content
    test_cases = yaml.safe_load(test_data_contents)
    
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Initialize a list to store all positive test case values
    all_positive_cases = []
    
    # Function to write data to a file, including headings for both positive and negative cases
    def write_to_file(file_path, positive_data, negative_data):
        with open(file_path, 'w') as file:
            if positive_data:
                file.write("====Good====\n\n")
                for item in positive_data:
                    file.write(f"{item}\n")
                file.write("\n")  # Add a newline for separation
            if negative_data:
                file.write("====Bad====\n\n")
                for item in negative_data:
                    file.write(f"{item}\n")
    
    # Iterate over the test cases and create a single file for each
    for case_name, case_data in test_cases.items():
        file_path = os.path.join(output_dir, f"{case_name}.txt")
        # Extract positive and negative examples, if available
        positive_data = case_data.get('test_positive_examples', [])
        negative_data = case_data.get('test_negative_examples', [])
        
        # Append positive data to the all_positive_cases list
        all_positive_cases.extend(positive_data)
        
        # Write both positive and negative examples to the same file
        write_to_file(file_path, positive_data, negative_data)
    
    # Write all positive cases to all_cases.txt
    all_cases_file_path = os.path.join(output_dir, "all_cases.txt")
    with open(all_cases_file_path, 'w') as file:
        for item in all_positive_cases:
            file.write(f"{item}\n")

# Usage
file_path = 'includes/extractions/test_cases/test_data.yaml'  # Update this to your file's location
output_dir = 'tests/inputs/extraction_types/'  # Update this to your desired output directory
create_test_case_files(file_path, output_dir)

print("Test case files and all_cases.txt created successfully.")