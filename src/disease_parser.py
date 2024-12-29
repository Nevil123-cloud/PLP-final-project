import pandas as pd
import re
from datetime import datetime
from typing import Dict, List, Tuple
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

class DiseaseOutbreakParser:
    def __init__(self):
        # Define regions
        self.east_african_countries = {
            'Uganda': {'Kampala', 'Entebbe', 'Gulu', 'Mbarara'},
            'Kenya': {'Nairobi', 'Mombasa', 'Kisumu'},
            'Tanzania': {'Dar es Salaam', 'Arusha', 'Zanzibar'},
            'Rwanda': {'Kigali', 'Butare'},
            'Burundi': {'Bujumbura', 'Gitega'},
            'South Sudan': {'Juba', 'Malakal'},
            'Ethiopia': {'Addis Ababa', 'Dire Dawa'},
            'Somalia': {'Mogadishu', 'Hargeisa'}
        }
        
        # Define major diseases in Africa
        self.african_diseases = {
            'high_priority': {'Ebola', 'Malaria', 'Cholera', 'Tuberculosis', 'HIV'},
            'medium_priority': {'Measles', 'Meningitis', 'Rabies'},
            'low_priority': {'Influenza', 'Hepatitis'}
        }
        
        # Combine all diseases for easier lookup
        self.all_diseases = set.union(*self.african_diseases.values())
        
        # Initialize geocoder
        self.geocoder = Nominatim(user_agent="disease_outbreak_tracker")
        
        # Create flat set of all locations
        self.all_locations = {city for cities in 
                            [places for places in self.east_african_countries.values()] 
                            for city in cities}
        self.all_locations.update(self.east_african_countries.keys())
    
    def parse_headline(self, headline: str) -> Dict:
        """Parse a single headline for disease outbreak information."""
        data = {
            'headline': headline.strip(),
            'date': self._extract_date(headline),
            'disease': self._extract_disease(headline),
            'location': self._extract_location(headline),
            'severity': self._analyze_severity(headline),
            'region': self._classify_region(headline)
        }
        
        # Add coordinates if location is found
        if data['location']['country'] or data['location']['city']:
            coords = self._get_coordinates(data['location'])
            data['location'].update(coords)
            
        return data
    
    def _extract_disease(self, headline: str) -> str:
        """Extract disease name from headline."""
        headline_lower = headline.lower()
        for disease in self.all_diseases:
            if disease.lower() in headline_lower:
                return disease
        return 'Unknown'
    
    def _extract_location(self, headline: str) -> Dict[str, str]:
        """Extract location information from headline."""
        location = {
            'country': None,
            'city': None,
            'is_east_africa': False,
            'is_uganda': False
        }
        
        # Check for countries and cities
        for country, cities in self.east_african_countries.items():
            if country in headline:
                location['country'] = country
                location['is_east_africa'] = True
                if country == 'Uganda':
                    location['is_uganda'] = True
            
            for city in cities:
                if city in headline:
                    location['city'] = city
                    location['country'] = country
                    location['is_east_africa'] = True
                    if country == 'Uganda':
                        location['is_uganda'] = True
                    break
        
        return location
    
    def _analyze_severity(self, headline: str) -> str:
        """Analyze the severity of the outbreak based on keywords and context."""
        high_severity = ['outbreak', 'epidemic', 'death', 'fatal', 'emergency', 'claims lives', 'surge']
        medium_severity = ['spread', 'cases', 'infected', 'confirmed', 'rise', 'increase', 'alert']
        
        headline_lower = headline.lower()
        
        # Check disease priority
        disease = self._extract_disease(headline)
        if disease in self.african_diseases['high_priority']:
            severity_base = 2
        elif disease in self.african_diseases['medium_priority']:
            severity_base = 1
        else:
            severity_base = 0
            
        # Add severity based on keywords
        if any(word in headline_lower for word in high_severity):
            severity_base += 2
        elif any(word in headline_lower for word in medium_severity):
            severity_base += 1
            
        # Map final score to severity level
        if severity_base >= 3:
            return 'High'
        elif severity_base >= 1:
            return 'Medium'
        return 'Low'
    
    def _classify_region(self, headline: str) -> Dict[str, bool]:
        """Classify the region of the outbreak."""
        location = self._extract_location(headline)
        return {
            'is_africa': True if location['country'] else self._is_african_location(headline),
            'is_east_africa': location['is_east_africa'],
            'is_uganda': location['is_uganda']
        }
    
    def _is_african_location(self, headline: str) -> bool:
        """Check if the location is in Africa."""
        return any(location in headline for location in self.all_locations)
    
    def _extract_date(self, headline: str) -> str:
        """Extract date from headline."""
        # Look for date at the start of headline (YYYY-MM-DD format)
        date_match = re.match(r'(\d{4}-\d{2}-\d{2}):', headline)
        if date_match:
            return date_match.group(1)
        
        # If no date found, return None instead of current date
        return None
    
    def _get_coordinates(self, location: Dict) -> Dict[str, float]:
        """Get coordinates for a location using geocoding."""
        coords = {'latitude': None, 'longitude': None}
        
        try:
            # Try city first if available
            if location['city']:
                search_term = f"{location['city']}, {location['country']}"
            elif location['country']:
                search_term = location['country']
            else:
                return coords
                
            # Attempt geocoding
            location_data = self.geocoder.geocode(search_term)
            if location_data:
                coords['latitude'] = location_data.latitude
                coords['longitude'] = location_data.longitude
                
        except GeocoderTimedOut:
            pass  # Keep default None values if geocoding fails
            
        return coords

    def process_headlines(self, headlines: List[str]) -> pd.DataFrame:
        """Process multiple headlines and return a DataFrame."""
        parsed_data = [self.parse_headline(headline) for headline in headlines]
        df = pd.DataFrame(parsed_data)
        
        # Convert date strings to datetime objects where available
        df['date'] = pd.to_datetime(df['date'])
        
        return df
