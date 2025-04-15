# pyDSV/csvLoader.py

import csv
import pandas as pd


class CSVLoader:
    """
    A class to load and validate a CSV file into a pandas DataFrame.

    Attributes:
        csv_file_path (str): The path to the CSV file.
        df (pandas.DataFrame): The DataFrame containing the CSV data after successful loading.

    Methods:
        is_csv_valid(): Checks if the CSV file is readable and properly formatted.
        load_to_dataframe(): Loads the CSV file into a pandas DataFrame.
    """
    
    def __init__(self, csv_file_path):
        """
        Initializes the CSVLoader with the given CSV file path.

        Args:
            csv_file_path (str): The path to the CSV file to be loaded.

        Raises:
            ValueError: If the CSV file is malformed or unreadable.
        """
        self.csv_file_path = csv_file_path
        if not self.is_csv_valid():
            raise ValueError("CSV file is malformed or unreadable.")
        self.df = self.load_to_dataframe()

    def is_csv_valid(self):
        """
        Checks if the CSV file is readable and properly formatted.

        This method attempts to open and read the CSV file, checking for basic format issues such as
        missing or malformed rows. If the file cannot be read as a CSV, it returns False.

        Returns:
            bool: True if the CSV file is valid, False otherwise.
        """
        try:
            with open(self.csv_file_path, newline='') as csvfile:
                reader = csv.reader(csvfile)
                for _ in reader:
                    pass
            return True
        except csv.Error as e:
            print(f"CSV Error: {e}")
            return False
        except Exception as e:
            print(f"General Error: {e}")
            return False

    def load_to_dataframe(self):
        """
        Loads the CSV file into a pandas DataFrame.

        This method first checks that the CSV file has valid headers and the correct number of columns.
        After validation, it loads the CSV into a pandas DataFrame.

        Returns:
            pandas.DataFrame: The loaded DataFrame from the CSV file.

        Raises:
            ValueError: If the CSV file contains invalid or missing column headers, or rows with 
            mismatched columns.
        """
        with open(self.csv_file_path, newline='') as f:
            first_line = f.readline().strip()
            if any(col is None or col.strip() == "" for col in first_line.split(",")):
                raise ValueError("CSV contains empty or missing column headers.")
        with open(self.csv_file_path, newline='') as f:
            reader = csv.reader(f)
            header = next(reader)
            num_columns = len(header)
            for row in reader:
                if len(row) != num_columns:
                    raise ValueError(f"CSV row has an incorrect number of columns: {row}")
        df = pd.read_csv(self.csv_file_path)
        return df