# StudyBuddy

## Setup

First, copy `.env.template` to `.env` and provide missing values for variables.

Then:

### Unix-like

```sh
python -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
```

### Windows

```sh
python -m venv venv
venv\Scripts\activate
python -m pip install -r requirements.txt
```

## Run

```sh
python -m streamlit run tts.py
```
