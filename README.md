Simple Calculator

This repository contains a small, safe command-line calculator implemented in `python.py`.

Usage:

Run the REPL:

```powershell
python python.py
```

Evaluate a single expression:

```powershell
python python.py -e "2 + 2 * sin(pi/2)"
```

Notes:
- The evaluator is intentionally restricted: it only allows numeric constants, basic arithmetic operators, calls to math functions (from the `math` module), and a few safe builtins like `abs` and `round`.
- Trying to use attribute access, importing, or other Python features will raise an error.
