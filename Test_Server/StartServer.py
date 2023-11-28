import json
import subprocess

# Open the JSON file and load the contents
with open('run_command.json', 'r') as f:
    data = json.load(f)

# Extract the command from the JSON data
command = data['command']

# Use subprocess.run() to execute the command
subprocess.run(command, shell=True)