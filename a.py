import json

input_path = "train1.jsonl"
output_path = "train1_fixed.jsonl"

with open(input_path, "r", encoding="utf-8") as infile, \
     open(output_path, "w", encoding="utf-8") as outfile:
    
    for line in infile:
        data = json.loads(line)
        
        # Force output to string
        if "output" in data:
            data["output"] = str(data["output"])
        
        outfile.write(json.dumps(data, ensure_ascii=False) + "\n")
