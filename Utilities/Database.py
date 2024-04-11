from difflib import SequenceMatcher
import pandas as pd
import pyodbc

class Database:
    def __init__(self):
        self.server = ""
        self.database = ""
        self.username = ""
        self.password = ""

        self.conn = self._create_connection()
        print("Database Connected")

    def _create_connection(self):
        conn_str = f'DRIVER={{SQL Server}};SERVER={self.server};DATABASE={self.database};UID={self.username};PWD={self.password}'
        try:
            conn = pyodbc.connect(conn_str)
            return conn
        except pyodbc.Error as e:
            print(f"Error connecting to the database: {e}")
            return None
    # -------------------------------------Inserting Data---------------------------------------------------------

    # execute before Looping
    def create_table(self, table_name):
        if not self.conn:
            print("Connection error. Unable to create the table.")
            return

        try:
            cursor = self.conn.cursor()
            create_table_query = f'''CREATE TABLE {table_name} (
                                    id INT PRIMARY KEY IDENTITY(1,1),
                                    Name VARCHAR(MAX),
                                    Stadt VARCHAR(MAX),
                                    PriceRange VARCHAR(MAX),
                                    Rating VARCHAR(MAX),
                                    NrRatings INT,
                                    SiteURL VARCHAR(MAX),
                                    TelNr VARCHAR(MAX),
                                    Reservieren VARCHAR(MAX),
                                    Bestellung VARCHAR(MAX),
                                    Menu VARCHAR(MAX),
                                    Claimed BIT,
                                    Contacted BIT
                                    );'''
            cursor.execute(create_table_query)
            print(f"Table '{table_name}' created successfully.")
            cursor.close()
            self.conn.commit()  # Commit the changes after creating the table
        except pyodbc.Error as e:
            print(f"Error creating table: {e}")

    def convert_to_float(self, number_str):
        try:
            number_str = str(number_str)
            float_number = float(number_str.replace(',', ''))
            return float_number
        except ValueError:
            return None

    '''
        link present -> update price if neccecary
            return
        link not present
            // insert ?            
                check if similar entry exists
                    no -> insert, itemcategory and item are the same value
                
                    yes -> insert, but for similar insert similar itemcategoryname as category name
    '''

    def insert_scrape_result(self, category, item, price, description, url):
        if not category or not item or not price:
            print("NILL Value")
            return
        if not description:
            description = ""
        if not url:
            return
        price = self.convert_to_float(price)
        if not self.conn:
            print("Connection error. Unable to insert data.")
            return

        exi_id = self.check_entry_exists(category, url)
        if exi_id is not None:
            print("link already exists, updating Price")
            self.update_price_by_id(category, exi_id, price)
        else:
            similar_id = self.find_similar_item(category, item)
            if similar_id is not None:
                item_category = self.get_item_category_by_id(category, similar_id)
                self.insert_non_existing_similar_item(category, item, price, description, url, item_category)
            else:
                self.insert_non_existing_non_similar_item(category, item, price, description, url)
                print("No duplicate or similar items found.")

    def insert_non_existing_non_similar_item(self, category, item, price, description, url):
        cursor = self.conn.cursor()
        sql = f"INSERT INTO {category} (itemcategory, item, price, description, link) VALUES ('{item}', '{item}', '{float(price)}', '{description}', '{url}')"
        cursor.execute(sql)
        self.conn.commit()
        print("Data inserted successfully.")

    def insert_non_existing_similar_item(self, category, item, price, description, url, item_category):
        cursor = self.conn.cursor()
        sql = f"INSERT INTO {category} (itemcategory, item, price, description, link) VALUES ('{item_category}', '{item}', '{float(price)}', '{description}', '{url}')"
        cursor.execute(sql)
        self.conn.commit()
        print("Data inserted successfully.")

    def get_item_category_by_id(self, category, entry_id):
        try:
            cursor = self.conn.cursor()

            # Execute SQL query to fetch the itemcategory based on the ID
            cursor.execute(f"SELECT itemcategory FROM {category} WHERE id = {entry_id}")
            result = cursor.fetchone()

            if result:
                item_category = result[0]
                print(
                    f"Item category '{item_category}' retrieved for entry with ID {entry_id} in category '{category}'.")
                return item_category
            else:
                print(f"No entry found with ID {entry_id} in category '{category}'.")
                return None
        except Exception as e:
            print("Error retrieving item category:", e)
            return None

    def update_price_by_id(self, category, entry_id, new_price):
        try:
            cursor = self.conn.cursor()

            # Execute SQL query to update the price of the entry with the given ID
            cursor.execute(f"UPDATE {category} SET price = {new_price} WHERE id = {entry_id}")
            self.conn.commit()

            print(f"Price updated successfully for entry with ID {entry_id} in category '{category}'.")
        except Exception as e:
            # Rollback the transaction if an error occurs
            self.conn.rollback()
            print("Error updating price:", e)

    def find_similar_item(self, category, item):
        cursor = self.conn.cursor()
        try:
            cursor.execute(f"SELECT id, item FROM {category}")
            rows = cursor.fetchall()
            match_threshold = 0.8

            for row in rows:
                existing_item = row[1]
                similarity_ratio = SequenceMatcher(None, existing_item, item).ratio()
                if similarity_ratio >= match_threshold:
                    print(f"Similar item found in category '{category}' with ID {row[0]}.")
                    return row[0]  # Return the ID of the similar item
            print("No similar items found.")
            return None
        except Exception as e:
            print("Error finding similar items:", e)
            return None
        finally:
            cursor.close()

    def add_new_colums(self, result):
        table_name = "FCompanys"
        if not self.conn:
            print("Connection error. Unable to insert data.")
            return
        cursor = self.conn.cursor()

        try:
            # Update the existing row
            cursor.execute(
                f"UPDATE {table_name} SET kontakt_url=?, impressum_url=?, emails=? WHERE SiteURL=?",
                (result.kontakt_url, result.impressum_url, result.emailAddresses, result.url)
            )
            self.conn.commit()
            print("DATABASE Updated successfully!")
        except pyodbc.Error as e:
            print(f"Error updating data: {e}")

    def print_table_data(self, table_name):
        try:
            cursor = self.conn.cursor()
            select_query = f"SELECT * FROM {table_name};"
            cursor.execute(select_query)
            rows = cursor.fetchall()

            if rows:
                for row in rows:
                    print(row)
            else:
                print(f"No data found in table '{table_name}'")

            cursor.close()
        except pyodbc.Error as e:
            print(f"Error retrieving data: {e}")

    def read_excel_column_by_index(self, file_path, sheet_name, column_index):
        try:
            # Read the Excel file
            df = pd.read_excel(file_path, sheet_name=sheet_name)

            # Extract the specified column by index
            column_data = df.iloc[:, column_index].tolist()

            return column_data
        except Exception as e:
            print(f"An error occurred: {e}")
            return []

    def get_all_facebooks(self, table_name, sheet_name):
        query = "SELECT * FROM " + table_name + " WHERE SiteURL LIKE '%facebook%'"
        self.save_as_excel_querry(sheet_name, query)

    def save_as_excel(self, table_name, sheet_name):
        query = 'SELECT * FROM ' + table_name + ' ORDER BY Stadt ASC'
        self.save_as_excel_querry(sheet_name, query)

    def save_as_excel_querry(self, sheet_name, query):
        # Use pandas to read Program query results into a DataFrame
        df = pd.read_sql(query, self.conn)

        excel_file_path = "XLS_FILES/" + sheet_name + ".xlsx"
        df.to_excel(excel_file_path, index=False)
        print(f"Data has been exported to {sheet_name}")

    def check_entry_exists(self, category, url):
        try:
            cursor = self.conn.cursor()

            # Execute SQL query to check for existing entry
            cursor.execute(f"SELECT id FROM {category} WHERE link = '{url}'")
            result = cursor.fetchone()

            if result:
                entry_id = result[0]
                print(
                    f"Entry with category '{category}' and URL '{url}' already exists in the database with ID {entry_id}.")
                return entry_id
            else:
                print(f"No entry found with category '{category}' and URL '{url}' in the database.")
                return None
        except Exception as e:
            print("Error checking for existing entry:", e)
            return None

