# Copyright 2025 blu0
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0

import requests
import yaml
import json
import os
from datetime import datetime

# Load rules index
with open("rules_index.yaml", "r") as f:
    index = yaml.safe_load(f)

rule_sets = index["rule_sets"]

# List all rule sets
print("Available rule sets:\n")
for i, rule in enumerate(rule_sets):
    print(f"{i+1}. {rule['name']}")

set_choice = int(input("\nPick a rule set number to load: ")) - 1
selected_set = rule_sets[set_choice]

# Load selected YAML rule file
with open(selected_set["file"], "r") as f:
    rules = yaml.safe_load(f)

scenarios = rules["scenarios"]

# Display individual scenarios
print(f"\nLoaded: {selected_set['name']}\n")
for i, s in enumerate(scenarios):
    print(f"{i+1}. {s['name']} – {s['description']}")

print(f"{len(scenarios)+1}. Run all scenarios in this set")

scenario_choice = int(input("\nPick a scenario number to run: ")) - 1

# Make sure logs/ exists
os.makedirs("logs", exist_ok=True)
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
logfile = f"logs/run_{selected_set['name'].replace(' ', '_').lower()}_{timestamp}.json"
log = []

def run_scenario(s):
    print(f"\n--- Running: {s['name']} ---\n")
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3",
            "prompt": s["prompt"],
            "stream": False
        }
    )
    output = response.json()["response"]
    print(output)
    print("\n----------------------------\n")

    result = {
        "rule_set": selected_set["name"],
        "scenario": s["name"],
        "prompt": s["prompt"],
        "response": output,
        "timestamp": datetime.now().isoformat()
    }
    log.append(result)

# Run one or all
if scenario_choice == len(scenarios):
    for s in scenarios:
        run_scenario(s)
else:
    run_scenario(scenarios[scenario_choice])

# Write log
with open(logfile, "w") as f:
    json.dump(log, f, indent=2)

print(f"\n📝 Log saved to {logfile}")

