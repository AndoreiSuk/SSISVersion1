import pandas as pd
import os
# Will use this for the absolute path to the directory where database.py is located. Instead of /folder/filename.py
DB_Directory = os.path.dirname(os.path.abspath(__file__))
class Database:
    def __init__(self, filename: str, columns: list):
        self.columns = columns
        self.filename = os.path.join(DB_Directory, f"{filename}.csv")
        self.initialize()
    def initialize(self):
        # This method creates the CSV file with headers if it doesn't exist.
        if not os.path.exists(self.filename):
            try:
                df = pd.DataFrame(columns=self.columns)
                df.to_csv(self.filename, index=False)
            except Exception as e:
                print(f"Error initializing database file {self.filename}: {e}")
    def get_all(self):
        # Retrieves all records from the CSV file.
        # Returns a list of dictionaries, or an empty list if an error occurs or file is empty.
        try:
            if not os.path.exists(self.filename):
                print(f"Warning: Data file {self.filename} not found. Attempting to initialize.")
                self.initialize()
            if os.path.exists(self.filename) and os.path.getsize(self.filename) == 0:
                print(f"Warning: Data file {self.filename} is empty. Re-initializing with headers.")
                self.initialize()
            df = pd.read_csv(self.filename)
            return df.to_dict('records')
        except pd.errors.EmptyDataError:
            print(f"Warning: Data file {self.filename} is empty or contains no data. Returning empty list.")
            return []
        except FileNotFoundError:
            print(f"Error: Data file {self.filename} was not found. Returning empty list.")
            return []
        except Exception as e:
            print(f"An error occurred while reading {self.filename}: {e}. Returning empty list.")
            return []
    def check(self, id_to_check):
        try:
            df = pd.read_csv(self.filename)
            if 'ID' not in df.columns:
                return False
            # Make ID check case-insensitive for robustness when checking for duplicates
            return (df['ID'].astype(str).str.lower() == str(id_to_check).lower()).any()
        except (FileNotFoundError, pd.errors.EmptyDataError):
            return False
        except Exception as e:
            print(f"Error checking ID in {self.filename}: {e}")
            return False
    def insert_one(self, data: dict):
        try:
            processed_data = {key: str(value) for key, value in data.items()}
            df = pd.read_csv(self.filename)
            if not all(col in df.columns for col in self.columns):
                df = pd.DataFrame(columns=self.columns)
            new_df = pd.DataFrame([processed_data], columns=self.columns)
            df = pd.concat([df, new_df], ignore_index=True)
            df.to_csv(self.filename, index=False)
            return True
        except Exception as e:
            print(f"Error inserting data into {self.filename}: {e}")
            return False
    def edit(self, original_id: str, new_data: dict):
        try:
            df = pd.read_csv(self.filename)
            if 'ID' not in df.columns:
                print(f"Error editing {self.filename}: 'ID' column missing.")
                return False

            match_idx = -1
            # Find the row using original_id, performing a case-insensitive search
            for index, row_id in enumerate(df['ID'].astype(str)):
                if row_id.lower() == str(original_id).lower():
                    match_idx = index
                    break

            if match_idx != -1:
                processed_new_data = {key: str(value) for key, value in new_data.items()}
                new_id_from_data = processed_new_data.get('ID')

                # Check for new ID conflicts:
                # If the new ID is different from the original ID (case-insensitively)
                # AND it already exists for a *different* record, then block the change.
                if new_id_from_data and new_id_from_data.lower() != original_id.lower():
                    existing_ids_lower = df['ID'].astype(str).str.lower()
                    # Check if the new ID conflicts with any other ID *excluding* the row being edited
                    # Use a boolean mask for filtering the DataFrame before checking for existence
                    other_records_mask = [i != match_idx for i in range(len(df))]
                    if (existing_ids_lower[other_records_mask] == new_id_from_data.lower()).any():
                        print(f"Error editing {self.filename}: New ID '{new_id_from_data}' (case-insensitive) already exists for another record.")
                        return False

                for key, value in processed_new_data.items():
                    if key in df.columns:
                        df.loc[match_idx, key] = value # Update with new value, including ID if changed
                df.to_csv(self.filename, index=False)
                return True
            else:
                print(f"Error editing {self.filename}: Original ID '{original_id}' not found.")
                return False
        except Exception as e:
            print(f"Error editing data in {self.filename}: {e}")
            return False
    def remove(self, id_to_remove):
        try:
            df = pd.read_csv(self.filename)
            if 'ID' not in df.columns:
                print(f"Error removing from {self.filename}: 'ID' column missing.")
                return False # Cannot remove if ID column doesn't exist
            
            initial_len = len(df)
            # Perform case-insensitive removal
            df_filtered = df[df['ID'].astype(str).str.lower() != str(id_to_remove).lower()]
            
            if len(df_filtered) < initial_len:
                df_filtered.to_csv(self.filename, index=False)
                return True
            print(f"Error removing from {self.filename}: ID '{id_to_remove}' not found.")
            return False # ID not found
        except Exception as e:
            print(f"Error removing data from {self.filename}: {e}")
            return False
    def get_ids(self):
        all_records = self.get_all()
        rows = ["No Selection"]
        for row in all_records:
            if isinstance(row, dict) and "ID" in row:
                rows.append(str(row["ID"]))
        # Use dict.fromkeys to preserve order while removing duplicates
        return list(dict.fromkeys(rows))
    def get_program_ids(self):
        return self.get_ids()
    def get_college_ids(self):
        return self.get_ids()
# example ni sha
programs = Database('programs', ["ID", "NAME", "COLLEGE"])
students = Database('students', ["ID", "FIRSTNAME", "LASTNAME", "SEX", "PROGRAM", "YEAR LEVEL"])
colleges = Database('colleges', ["ID", "NAME"])