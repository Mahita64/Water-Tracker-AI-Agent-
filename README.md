
# AI Water Tracker System
AI Water Tracker so now you finally drink enough water.

## 🖥️ Using/Tech Stack:
Agentic AI, FastAPI, Uvicorn, SQLite, Google Gemini, Streamlit, Python

## 🚀 Create a Python 3.10 Conda Environment
```bash
conda create -n watertracker python=3.10 -y
conda activate watertracker
```

## 📦 Install Dependencies
Make sure you are inside the project folder (where requirements.txt exists), then run:
```bash
pip install -r requirements.txt
```


## 🔑 Set Up Your Google API Key
In the .env file in the project root, paste you Google API key where it says:
```bash
GOOGLE_API=PASTE_YOUR_API_KEY_HERE
```
This key is required for the AI hydration assistant using Gemini 2.5 Flash.



## 🧭 Run the FastAPI Backend
Start the API server using:
```bash
uvicorn src.api:app --reload
```
This launches your backend service that stores water intake in the database.


## 🍄 (Optional) Insert Dummy Hydration Data
Populate your database with random sample entries for the past 7 days:
```bash
python src/dummy.py
```


## 🤩 Run the Streamlit Dashboard
Launch the UI:
```bash
streamlit run dashboard.py
```
