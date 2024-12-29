import pandas as pd
import re
from datetime import datetime
from typing import Dict, List, Tuple

class DiseaseOutbreakParser:
    def __init__(self):
        # Define regions
        self.east_african_countries = {
            'Uganda', 'Kenya', 'Tanzania', 'Rwanda', 'Burundi', 
            'South Sudan', 'Ethiopia', 'Somalia', 'Zanzibar', 'Arusha',
            'Nairobi', 'Dar es Salaam', 'Kampala', 'Entebbe'
        }
        
        # Define major diseases in Africa
        self.african_diseases = {
            'high_priority': {'Ebola', 'Malaria', 'Cholera', 'Tuberculosis', 'HIV'},
            'medium_priority': {'Measles', 'Meningitis', 'Rabies'},
            'low_priority': {'Influenza', 'Hepatitis'}
        }
        
        # Combine all diseases for easier lookup
        self.all_diseases = set.union(*self.african_diseases.values())
        
    def parse_headline(self, headline: str) -> Dict:
        """Parse a single headline for disease outbreak information."""
        data = {
            'headline': headline,
            'date': self._extract_date(headline),
            'disease': self._extract_disease(headline),
            'location': self._extract_location(headline),
            'severity': self._analyze_severity(headline),
            'region': self._classify_region(headline)
        }
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
        
        # Check for locations
        for place in self.east_african_countries:
            if place in headline:
                location['is_east_africa'] = True
                if place in ['Uganda', 'Kampala', 'Entebbe']:
                    location['is_uganda'] = True
                    location['country'] = 'Uganda'
                    if place != 'Uganda':
                        location['city'] = place
                break
            
        return location
    
    def _analyze_severity(self, headline: str) -> str:
        """Analyze the severity of the outbreak based on keywords."""
        high_severity = ['outbreak', 'epidemic', 'death', 'fatal', 'emergency', 'claims lives']
        medium_severity = ['spread', 'cases', 'infected', 'confirmed', 'rise', 'increase']
        
        headline_lower = headline.lower()
        
        if any(word in headline_lower for word in high_severity):
            return 'High'
        elif any(word in headline_lower for word in medium_severity):
            return 'Medium'
        return 'Low'
    
    def _classify_region(self, headline: str) -> Dict[str, bool]:
        """Classify the region of the outbreak."""
        return {
            'is_africa': self._is_african_location(headline),
            'is_east_africa': self._is_east_african_location(headline),
            'is_uganda': 'Uganda' in headline or 'Kampala' in headline or 'Entebbe' in headline
        }
    
    def _is_african_location(self, headline: str) -> bool:
        """Check if the location is in Africa."""
        african_keywords = {'Africa', 'Uganda', 'Kenya', 'Tanzania', 
                          'Ethiopia', 'Nigeria', 'Cairo', 'Kampala',
                          'Johannesburg', 'Dakar', 'Zanzibar', 'Arusha',
                          'Nairobi', 'Dar es Salaam', 'Entebbe'}
        return any(location in headline for location in african_keywords)
    
    def _is_east_african_location(self, headline: str) -> bool:
        """Check if the location is in East Africa."""
        return any(country in headline for country in self.east_african_countries)
    
    def _extract_date(self, headline: str) -> str:
        """Extract date from headline if available."""
        # This would be enhanced with actual date extraction logic
        return datetime.now().strftime('%Y-%m-%d')

    def process_headlines(self, headlines: List[str]) -> pd.DataFrame:
        """Process multiple headlines and return a DataFrame."""
        parsed_data = [self.parse_headline(headline) for headline in headlines]
        return pd.DataFrame(parsed_data)
