import json

# Read the raw JSON data from the file
with open('./data/raw/example.json', 'r') as in_file:
    json_raw = json.load(in_file)

# Create a pretty-formatted JSON string
pretty_json = json.dumps(json_raw, indent=4)

# Write the pretty-formatted JSON string directly to the output file
with open('./data/raw/pretty_example.json', 'w') as out_file:
    out_file.write(pretty_json)
