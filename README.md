ConsciousDay Agent – Morning Reflection App

ConsciousDay Agent is a Streamlit-based journaling and daily planning tool designed to help users reflect on their mental and emotional state each morning and receive a tailored strategy for the day.

Features:

* Morning journal input
* Dream interpretation input
* Daily intention setting
* Top 3 priorities field
* AI-generated reflection summary and suggested strategy
* View and retrieve past reflections by date
* Simple and clean UI

Technologies Used:

* Python
* Streamlit
* LangChain
* OpenRouter API
* SQLite for local data storage

Folder Structure:

* app.py – Main application script
* db/database.py – Handles database operations
* agent/agent.py – AI logic and prompt formatting

How to Run Locally:

1. Clone the repository
2. Create and activate a virtual environment
3. Install required packages
4. Add an .env file with your OpenRouter API key
5. Run the app using the command: streamlit run app.py

Example .env file:

OPENROUTER\_API\_KEY=your\_openrouter\_api\_key\_here

Deployment:

To deploy on Streamlit Cloud:

* Push the code to a public GitHub repository
* Add the OpenRouter API key in Streamlit Cloud under Settings > Secrets
* Deploy the app directly from the repository

Usage Notes:

* Login is not required
* Reflections are stored using a local SQLite database
* AI output is generated dynamically based on user input

License:

This project is intended for educational and personal use only.
