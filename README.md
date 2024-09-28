# dnd_engine: intoxicated by LitRPG

## Install

```
pip install git+https://github.com/AlexeyNilov/dnd_engine.git
```

## Development

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
python -m flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
python -m flake8 . --count --exit-zero --statistics
python -m pytest test/test_*.py
mypy .
black dnd_engine/ sample/ test/
```
