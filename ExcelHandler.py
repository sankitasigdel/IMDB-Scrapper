import os
from abc import ABC, abstractmethod
from typing import List, Dict
from datetime import datetime
import pandas as pd

class IExcelHandler(ABC):
    """Interface for Excel operations"""
    
    @abstractmethod
    def save_to_excel(self, data: List[Dict], filename: str) -> str:
        """Save data to Excel file"""
        pass

class ExcelHandler(IExcelHandler):
    """Handles Excel file operations"""
    
    def __init__(self, save_directory: str = None):
        if save_directory:
            self.save_directory = save_directory
        else:
            self.save_directory = os.path.expanduser("~/Desktop/")
        
        # Create directory if it doesn't exist
        os.makedirs(self.save_directory, exist_ok=True)
    
    def save_to_excel(self, data: List[Dict], base_filename: str) -> str:
        """Save data to Excel file with timestamp"""
        if not data:
            print("No data to save")
            return None
        
        df = pd.DataFrame(data)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        sanitized_name = base_filename.replace(' ', '_').replace('/', '_')
        filename = f"imdb_search_{sanitized_name}_{timestamp}.xlsx"
        
        full_path = os.path.join(self.save_directory, filename)
        
        try:
            df.to_excel(full_path, index=False, sheet_name='IMDb Results')
            print(f"✓ Data saved to: {full_path}")
            return full_path
        except Exception as e:
            print(f"Error saving Excel file: {e}")
            return None