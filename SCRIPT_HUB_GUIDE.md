# Script Hub - Run Your Python Scripts with a Nice UI

## 🚀 Quick Start (2 minutes)

### Step 1: Install Streamlit
```bash
pip install streamlit
```

### Step 2: Create a folder for your scripts
```bash
mkdir my_scripts
```

### Step 3: Run Script Hub
```bash
streamlit run script_hub.py
```

That's it! Your browser opens with a nice interface.

---

## 📁 Adding Your Scripts

Just drop your Python scripts in the `my_scripts` folder. They'll automatically appear in the dropdown!

### Your scripts should accept parameters in one of these ways:

**Option 1: Simple arguments** (easiest)
```python
import sys
topic = sys.argv[1] if len(sys.argv) > 1 else "default"
print(f"Researching {topic}...")
```

**Option 2: Named arguments** (recommended)
```python
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--topic', default='AI')
parser.add_argument('--depth', default='standard')
args = parser.parse_args()
print(f"Researching {args.topic} at {args.depth} depth...")
```

**Option 3: JSON input** (most flexible)
```python
import json
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--json', help='JSON parameters')
args = parser.parse_args()
if args.json:
    params = json.loads(args.json)
    print(f"Got parameters: {params}")
```

---

## ✨ What You Can Do

### 1. Run Your Scripts
- Select any script from dropdown
- Enter parameters (simple text, key=value, or JSON)
- Click Run
- See output in real-time

### 2. Edit & Format Output
- Take raw script output
- Apply templates (Executive Report, Technical Analysis, etc.)
- Edit manually to perfect it
- Save as Text, Markdown, or HTML

### 3. Use Templates
- Quick-start templates for common tasks
- Web scraping, API calls, data analysis
- Save and modify for your needs

### 4. Track History
- All runs are saved
- Reload previous outputs
- Download any past result

---

## 🎯 Example Workflow

1. **You have a script** that scrapes competitor data:
   ```python
   # competitor_scraper.py
   import sys
   company = sys.argv[1]
   print(f"Analyzing {company}...")
   # ... your scraping code ...
   print("Results: ...")
   ```

2. **Drop it in my_scripts folder**

3. **Run it from the UI**:
   - Select "competitor_scraper.py"
   - Enter: "Apple"
   - Click Run

4. **Edit the output**:
   - Go to "Edit Output" tab
   - Apply "Executive Report" template
   - Add your insights
   - Save as a polished PDF

---

## 💡 Pro Tips

- **Timeouts**: Scripts have 5-minute max runtime
- **Output**: Everything your script prints will appear
- **Errors**: Errors show up in red in the output
- **Templates**: Start with templates, then customize
- **Formats**: Save as .txt for simple, .md for formatted, .html for web

---

## 📝 The Example Script

I included `example_research_script.py` which shows:
- How to accept different parameter types
- How to create nice formatted output
- How to output JSON, Markdown, or Text

Try it:
1. Copy it to your my_scripts folder
2. Run with topic "renewable energy"
3. Edit the output
4. Save your report!

---

## 🔧 Troubleshooting

**Scripts not showing?**
- Make sure they're .py files
- Check the folder path is correct
- Refresh the page

**Script fails?**
- Check if all required packages are installed
- Look at the error message in output
- Test script in terminal first

**Want Claude AI in your scripts?**
```python
import requests
response = requests.post(
    "https://api.anthropic.com/v1/messages",
    json={"model": "claude-3-sonnet", "messages": [...]}
)
```

---

That's everything! Drop your scripts in, run them, edit outputs, save reports. No terminal needed! 🎉