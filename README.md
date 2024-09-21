# dnd_engine: intoxicated by litrpg

## Install

python 3.9+ is required, 3.11+ is recommended

```
git clone https://github.com/AlexeyNilov/dnd_engine.git
cd dnd_engine
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp conf/settings.py.sample conf/settings.py # And add the settings if needed
pre-commit install
```

Run linters and tests

```
flake8 . --extend-exclude .venv,.pytest_cache,.mypy_cache --count --select=E9,F63,F7,F82 --show-source --statistics
flake8 . --extend-exclude .venv,.pytest_cache,.mypy_cache --count --exit-zero --max-complexity=5 --max-line-length=128 --statistics --ignore=E402
python -m pytest test/test_*.py
python -m mypy .
```
