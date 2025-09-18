"""Page discovery utilities"""
import os
import glob
from config.app_config import PAGE_CONFIG

class PageDiscovery:
    def __init__(self, pages_dir="pages"):
        self.pages_dir = pages_dir
    
    def get_available_pages(self):
        if not os.path.exists(self.pages_dir):
            return []
        page_files = glob.glob(f"{self.pages_dir}/*.py")
        return sorted(page_files)
    
    def get_page_info(self, filename):
        filename_lower = os.path.basename(filename).lower()
        for key, config in PAGE_CONFIG.items():
            if key in filename_lower:
                return config['icon'], config['title'], config['description']
        clean_name = filename.replace('.py', '').replace('_', ' ').title()
        return "🤖", clean_name, "AI assistant page"
    
    def validate_pages_directory(self):
        return os.path.exists(self.pages_dir)