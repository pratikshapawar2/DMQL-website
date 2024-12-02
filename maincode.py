import streamlit as st
import sqlite3
import pandas as pd
import os
import threading

# Lock for database operations
db_lock = threading.Lock()

# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Define the path to the SQLite database in /tmp directory (writable in Streamlit Cloud)
sqlite_db = "/tmp/mydatabase.db"

# SQL file paths (inside sql_queries directory)
create_sql_path = os.path.join(current_dir, "sql_queries", "create.sql")
alter_sql_path = os.path.join(current_dir, "sql_queries", "alter.sql")
# Add other SQL files if needed
# For example:
# load_sql_path = os.path.join(current_dir, "sql_queries", "load.sql")

# Directory containing the CSV files
csv_directory = os.path.join(current_dir, "data_files")

# Function to execute SQL file
def execute_sql_file(file_path):
    try:
        conn = sqlite3.connect(sqlite_db, check_same_thread=False)
        cursor = conn.cursor()

        # Read and execute the SQL file
        with open(file_path, 'r') as sql_file:
            sql_script = sql_file.read()
        cursor.executescript(sql_script)
        conn.commit()
        print(f"SQL script {file_path} executed successfully!")
    except Exception as e:
        print(f"An error occurred while executing the SQL file {file_path}: {e}")
    finally:
        cursor.close()
        conn.close()

# Initialize the database
def init_db():
    # Always initialize the database on app start
    execute_sql_file(create_sql_path)
    # If you have other SQL files, execute them as needed
    # execute_sql_file(load_sql_path)
    execute_sql_file(alter_sql_path)
    load_csv_to_sqlite(csv_directory, sqlite_db)

def load_csv_to_sqlite(csv_directory, sqlite_db):
    conn = sqlite3.connect(sqlite_db, check_same_thread=False)
    cursor = conn.cursor()
    try:
        for filename in os.listdir(csv_directory):
            if filename.endswith(".csv"):
                file_path = os.path.join(csv_directory, filename)
                table_name = os.path.splitext(filename)[0]
                df = pd.read_csv(file_path)
                df.to_sql(table_name, conn, if_exists='replace', index=False)
                print(f"Loaded {filename} into table {table_name}.")
    except Exception as e:
        print(f"An error occurred while loading CSV files: {e}")
    finally:
        cursor.close()
        conn.close()

# Function to execute SQL queries
def execute_query(query):
    with db_lock:
        conn = sqlite3.connect(sqlite_db, check_same_thread=False)
        try:
            cursor = conn.cursor()
            if query.strip().upper().startswith('SELECT'):
                cursor.execute(query)
                rows = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]
                df = pd.DataFrame(rows, columns=columns)
                return df, None
            else:
                cursor.execute(query)
                conn.commit()
                return None, f"Query executed successfully. {cursor.rowcount} rows affected."
        except Exception as e:
            st.error(f"An error occurred: {e}")
            return None, f"An error occurred: {e}"
        finally:
            cursor.close()
            conn.close()

# Streamlit app
st.title("SQLite Database Management App")

# Initialize the database every time the app runs (due to /tmp being cleared on restart)
init_db()

# Sidebar menu
menu = ["View Tables", "Execute Query"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "View Tables":
    st.subheader("Available Tables")
    with db_lock:
        conn = sqlite3.connect(sqlite_db, check_same_thread=False)
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            table_list = [table[0] for table in tables]
            st.write("Tables in the database:", table_list)

            selected_table = st.selectbox("Select a table to view", table_list)
            if selected_table:
                query = f"SELECT * FROM {selected_table} LIMIT 100"
                df, _ = execute_query(query)
                if df is not None:
                    st.dataframe(df)
        except Exception as e:
            st.error(f"An error occurred: {e}")
        finally:
            conn.close()

elif choice == "Execute Query":
    st.subheader("Run SQL Query")
    query = st.text_area("Enter your SQL query:")
    if st.button("Execute"):
        if query.strip():
            df_result, message = execute_query(query)
            if message:
                st.info(message)
            if df_result is not None and not df_result.empty:
                st.dataframe(df_result)
            elif df_result is not None:
                st.write("Query executed successfully. No results to display.")
        else:
            st.warning("Please enter a SQL query.")
