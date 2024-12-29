import matplotlib.pyplot as plt
import seaborn as sns
from mpl_toolkits.basemap import Basemap
import pandas as pd
from typing import Optional, Tuple, List
import numpy as np

class OutbreakVisualizer:
    def __init__(self, data: pd.DataFrame):
        self.data = data
        plt.style.use('seaborn-v0_8')  # Using a specific seaborn style that's compatible
        
    def plot_disease_distribution(self, 
                                region: str = 'uganda',
                                title: Optional[str] = None,
                                figsize: Tuple[int, int] = (10, 6)) -> None:
        """Plot disease distribution for specified region."""
        if region == 'uganda':
            data = self.data[self.data['location'].apply(lambda x: x['is_uganda'])]
        elif region == 'east_africa':
            data = self.data[self.data['location'].apply(lambda x: x['is_east_africa'])]
        else:
            data = self.data
            
        plt.figure(figsize=figsize)
        disease_counts = data['disease'].value_counts()
        
        sns.barplot(x=disease_counts.values, y=disease_counts.index)
        plt.title(title or f'Disease Distribution in {region.title()}')
        plt.xlabel('Number of Outbreaks')
        plt.ylabel('Disease')
        plt.tight_layout()
        
    def plot_severity_distribution(self,
                                 region: str = 'uganda',
                                 title: Optional[str] = None,
                                 figsize: Tuple[int, int] = (8, 6)) -> None:
        """Plot severity distribution for specified region."""
        if region == 'uganda':
            data = self.data[self.data['location'].apply(lambda x: x['is_uganda'])]
        elif region == 'east_africa':
            data = self.data[self.data['location'].apply(lambda x: x['is_east_africa'])]
        else:
            data = self.data
            
        plt.figure(figsize=figsize)
        severity_counts = data['severity'].value_counts()
        
        colors = {'High': 'red', 'Medium': 'yellow', 'Low': 'green'}
        plt.pie(severity_counts.values, 
                labels=severity_counts.index,
                colors=[colors[sev] for sev in severity_counts.index],
                autopct='%1.1f%%')
        plt.title(title or f'Outbreak Severity Distribution in {region.title()}')
        plt.axis('equal')
        
    def plot_temporal_trends(self,
                           region: str = 'uganda',
                           disease: Optional[str] = None,
                           title: Optional[str] = None,
                           figsize: Tuple[int, int] = (12, 6)) -> None:
        """Plot temporal trends of outbreaks."""
        if region == 'uganda':
            data = self.data[self.data['location'].apply(lambda x: x['is_uganda'])]
        elif region == 'east_africa':
            data = self.data[self.data['location'].apply(lambda x: x['is_east_africa'])]
        else:
            data = self.data
            
        if disease:
            data = data[data['disease'] == disease]
            
        plt.figure(figsize=figsize)
        temporal_data = data.groupby('date').size()
        
        plt.plot(temporal_data.index, temporal_data.values, marker='o')
        plt.title(title or f'Temporal Trends of Outbreaks in {region.title()}')
        plt.xlabel('Date')
        plt.ylabel('Number of Outbreaks')
        plt.xticks(rotation=45)
        plt.tight_layout()
        
    def plot_east_africa_map(self,
                            title: Optional[str] = None,
                            figsize: Tuple[int, int] = (15, 10)) -> None:
        """Plot outbreak locations on East Africa map."""
        plt.figure(figsize=figsize)
        
        # Create map focused on East Africa
        m = Basemap(llcrnrlon=28., llcrnrlat=-12., urcrnrlon=52., urcrnrlat=5.,
                   resolution='l', projection='merc')
        
        m.drawcoastlines()
        m.drawcountries()
        m.fillcontinents(color='lightgray', lake_color='lightblue')
        m.drawmapboundary(fill_color='lightblue')
        
        # Filter East African data
        east_africa_data = self.data[self.data['location'].apply(lambda x: x['is_east_africa'])]
        
        # Plot outbreak locations
        for _, row in east_africa_data.iterrows():
            if row['location']['city'] and row['location']['country']:
                # This would need actual lat/lon coordinates
                # For now, using placeholder logic
                x, y = m(35, 0)  # Example coordinates
                m.plot(x, y, 'ro', markersize=8)
        
        plt.title(title or 'Disease Outbreaks in East Africa')
        plt.tight_layout()
        
    def plot_disease_severity_heatmap(self,
                                    region: str = 'uganda',
                                    title: Optional[str] = None,
                                    figsize: Tuple[int, int] = (10, 8)) -> None:
        """Plot disease severity heatmap."""
        if region == 'uganda':
            data = self.data[self.data['location'].apply(lambda x: x['is_uganda'])]
        elif region == 'east_africa':
            data = self.data[self.data['location'].apply(lambda x: x['is_east_africa'])]
        else:
            data = self.data
            
        # Create severity-disease matrix
        severity_map = {'Low': 0, 'Medium': 1, 'High': 2}
        pivot_data = pd.crosstab(data['disease'], data['severity'])
        
        plt.figure(figsize=figsize)
        sns.heatmap(pivot_data, cmap='YlOrRd', annot=True, fmt='d')
        plt.title(title or f'Disease Severity Heatmap - {region.title()}')
        plt.tight_layout()
