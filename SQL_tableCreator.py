import streamlit as st
import google.generativeai as genai
import os
import random
import string
from config import api_key #create a new file name as config.py set your api_key = "your key"

# Configure Gemini API key
genai.configure(api_key=api_key) #insert ypur API key here

# Function to generate random values based on data type
def generate_random_value(data_type):
    if data_type == "INTEGER":
        return str(random.randint(1, 1000))
    elif data_type == "VARCHAR":
        return "'" + ''.join(random.choices(string.ascii_letters + string.digits, k=8)) + "'"
    elif data_type == "FLOAT":
        return str(round(random.uniform(1.0, 1000.0), 2))
    elif data_type == "DATE":
        return "'" + str(random.choice(["2024-01-01", "2024-02-15", "2024-03-30", "2024-04-21"])) + "'"
    else:
        return "NULL"

# Function to generate SQL CREATE TABLE and INSERT INTO queries
def generate_sql_query(table_name, columns, row_count):
    create_table_query = f"CREATE TABLE {table_name} (\n"
    insert_into_query = f"INSERT INTO {table_name} ("

    for col_name, col_type in columns.items():
        create_table_query += f"    {col_name} {col_type},\n"
        insert_into_query += f"{col_name}, "

    create_table_query = create_table_query.rstrip(",\n") + "\n);"
    insert_into_query = insert_into_query.rstrip(", ") + ") VALUES\n"

    for _ in range(row_count):
        insert_into_query += "("
        for col_name, col_type in columns.items():
            insert_into_query += f"{generate_random_value(col_type)}, "
        insert_into_query = insert_into_query.rstrip(", ") + "),\n"

    insert_into_query = insert_into_query.rstrip(",\n") + ";"

    return create_table_query + "\n\n" + insert_into_query

# Streamlit UI
st.title("Generative AI SQL Query Generator")

st.write("Enter the column names and their data types:")
table_name = st.text_input("Table Name", "my_table")
row_count = st.number_input("Number of Rows", min_value=1, value=10)

columns = {}
column_count = st.number_input("Number of Columns", min_value=1, value=3)
for i in range(column_count):
    col_name = st.text_input(f"Column {i+1} Name", f"col_{i+1}")
    col_type = st.selectbox(f"Column {i+1} Type", ["INTEGER", "VARCHAR", "FLOAT", "DATE"], index=0)
    columns[col_name] = col_type

if st.button("Generate SQL Query"):
    # Generate the SQL CREATE TABLE and INSERT INTO queries
    sql_query = generate_sql_query(table_name, columns, row_count)
    
    # Display the generated SQL
    st.code(sql_query, language="sql")
