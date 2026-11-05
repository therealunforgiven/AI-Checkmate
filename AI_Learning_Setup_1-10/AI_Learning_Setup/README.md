# AI Learning Pipeline - Setup Guide (1-10 Elementary)

## Folder Structure
```
AI_Learning/
├── scripts/
│   ├── 01_elementary/script.py
│   ├── 02_elementary/script.py
│   ├── ...
│   └── 10_elementary/script.py
├── outputs/          # Script outputs go here
├── reports/          # JSON reports after each run
├── logs/
└── runner.py         # Main pipeline runner
```

## Quick Setup Commands (Linux)

```bash
# Create the base folder
mkdir -p ~/AI_Learning
cd ~/AI_Learning

# Copy the files from the email/zip into this folder
# Then run:

python3 runner.py
```

## Windows
Same structure. Use Python from the command prompt or PowerShell:
```
python runner.py
```

## What the Runner Does
- Finds all folders in `scripts/` that start with numbers (01_, 02_, etc.)
- Runs the `.py` file inside each one, in order
- Saves stdout and stderr to `outputs/<folder>/`
- Writes a JSON report to `reports/<folder>_report.json` with status, runtime, and preview of output
- Continues to the next script even if one fails

## Adding More Scripts Later
1. Create a new folder like `scripts/11_highschool/`
2. Put your `script.py` inside it
3. Run `python3 runner.py` again — it will pick up the new one automatically

## Backup
Keep this entire `AI_Learning` folder (or at least the scripts + runner.py) backed up to Google Drive. If you need to start over, just re-copy the folder and run the runner.

## Notes
- Default timeout per script is 1 hour. Edit runner.py to change it.
- Scripts run in their own folder, so relative file paths work.
- Reports are simple JSON — easy to read or parse later.
