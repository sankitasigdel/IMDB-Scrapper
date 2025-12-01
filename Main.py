from SafariHandler import SafariHandler
from scraper import IMDbScraper
from ExcelHandler import ExcelHandler
from EmailHandler import OutlookEmailHandler

class IMDbSearchApp:
    """Main application class that orchestrates all components"""
    
    def __init__(self):
        self.browser = SafariHandler(wait_time=2)
        self.scraper = IMDbScraper(max_results=10)
        self.excel_handler = ExcelHandler()  # Saves to Desktop by default
        self.email_handler = OutlookEmailHandler()
    
    def run(self):
        """Main workflow: scrape, save, and email"""
        print("\n" + "="*60)
        print("IMDb MOVIE SCRAPER WITH EMAIL")
        print("="*60 + "\n")
        
        # Get user inputs
        movie_name = input("Enter movie name to search: ").strip()
        recipient_email = input("Enter recipient email: ").strip()
        
        if not movie_name or not recipient_email:
            print("Movie name and email are required!")
            return
        
        print(f"\n{'='*60}")
        print(f"Processing search for: {movie_name}")
        print(f"{'='*60}\n")
        
        # Step 1: Close Safari
        self.browser.close_browser()
        
        # Step 2: Open Safari with IMDb search
        search_url = self.scraper.build_search_url(movie_name)
        self.browser.open_and_navigate(search_url)
        
        # Step 3: Scrape search results
        print("Scraping IMDb search results...")
        movies_data = self.scraper.scrape_search_results(movie_name)
        
        if not movies_data:
            print("No movie data found. Exiting...")
            return
        
        # Step 4: Save to Excel
        file_path = self.excel_handler.save_to_excel(movies_data, movie_name)
        
        if not file_path:
            print("Failed to save Excel file. Exiting...")
            return
        
        # Step 5: Send email with Excel attachment
        print("\nSending email...")
        subject = f"IMDb Search Results: {movie_name}"
        body = f"""Hello,

Please find attached the IMDb search results for "{movie_name}".

Found {len(movies_data)} movies.

Best regards"""
        
        email_sent = self.email_handler.send_email(
            to_email=recipient_email,
            subject=subject,
            body=body,
            attachment_path=file_path
        )
        
        if email_sent:
            print(f"\n{'='*60}")
            print(f"✓ SUCCESS!")
            print(f"✓ Scraped {len(movies_data)} movies")
            print(f"✓ Saved to: {file_path}")
            print(f"✓ Email sent to: {recipient_email}")
            print(f"{'='*60}\n")
        else:
            print("\n⚠ Email failed to send, but Excel file was saved locally.\n")

if __name__ == "__main__":
    app = IMDbSearchApp()
    app.run()