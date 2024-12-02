import streamlit as st
import sqlite3
import pandas as pd
import os

# Function to execute SQL file
def execute_sql_file(file_path):
    try:
        # Connect to SQLite database
        conn = sqlite3.connect('mydatabase.db')
        cursor = conn.cursor()
        
        # Read and execute the SQL file
        with open(file_path, 'r') as sql_file:
            sql_script = sql_file.read()
        cursor.executescript(sql_script)  # Use executescript for multiple SQL statements
        conn.commit()
        print("SQL script executed successfully!")
    except Exception as e:
        print(f"An error occurred while executing the SQL file: {e}")
    finally:
        cursor.close()
        conn.close()

# Initialize the database
def init_db():
    # Execute the create.sql file to set up the tables
    execute_sql_file("sql_queries/create.sql")  # Replace with the path to your create.sql file
 #   execute_sql_file("sql_queries/load.sql")
    execute_sql_file("sql_queries/alter.sql")
init_db()

# Directory containing the CSV files
csv_directory = "data_files"  # Replace with the path to your CSV directory

# SQLite database file
sqlite_db = "mydatabase.db"  # Replace with your SQLite database file name


def load_csv_to_sqlite(csv_directory, sqlite_db):
    # Connect to the SQLite database
    conn = sqlite3.connect(sqlite_db)
    cursor = conn.cursor()

    try:
        # Loop through all CSV files in the directory
        for filename in os.listdir(csv_directory):
            if filename.endswith(".csv"):  # Check if the file is a CSV
                file_path = os.path.join(csv_directory, filename)
                
                # Infer table name from the file name (remove .csv extension)
                table_name = os.path.splitext(filename)[0]

                # Load the CSV file into a Pandas DataFrame
                df = pd.read_csv(file_path)

                # Write the DataFrame to the SQLite database table
                # Use if_exists='replace' to overwrite existing data
                df.to_sql(table_name, conn, if_exists='replace', index=False)

                print(f"Loaded {filename} into table {table_name}.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        cursor.close()
        conn.close()

# Call the function to load CSV files into SQLite
load_csv_to_sqlite(csv_directory, sqlite_db)

# Function to execute SQL queries
def execute_query(query):
    conn = sqlite3.connect(sqlite_db)
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
        print(f"An error occurred: {e}")
        return None, f"An error occurred: {e}"
    finally:
        cursor.close()
        conn.close()


# Streamlit app
st.title("SQLite Database Management App")

# Initialize the database
init_db()

# Sidebar menu
menu = ["View Tables", "Execute Query", "Load CSV Data"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "View Tables":
    st.subheader("Available Tables")
    conn = sqlite3.connect(sqlite_db)
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