import requests
import json
from datetime import datetime
from typing import Dict, List, Any
import os 
from dotenv import load_dotenv

load_dotenv()

class MadridEventsFetcher:

    def __init__(self):
        self.newsdata_api_key = os.getenv("NEWSDATA_API_KEY")
        self.sources = {
            'newsdata': 'https://newsdata.io/api/1/latest',
            'cultural_events': 'https://datos.madrid.es/egob/catalogo/206974-0-agenda-eventos-culturales-100.json',
            'general_events': 'https://datos.madrid.es/egob/catalogo/300107-0-agenda-actividades-eventos.json'
        }
        
    def fetch_newsdata(self, limit: int = 10) -> Dict[str, Any]:
        """
        Fetch news articles from NewsData.io API
        
        You  get 200 API credits per day for making requests. Each request will fetch 10 articles per credit.
        
        Returns:
            Dict containing API response with articles
        """
        params = {
            'apikey': self.newsdata_api_key,
            'country': 'es',
            'language': 'en,es,fr',
            'size': limit
        }
        
        try:
            print(f"\n{'='*60}")
            print("Fetching NewsData.io articles...")
            print(f"{'='*60}")
            
            response = requests.get(self.sources['newsdata'], params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            print(f"Status: {data.get('status')}")
            print(f"Total Results: {data.get('totalResults', 0)}")
            print(f"Articles fetched: {len(data.get('results', []))}")
            
            # Print sample article
            if data.get('results'):
                article = data['results'][0]
                print(f"\nSample Article:")
                print(f"  Title: {article.get('title', 'N/A')[:80]}...")
                print(f"  Source: {article.get('source_id', 'N/A')}")
                print(f"  Published: {article.get('pubDate', 'N/A')}")
                print(f"  Language: {article.get('language', 'N/A')}")
            
            return data
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching NewsData: {e}")
            return {'status': 'error', 'error': str(e)}

    def fetch_cultural_events(self, limit: int = 10) -> Dict[str, Any]:
        """
        Fetch cultural events from Madrid Open Data
        
        Returns:
            Dict containing events data
        """
        try:
            print(f"\n{'='*60}")
            print("Fetching Madrid Cultural Events...")
            print(f"{'='*60}")
            
            response = requests.get(self.sources['cultural_events'], timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Extract events from @graph
            events = data.get('@graph', [])
            
            print(f"Total events fetched: {len(events)}")
            
            # Print sample event
            if events:
                event = events[0]
                print(f"\nSample Cultural Event:")
                print(f"  Title: {event.get('title', 'N/A')}")
                print(f"  Type: {event.get('@type', 'N/A')}")
                print(f"  Location: {event.get('location', {}).get('locality', 'N/A')}")
                
                # Handle date formats
                dtstart = event.get('dtstart')
                if dtstart:
                    print(f"  Start Date: {dtstart}")
            
            return {
                'total_events': len(events),
                'events': events[:limit],
                'full_data': data
            }
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching Cultural Events: {e}")
            return {'status': 'error', 'error': str(e)}

    def fetch_general_events(self, limit: int = 10) -> Dict[str, Any]:
        """
        Fetch general activities and events from Madrid Open Data
        
        Args:
            limit: Number of events to return in summary
        
        Returns:
            Dict containing events data
        """
        try:
            print(f"\n{'='*60}")
            print("Fetching Madrid General Events & Activities...")
            print(f"{'='*60}")
            
            response = requests.get(self.sources['general_events'], timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Extract events from @graph
            events = data.get('@graph', [])
            
            print(f"Total events fetched: {len(events)}")
            
            # Print sample event
            if events:
                event = events[0]
                print(f"\nSample General Event:")
                print(f"  Title: {event.get('title', 'N/A')}")
                print(f"  Type: {event.get('@type', 'N/A')}")
                
                # Try different location fields
                location = event.get('event-location') or event.get('location', {})
                if isinstance(location, dict):
                    print(f"  Location: {location.get('locality', 'N/A')}")
                else:
                    print(f"  Location: {location}")
                
                dtstart = event.get('dtstart')
                if dtstart:
                    print(f"  Start Date: {dtstart}")
            
            return {
                'total_events': len(events),
                'events': events[:limit],
                'full_data': data
            }
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching General Events: {e}")
            return {'status': 'error', 'error': str(e)}

    def fetch_all(self, save_to_file: bool = True) -> Dict[str, Any]:
        """
        Fetch data from all sources
        
        Args:
            save_to_file: Whether to save results to JSON files
        
        Returns:
            Dict containing all fetched data
        """
        print(f"\n{'#'*60}")
        print("# Madrid Events Multi-Source Data Fetch")
        print(f"# {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'#'*60}")
        
        results = {
            'timestamp': datetime.now().isoformat(),
            'newsdata': self.fetch_newsdata(),
            'cultural_events': self.fetch_cultural_events(),
            'general_events': self.fetch_general_events()
        }
        
        if save_to_file:
            # Save individual source files
            for source_name, source_data in results.items():
                if source_name != 'timestamp':
                    filename = f'sample_data_{source_name}.json'
                    with open(filename, 'w', encoding='utf-8') as f:
                        json.dump(source_data, f, ensure_ascii=False, indent=2)
                    print(f"\n✓ Saved {source_name} to {filename}")
            
            # Save combined file
            combined_filename = 'sample_data_all_sources.json'
            with open(combined_filename, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            print(f"✓ Saved all sources to {combined_filename}")
        
        print(f"\n{'='*60}")
        print("Fetch complete!")
        print(f"{'='*60}\n")
        
        return results

def main():
    fetcher = MadridEventsFetcher()
    results = fetcher.fetch_all(save_to_file=True)

if __name__ == "__main__":
    main()

    