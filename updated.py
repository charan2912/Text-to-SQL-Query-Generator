from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import sqlite3
import google.generativeai as genai
import tempfile

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(question, prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content([prompt[0], question])
    sql_query = response.text.strip()
    return sql_query

def read_sql_query(sql, db_path):
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    try:
        print(f"Executing SQL query: {sql}")  # Debugging statement
        cur.execute(sql)
        rows = cur.fetchall()
    except sqlite3.OperationalError as e:
        print(f"SQL Error: {e}")
        rows = []
    finally:
        con.commit()
        con.close()
    return rows

def handle_uploaded_database(uploaded_file):
    # Create a temporary file to save the uploaded database
    with tempfile.NamedTemporaryFile(delete=False, suffix=".db") as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        return tmp_file.name

def get_database_description(db_path):
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    description = []

    # Get table names
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cur.fetchall()
    
    for table in tables:
        table_name = table[0]
        description.append(f"Table: {table_name}")
        
        # Get columns for each table
        cur.execute(f"PRAGMA table_info({table_name});")
        columns = cur.fetchall()
        column_details = ", ".join([f"{col[1]} ({col[2]})" for col in columns])
        description.append(f"  Columns: {column_details}")
    
    con.close()
    return "\n".join(description)

prompt = [
    """
    You are an expert in converting English questions to SQL queries or providing database explanations. 
    The SQL database provided has various tables with columns. Generate only the SQL query needed to answer the following question. 
    If the question asks for database structure or explanation, provide a summary of tables and columns in the database. 

    For example:
    - Question: How many records are in the database?
      SQL: SELECT COUNT(*) FROM <table_name>;
    
    - Question: Tell me all the students studying in DL class.
      SQL: SELECT * FROM <table_name> WHERE CLASS = 'DL';
    
    - Question: What is the database about?
      Explanation: The database contains tables with columns such as NAME, CLASS, and SECTION. Details of each table and its columns are provided.
    """
]

st.set_page_config(page_title="Database Query App")
st.header("Upload Your Database and Ask SQL Questions")

# File uploader
uploaded_file = st.file_uploader("Choose an SQLite database file", type="db")

if uploaded_file:
    # Handle file upload and store the database
    db_path = handle_uploaded_database(uploaded_file)

    question = st.text_input("Input:", key="input")
    submit = st.button("Get Response")

    if submit:
        response = get_gemini_response(question, prompt)
        print(f"Generated Response: {response}")

        # Handle database description requests
        if "what is the database about" in question.lower():
            description = get_database_description(db_path)
            st.subheader("Database Description")
            st.write(description)
        elif response.lower().startswith("select"):
            result = read_sql_query(response, db_path)
            st.subheader("Query Results")
            for row in result:
                st.write(row)
        else:
            st.subheader("Error")
            st.write("The model generated an invalid SQL query or explanation.")
else:
    st.write("Please upload an SQLite database file to proceed.")
