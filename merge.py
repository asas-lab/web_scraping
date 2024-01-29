import json

def merge_json_datasets(file1_path, file2_path, output_path):
    # Read the content of both JSON files
    with open(file1_path, 'r') as file1:
        data1 = json.load(file1)

    with open(file2_path, 'r') as file2:
        data2 = json.load(file2)

    # Merge the datasets
    merged_data = data1 + data2

    # Write the merged content back to a new file
    with open(output_path, 'w', encoding='utf-8') as output_file:
        json.dump(merged_data, output_file, ensure_ascii=False, indent=4)

# Example usage:
# file1_path = 'AlriyadhNews.json'
# file2_path = 'AlyaumNews.json'
# output_path = 'ArabNews.json'

merge_json_datasets(file1_path, file2_path, output_path)
