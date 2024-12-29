import pandas as pd
import numpy as np
from typing import Dict, List, Optional
from datetime import datetime, timedelta

class AfricaOutbreakAnalyzer:
    def __init__(self, data: pd.DataFrame):
        self.data = data
        self.uganda_data = self._filter_uganda_data()
        self.east_africa_data = self._filter_east_africa_data()
        
        # Define priority levels for diseases
        self.disease_priority = {
            'Ebola': 'high',
            'Malaria': 'high',
            'Cholera': 'high',
            'Tuberculosis': 'high',
            'HIV': 'high',
            'Measles': 'medium',
            'Meningitis': 'medium',
            'Rabies': 'medium',
            'Influenza': 'low',
            'Hepatitis': 'low'
        }
    
    def _filter_uganda_data(self) -> pd.DataFrame:
        """Filter data for Uganda-specific outbreaks."""
        return self.data[self.data['location'].apply(lambda x: x['is_uganda'])]
    
    def _filter_east_africa_data(self) -> pd.DataFrame:
        """Filter data for East African outbreaks."""
        return self.data[self.data['location'].apply(lambda x: x['is_east_africa'])]
    
    def analyze_disease_distribution(self, region: str = 'uganda') -> Dict[str, Dict]:
        """Analyze disease distribution with detailed statistics."""
        if region == 'uganda':
            data = self.uganda_data
        elif region == 'east_africa':
            data = self.east_africa_data
        else:
            data = self.data
            
        disease_stats = {}
        for disease in data['disease'].unique():
            disease_data = data[data['disease'] == disease]
            disease_stats[disease] = {
                'count': len(disease_data),
                'severity_distribution': disease_data['severity'].value_counts().to_dict(),
                'priority': self.disease_priority.get(disease, 'unknown'),
                'latest_outbreak': disease_data['date'].max().strftime('%Y-%m-%d') if not disease_data.empty else None
            }
            
        return disease_stats
    
    def analyze_severity_trends(self, region: str = 'uganda', 
                              time_window: Optional[int] = None) -> Dict[str, Dict]:
        """Analyze severity trends with optional time window (in days)."""
        if region == 'uganda':
            data = self.uganda_data
        elif region == 'east_africa':
            data = self.east_africa_data
        else:
            data = self.data
            
        if time_window:
            cutoff_date = datetime.now() - timedelta(days=time_window)
            data = data[data['date'] >= cutoff_date]
            
        severity_stats = {}
        for severity in ['High', 'Medium', 'Low']:
            severity_data = data[data['severity'] == severity]
            severity_stats[severity] = {
                'count': len(severity_data),
                'disease_distribution': severity_data['disease'].value_counts().to_dict(),
                'percentage': (len(severity_data) / len(data) * 100) if len(data) > 0 else 0
            }
            
        return severity_stats
    
    def get_high_priority_outbreaks(self, region: str = 'uganda', 
                                  min_severity: str = 'High') -> pd.DataFrame:
        """Get high priority outbreaks with minimum severity level."""
        if region == 'uganda':
            data = self.uganda_data
        elif region == 'east_africa':
            data = self.east_africa_data
        else:
            data = self.data
            
        severity_levels = {
            'High': 3,
            'Medium': 2,
            'Low': 1
        }
        
        min_severity_level = severity_levels[min_severity]
        
        # Filter based on severity and high-priority diseases
        high_priority = data[
            (data['severity'].map(lambda x: severity_levels[x]) >= min_severity_level) &
            (data['disease'].map(lambda x: self.disease_priority.get(x)) == 'high')
        ]
        
        return high_priority.sort_values('date', ascending=False)
    
    def analyze_temporal_patterns(self, 
                                region: str = 'uganda',
                                disease: Optional[str] = None,
                                time_window: Optional[int] = None) -> pd.DataFrame:
        """Analyze temporal patterns with optional disease filter and time window."""
        if region == 'uganda':
            data = self.uganda_data
        elif region == 'east_africa':
            data = self.east_africa_data
        else:
            data = self.data
            
        if disease:
            data = data[data['disease'] == disease]
            
        if time_window:
            cutoff_date = datetime.now() - timedelta(days=time_window)
            data = data[data['date'] >= cutoff_date]
            
        # Group by date and get counts
        temporal_data = data.groupby(['date', 'disease']).size().unstack(fill_value=0)
        
        # Add cumulative counts
        temporal_data['cumulative_total'] = temporal_data.sum(axis=1).cumsum()
        
        return temporal_data
    
    def get_summary_statistics(self, region: str = 'uganda') -> Dict:
        """Get comprehensive summary statistics for specified region."""
        if region == 'uganda':
            data = self.uganda_data
        elif region == 'east_africa':
            data = self.east_africa_data
        else:
            data = self.data
            
        if data.empty:
            return {
                'total_outbreaks': 0,
                'message': f'No outbreak data available for {region}'
            }
            
        # Basic statistics
        stats = {
            'total_outbreaks': len(data),
            'unique_diseases': data['disease'].nunique(),
            'severity_distribution': data['severity'].value_counts().to_dict(),
            'most_common_disease': data['disease'].mode().iloc[0],
            'high_severity_count': len(data[data['severity'] == 'High']),
            'date_range': {
                'first_outbreak': data['date'].min().strftime('%Y-%m-%d'),
                'latest_outbreak': data['date'].max().strftime('%Y-%m-%d')
            }
        }
        
        # Disease priority distribution
        priority_counts = data['disease'].map(self.disease_priority).value_counts()
        stats['priority_distribution'] = priority_counts.to_dict()
        
        # Location statistics
        stats['location_stats'] = {
            'countries_affected': len(set(row['location']['country'] 
                                       for _, row in data.iterrows() 
                                       if row['location']['country'])),
            'cities_affected': len(set(row['location']['city'] 
                                     for _, row in data.iterrows() 
                                     if row['location']['city']))
        }
        
        # Recent trends (last 30 days)
        cutoff_date = data['date'].max() - timedelta(days=30)
        recent_data = data[data['date'] >= cutoff_date]
        stats['recent_trends'] = {
            'total_outbreaks': len(recent_data),
            'severity_distribution': recent_data['severity'].value_counts().to_dict() if not recent_data.empty else {}
        }
        
        return stats
