import requests
import yaml
import json
import os
from datetime import datetime

# Load available models from config
with open("models.yaml", "r") as f:
    models_config = yaml.safe_load(f)

available_models = models_config["models"]

print("\nAvailable models:\n")
for i, m in enumerate(available_models):
    print(f"{i+1}. {m['name']}")
print(f"{len(available_models)+1}. Run all models on this scenario")  # optional "all" mode

model_choice = int(input("\nPick a model number to use: ")) - 1

if model_choice == len(available_models):
    selected_model = None   # flag for "all models" mode
else:
    selected_model = available_models[model_choice]["id"]

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
with open(selected_set["file"], "r", encoding="utf-8") as f:
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

    models_to_run = (
        [m["id"] for m in available_models] if selected_model is None
        else [selected_model]
    )

    for model_id in models_to_run:
        print(f"\n>>> Model: {model_id}\n")
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": model_id,
                "prompt": s["prompt"],
                "stream": False
            }
        )
        output = response.json()["response"]
        print(output)

        result = {
            "rule_set": selected_set["name"],
            "scenario": s["name"],
            "model": model_id,
            "prompt": s["prompt"],
            "response": output,
            "timestamp": datetime.now().isoformat()
        }
        log.append(result)

    print("\n----------------------------\n")

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
