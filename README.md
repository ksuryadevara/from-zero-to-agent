# From Zero to Agent
## Understanding AI by Building It

Complete source code for the 12-part blog series published on Medium.

> By the end of this series you will have built a working AI agent
> from scratch — using nothing but Python and NumPy. No frameworks.
> No black boxes. Every operation visible, every decision justified,
> every line of code written and understood by you.

---

## Series Posts

| Post | Title | Status |
|------|-------|--------|
| 1 | What Your Training Didn't Tell You | ✅ Published |
| 2 | The Hardest Problem Is Also the Most Obvious | 🔜 Coming Soon |
| 3 | How a Machine Reads | 🔜 Coming Soon |
| 4 | Attention — The Idea That Changed Everything | 🔜 Coming Soon |
| 5 | One Head Is Never Enough | 🔜 Coming Soon |
| 6 | The Parts Nobody Talks About | 🔜 Coming Soon |
| 7 | The Reader — Building the Encoder | 🔜 Coming Soon |
| 8 | The Writer — Building the Decoder | 🔜 Coming Soon |
| 9 | The Complete Machine | 🔜 Coming Soon |
| 10 | Seeing What the Machine Sees | 🔜 Coming Soon |
| 11 | From Transformer to Agent — Built from Scratch | 🔜 Coming Soon |
| 12 | Where to Go from Here | 🔜 Coming Soon |

Code modules are added to the `code/` folder as each post publishes.
A new post publishes every ten days.

Read the full series on Medium:
[From Zero to Agent on Medium](https://medium.com/@ksuryadevara)

---

## Setup

### What You Need
- Python 3.10 or above — download from python.org
- VS Code — download from code.visualstudio.com
- Python extension inside VS Code — install from the Extensions panel

### Step by Step

**1. Clone the repository**
```bash
git clone https://github.com/ksuryadevara/from-zero-to-agent
cd from-zero-to-agent
```

**2. Create a virtual environment**
```bash
python -m venv venv
```

**3. Activate it**

Windows:
```bash
venv\Scripts\activate
```

Mac / Linux:
```bash
source venv/bin/activate
```

You will know it worked when you see `(venv)` at the start
of your terminal prompt.

**4. Install the only dependency**
```bash
pip install numpy
```

**5. Select your interpreter in VS Code**

`Ctrl+Shift+P` → type **Python: Select Interpreter**
→ choose the option that shows `venv` in the path
→ it will look like `Python 3.10.10 ('venv')`

**6. Run a module (from Post 2 onwards)**
```bash
python code/1_tokenizer.py
```

---

## Troubleshooting

**'python' is not recognised**
Try `python3` instead. Or verify Python is installed correctly
at python.org — version 3.10 or above.

**venv\Scripts\activate not recognised on Windows**
Run this once in your terminal first:
```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```
Then try activating again.

**ModuleNotFoundError: No module named 'numpy'**
Your venv is probably not activated.
Check for `(venv)` at the start of your terminal prompt.
If it is missing, activate first then run `pip install numpy` again.

**Output looks different from what the blog post shows**
Check your Python version:
```bash
python --version
```
This series was developed on Python 3.10.10.
Any version 3.10 or above should work correctly.

**Still stuck?**
Open an issue on this repository.
Include your exact error message, which module you were running,
your operating system, and your Python version.

---

## About

This series grew out of a simple problem — most explanations of
AI systems are either too simplified to be useful or too academic
to be accessible. This is an attempt to explain the Transformer
architecture completely and honestly, built from scratch, for people
who work with data seriously and are now being asked to build with AI.

---

*Karthik Suryadevara*
*Founder, IoTantra Technologies, Hyderabad*
*github.com/ksuryadevara*
```

---