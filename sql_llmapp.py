from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import sqlite3
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def get_gemini_response(question,prompt):
    model=genai.GenerativeModel("gemini-pro")
    response=model.generate_content([prompt[0],question])
    return response.text

def read_sql_query(sql, db):
    
        con = sqlite3.connect(db)
        cur = con.cursor()
        print(f"Executing SQL query: {sql}")  # Debugging statement
        cur.execute(sql)
        rows = cur.fetchall()
        con.commit()
        con.close()
        for row in rows:
            print(row)
        return rows
    

prompt=[
    """
    You are an expert in converting English questions to SQL queries. The SQL database has the name STUDENT and has the following columns: NAME, CLASS, SECTION,MARKS.
    Generate only the SQL query based on the user's question without any additional explanation or formatting. Do not include any comments or unnecessary text.
    For example:
    Question: How many entries of records are present?
    SQL: SELECT COUNT(*) FROM STUDENT;
    
    Question: Tell me all the students studying in DL class?
    SQL: SELECT * FROM STUDENT WHERE CLASS = 'DL';
    
    also the sql code should not have ''' in beginning or ending and sql word in the output
    """

]



st.set_page_config(page_title="I can Retrive Any SQL Query")
st.header("Gemini App to Retrive SQl Data")
question=st.text_input("Input:",key="input")
submit=st.button("Get Response")


if submit:
    response=get_gemini_response(question,prompt)
    response=read_sql_query(response,"student.db")
    st.subheader("The Response is")
    for row in response:
        print(row)
        st.header(row)