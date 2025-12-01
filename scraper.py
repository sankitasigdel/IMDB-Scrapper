from abc import ABC, abstractmethod
from typing import List, Dict
from urllib.parse import quote
import requests
from bs4 import BeautifulSoup

class IScraper(ABC):
    """Interface for web scraping operations"""
    
    @abstractmethod
    def scrape_search_results(self, query: str) -> List[Dict]:
        """Scrape search results for given query"""
        pass

class IMDbScraper(IScraper):
    """Scrapes movie data from IMDb"""
    
    def __init__(self, max_results: int = 10):
        self.max_results = max_results
        self.base_url = "https://www.imdb.com"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
    
    def build_search_url(self, query: str) -> str:
        """Build IMDb search URL"""
        encoded_query = quote(query)
        return f"{self.base_url}/find/?q={encoded_query}&s=tt&ttype=ft"
    
    def scrape_search_results(self, query: str) -> List[Dict]:
        """Scrape movie information from IMDb search results"""
        search_url = self.build_search_url(query)
        print(f"Scraping: {search_url}")
        
        try:
            response = requests.get(search_url, headers=self.headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            return self._parse_results(soup)
        
        except requests.RequestException as e:
            print(f"Error fetching data: {e}")
            return []
        except Exception as e:
            print(f"Error scraping IMDb: {e}")
            return []
    
    def _parse_results(self, soup: BeautifulSoup) -> List[Dict]:
        """Parse movie results from HTML"""
        movies = []

        # Find the UL list container
        ul = soup.find('ul', class_='ipc-metadata-list')
        if not ul:
            print("No list found")
            return movies

        # Each LI is one movie result
        items = ul.find_all('li', class_='ipc-metadata-list-summary-item')

        for li in items[:self.max_results]:
            try:
                movie = self._extract_movie_info(li)
                if movie:
                    movies.append(movie)
            except Exception as e:
                print(f"Error parsing result: {e}")
                continue

        print(f"Found {len(movies)} movies")
        return movies

    def _extract_movie_info(self, li) -> Dict:
        """Extract title, link, year, rating, etc from the nested IMDb HTML"""

        # ---------- TITLE ----------
        title_tag = li.find('h3', class_='ipc-title__text')
        if not title_tag:
            return None
        title = title_tag.get_text(strip=True)

        # ---------- LINK ----------
        link_tag = li.find('a', href=True)
        if link_tag:
            link = self.base_url + link_tag['href'].split('?')[0]
        else:
            link = None

        # ---------- YEAR / METADATA ----------
        metadata_tags = li.find_all('span', class_='cli-title-metadata-item')

        year = None
        duration = None
        rating = None

        if len(metadata_tags) >= 1:
            year = metadata_tags[0].get_text(strip=True)
        if len(metadata_tags) >= 2:
            duration = metadata_tags[1].get_text(strip=True)
        if len(metadata_tags) >= 3:
            rating = metadata_tags[2].get_text(strip=True)

        # ---------- POSTER IMAGE ----------
        img_tag = li.find('img', class_='ipc-image')
        img_url = img_tag['src'] if img_tag else None

        # ---------- IMDb RATING ----------
        rating_tag = li.find('span', attrs={'data-testid': 'ratingGroup--imdb-rating'})
        imdb_rating = None
        if rating_tag:
            imdb_rating = rating_tag.find('span', class_='ipc-rating-star--rating')
            imdb_rating = imdb_rating.get_text(strip=True) if imdb_rating else None

        return {
            'Title': title,
            'Year': year,
            'Duration': duration,
            'Content_Rating': rating,
            'IMDb_Rating': imdb_rating,
            'Poster_URL': img_url,
            'IMDb_Link': link
        }