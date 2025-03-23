# StudyBuddy

A text-to-speech application that converts written content into high-quality audio using OpenAI's text-to-speech API. This tool reduces mental fatigue by eliminating the need to mentally vocalize text while reading, allowing users to consume more content without getting tired.

Key features:
- Convert text to speech with high-quality AI voices
- Simple Streamlit interface for easy interaction

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
