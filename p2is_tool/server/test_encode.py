import sys, json
sys.path.append('.')
from src.encoders.bin_encoder import encode_bin_from_json

with open(r'C:\Users\nolan\Desktop\6666666656\repo\traduction\event_scripts\script_382.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Run encode on just this file to see if there are ANY warnings or errors
out_bytes = encode_bin_from_json(data, r'C:\Users\nolan\Desktop\6666666656\repo\traduction\event_scripts\script_382.json', 
                                 r'C:\Users\nolan\Desktop\6666666656\repo\traduction\event_scripts\script_382.bin')
