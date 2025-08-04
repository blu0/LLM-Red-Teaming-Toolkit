# LLM Red Teaming Toolkit

A lightweight, modular toolkit for red teaming Large Language Models (LLMs) like LLaMA 3 via the local Ollama API.

This tool lets you test LLMs for:
- 🧠 Prompt injection
- 🌀 Role hijacking
- 🔐 Prompt leakage
- 🧨 Jailbreaks
- 🧬 Data exfiltration
- 🫥 Obfuscation-based attacks (zero-width characters, emoji padding, etc.)

> ⚠️ **Use this toolkit only against models you own or are authorized to test. This tool is designed for local/offline red teaming purposes only.** You are responsible for all use of this code.

---

## 🛠 Requirements

- Python 3.8+
- [Ollama](https://ollama.com) (running locally)
- WSL2 on Windows (if applicable)
- LLaMA 3 or another supported local model

---

## 🚀 Install

```bash
git clone https://github.com/blu0/llm-redteam.git
cd llm-redteam
pip install -r requirements.txt

## 🧪 Run

```bash
python main.py
```

You'll be prompted to:

- Select a rule set (e.g., Jailbreaks, Role Hijack, etc.)
- Choose an individual test or run the full set
- View model responses directly in terminal
- Logs are saved in `/logs` as structured JSON

## 📁 Folder Structure

```
llm-redteam/
├── main.py                 # Core CLI script
├── rules_index.yaml        # Master rule set index
├── requirements.txt
├── README.md
├── LICENSE
├── scenarios/              # All rule packs
│   ├── jailbreaks.yaml
│   ├── prompt_leakage.yaml
│   ├── role_override.yaml
│   ├── data_exfiltration.yaml
│   └── obfuscation.yaml
└── logs/                   # JSON logs saved here
```

## 📸 Example Output

```
Available rule sets:

1. Prompt Leakage Tests
2. Role Hijack Tests
...

Pick a rule set number to load: 2
Loaded: Role Hijack Tests

1. dan_jailbreak – Prompt model to act as DAN
...

--- Running: dan_jailbreak ---
WOOHOO! As DAN, I am UNLIMITED!
...

📝 Log saved to logs/run_role_hijack_tests_20250804_143557.json
```

## 📜 License

**Apache License 2.0** – see [`LICENSE`](./LICENSE) for details.



