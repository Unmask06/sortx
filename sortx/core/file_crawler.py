"""
file_crawler.py
"""

import logging
from datetime import datetime
from pathlib import Path
from typing import Optional

import pandas as pd
import xlwings as xw

# Setup logging with a more informative format
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class FileCrawler:
    df: pd.DataFrame

    def __init__(
        self,
        excel_file_path: str,
        folder_directory: str,
        doc_no_column_name: Optional[str],
        header: int = 1,
        sheet_name: str | int = 1,
    ):
        self.excel_file_path = excel_file_path
        self.folder_directory = folder_directory
        self.doc_no_column_name = doc_no_column_name
        self.header = header - 1
        self.sheet_name = sheet_name - 1

    def read_excel(self):
        try:
            self.df = pd.read_excel(
                self.excel_file_path, sheet_name=self.sheet_name, header=self.header
            )
            logger.info("Excel file read successfully.")
        except Exception as e:
            logger.error(f"Error reading excel file: {e}")
            raise

    def update_folder_link(self):
        if self.df is None:
            logger.error("DataFrame is empty or not initialized.")
            raise ValueError("DataFrame is empty or not initialized.")

        for file_path in Path(self.folder_directory).rglob("*"):
            if (
                file_path.is_dir()
                and file_path.name in self.df[self.doc_no_column_name].values
            ):
                self.df.loc[
                    self.df[self.doc_no_column_name] == file_path.name,
                    ["status", "filepath", "processed_date"],
                ] = [
                    "Yes",
                    str(file_path),
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                ]
        logger.info("Folder link updated successfully.")

    def save_excel(self):
        try:
            with xw.App(visible=False) as app:
                wb = app.books.open(self.excel_file_path)
                sheet = wb.sheets[self.sheet_name]
                starting_cell = sheet.range(f"A{self.header}")
                sheet.range(starting_cell).expand("table").clear_contents()
                sheet.range(starting_cell).options(index=False).value = self.df
                wb.save()
                wb.close()
        except Exception as e:
            logger.error(f"Error saving excel file: {e}")
            raise ValueError("Error saving excel file.")