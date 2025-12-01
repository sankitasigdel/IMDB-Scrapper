import os
import time
from abc import ABC, abstractmethod

class IBrowserHandler(ABC):
    """Interface for browser operations"""
    
    @abstractmethod
    def close_browser(self):
        """Close the browser"""
        pass
    
    @abstractmethod
    def open_and_navigate(self, url: str):
        """Open browser and navigate to URL"""
        pass

class SafariHandler(IBrowserHandler):
    """Handles Safari browser operations"""
    
    def __init__(self, wait_time: int = 2):
        self.wait_time = wait_time
    
    def close_browser(self):
        """Close Safari application"""
        applescript = 'tell app "Safari" to quit'
        os.system(f"osascript -e '{applescript}'")
        print("Safari closed")
        time.sleep(self.wait_time)
    
    def open_and_navigate(self, url: str):
        """Open Safari and navigate to URL"""
        applescript = f'''
        tell application "Safari"
            activate
            delay 1
            open location "{url}"
        end tell
        '''
        os.system(f"osascript -e '{applescript}'")
        print(f"Navigating to: {url}")
        time.sleep(1)
