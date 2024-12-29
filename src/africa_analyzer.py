import pandas as pd
import numpy as np
from typing import Dict, List, Optional
from datetime import datetime

class AfricaOutbreakAnalyzer:
    def __init__(self, data: pd.DataFrame):
        self.data = data
        self.uganda_data = self._filter_uganda_data()
        self.east_africa_data = self._filter_east_africa_data()
    
    def _filter_uganda_data(self) -> pd.DataFrame:
        """Filter data for Uganda-specific outbreaks."""
        return self.data[self.data['location'].apply(lambda x: x['is_uganda'])]
    
    def _filter_east_africa_data(self) -> pd.DataFrame:
        """Filter data for East African outbreaks."""
        return self.data[self.data['location'].apply(lambda x: x['is_east_africa'])]
    
    def analyze_disease_distribution(self, region: str = 'uganda') -> Dict[str, int]:
        """Analyze disease distribution in specified region."""
        if region == 'uganda':
            data = self.uganda_data
        elif region == 'east_africa':
            data = self.east_africa_data
        else:
            data = self.data
            
        return data['disease'].value_counts().to_dict()
    
    def analyze_severity_trends(self, region: str = 'uganda') -> Dict[str, int]:
        """Analyze severity trends in specified region."""
        if region == 'uganda':
            data = self.uganda_data
        elif region == 'east_africa':
            data = self.east_africa_data
        else:
            data = self.data
            
        return data['severity'].value_counts().to_dict()
    
    def get_high_priority_outbreaks(self, region: str = 'uganda') -> pd.DataFrame:
        """Get high severity outbreaks in specified region."""
        if region == 'uganda':
            data = self.uganda_data
        elif region == 'east_africa':
            data = self.east_africa_data
        else:
            data = self.data
            
        return data[data['severity'] == 'High']
    
    def analyze_temporal_patterns(self, 
                                region: str = 'uganda',
                                disease: Optional[str] = None) -> pd.DataFrame:
        """Analyze temporal patterns of outbreaks."""
        if region == 'uganda':
            data = self.uganda_data
        elif region == 'east_africa':
            data = self.east_africa_data
        else:
            data = self.data
            
        if disease:
            data = data[data['disease'] == disease]
            
        return data.groupby('date').size().reset_index(name='count')
    
    def get_summary_statistics(self, region: str = 'uganda') -> Dict:
        """Get summary statistics for specified region."""
        if region == 'uganda':
            data = self.uganda_data
        elif region == 'east_africa':
            data = self.east_africa_data
        else:
            data = self.data
            
        return {
            'total_outbreaks': len(data),
            'unique_diseases': data['disease'].nunique(),
            'severity_distribution': data['severity'].value_counts().to_dict(),
            'most_common_disease': data['disease'].mode().iloc[0] if not data.empty else None,
            'high_severity_count': len(data[data['severity'] == 'High'])
        }
