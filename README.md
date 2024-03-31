# Damage simulator
Simulates 5e character damage and hit % for various weapons. Characters are hardcoded to campaign.

# Setup
Requires Python >= 3.8
```
python -m venv .venv
.venv/bin/activate
pip install -r requirements.txt
```

# Running
1. Ensure virtual environment is active by running `.venv/bin/activate`
2. `python damage.py`

# Tweaking
- Character attacks and modifiers are customized in `damage.py` in functions with character names.
- Add and edit weapons in `weapons.py`.
- Uncomment the `compute_matrices()` calls to generate damage and attack tables vs. AC.
- Reduce `SIMS` in `damage.py` to shorten runtime, particularly when computing matrices.
