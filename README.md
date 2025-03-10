# Live Impact - Sentiment Analysis of Feedback

This repository contains the code for the real-time sentiment analysis of participant feedback during the Nuit des Chercheurs event. It leverages Natural Language Processing (NLP) techniques to analyze and visualize the sentiment, satisfaction, and overall impact of various activities using interactive dashboards. This project won the 1st prize in the competition.

## Project Structure


## How to Use

### Step 1: Initialize the Feedback Database

To initialize the feedback database, run the `init_db.py` script located in the `data/` directory. This will set up the necessary database schema.

```bash
python data/init_db.py
```
### Step 2: Run the Backend Script

Next, navigate to the backend/ directory and run the app.py script to start the backend server. This will handle the data processing and sentiment analysis.

```bash
python backend/app.py

```

### Step 3: Run the Frontend Script

To launch the interactive frontend for visualizing the results, use Streamlit to run the app.py script located in the frontend/ directory. Open a new terminal window and run:

```bash
streamlit run frontend/app.py
```
This will start the frontend interface where you can view the real-time sentiment analysis results.
