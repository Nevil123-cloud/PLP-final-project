import matplotlib.pyplot as plt
import seaborn as sns
from mpl_toolkits.basemap import Basemap
import pandas as pd
from typing import Optional, Tuple, List
import numpy as np
from datetime import datetime, timedelta

class OutbreakVisualizer:
    def __init__(self, data: pd.DataFrame):
        self.data = data
        # Set default style instead of seaborn
        plt.style.use('default')
        sns.set_theme()  # This will apply seaborn styling
        
        # Define color schemes
        self.severity_colors = {
            'High': '#ff4444',    # Red
            'Medium': '#ffbb33',  # Orange
            'Low': '#00C851'      # Green
        }
        
        self.disease_colors = {
            'Ebola': '#FF4444',      # Red
            'Malaria': '#ffbb33',    # Orange
            'Cholera': '#33b5e5',    # Blue
            'Tuberculosis': '#aa66cc',# Purple
            'HIV': '#FF8800',        # Dark Orange
            'Measles': '#00C851',    # Green
            'Meningitis': '#2BBBAD', # Teal
            'Rabies': '#4285F4',     # Light Blue
            'Influenza': '#1C2331',  # Dark Blue
            'Hepatitis': '#CC0000'   # Dark Red
        }
        
    def plot_disease_distribution(self, 
                                region: str = 'uganda',
                                title: Optional[str] = None,
                                figsize: Tuple[int, int] = (12, 8)) -> None:
        """Plot disease distribution for specified region."""
        if region == 'uganda':
            data = self.data[self.data['location'].apply(lambda x: x['is_uganda'])]
        elif region == 'east_africa':
            data = self.data[self.data['location'].apply(lambda x: x['is_east_africa'])]
        else:
            data = self.data
            
        plt.figure(figsize=figsize)
        disease_counts = data['disease'].value_counts()
        
        # Create color map for diseases present in the data
        colors = [self.disease_colors.get(disease, '#808080') for disease in disease_counts.index]
        
        ax = sns.barplot(x=disease_counts.values, y=disease_counts.index, palette=colors)
        
        # Add value labels on the bars
        for i, v in enumerate(disease_counts.values):
            ax.text(v, i, f' {v}', va='center')
        
        plt.title(title or f'Disease Distribution in {region.title()}')
        plt.xlabel('Number of Outbreaks')
        plt.ylabel('Disease')
        plt.tight_layout()
        plt.savefig(f'disease_distribution_{region}.png')
        plt.close()
        
    def plot_severity_distribution(self,
                                 region: str = 'uganda',
                                 title: Optional[str] = None,
                                 figsize: Tuple[int, int] = (10, 8)) -> None:
        """Plot severity distribution for specified region."""
        if region == 'uganda':
            data = self.data[self.data['location'].apply(lambda x: x['is_uganda'])]
        elif region == 'east_africa':
            data = self.data[self.data['location'].apply(lambda x: x['is_east_africa'])]
        else:
            data = self.data
            
        plt.figure(figsize=figsize)
        severity_counts = data['severity'].value_counts()
        
        colors = [self.severity_colors[sev] for sev in severity_counts.index]
        wedges, texts, autotexts = plt.pie(severity_counts.values, 
                                         labels=severity_counts.index,
                                         colors=colors,
                                         autopct='%1.1f%%',
                                         explode=[0.05] * len(severity_counts))
        
        # Enhance the appearance of labels and percentages
        plt.setp(autotexts, size=10, weight="bold")
        plt.setp(texts, size=12)
        
        plt.title(title or f'Outbreak Severity Distribution in {region.title()}')
        plt.axis('equal')
        plt.savefig(f'severity_distribution_{region}.png')
        plt.close()
        
    def plot_temporal_trends(self,
                           region: str = 'uganda',
                           disease: Optional[str] = None,
                           title: Optional[str] = None,
                           figsize: Tuple[int, int] = (14, 8)) -> None:
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
        
        # Group by date and disease
        temporal_data = data.groupby(['date', 'disease']).size().unstack(fill_value=0)
        
        # Plot stacked area chart
        ax = temporal_data.plot(kind='area', stacked=True, 
                              color=[self.disease_colors.get(d, '#808080') for d in temporal_data.columns])
        
        plt.title(title or f'Temporal Trends of Outbreaks in {region.title()}')
        plt.xlabel('Date')
        plt.ylabel('Number of Outbreaks')
        plt.xticks(rotation=45)
        plt.grid(True, alpha=0.3)
        plt.legend(title='Diseases', bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()
        plt.savefig(f'temporal_trends_{region}.png')
        plt.close()
        
    def plot_east_africa_map(self,
                            title: Optional[str] = None,
                            figsize: Tuple[int, int] = (15, 10)) -> None:
        """Plot outbreak locations on East Africa map."""
        plt.figure(figsize=figsize)
        
        # Create map focused on East Africa
        m = Basemap(llcrnrlon=28., llcrnrlat=-12., urcrnrlon=52., urcrnrlat=5.,
                   resolution='l', projection='merc')
        
        m.drawcoastlines(linewidth=0.5)
        m.drawcountries(linewidth=0.5)
        m.fillcontinents(color='lightgray', lake_color='lightblue')
        m.drawmapboundary(fill_color='lightblue')
        
        # Filter East African data
        east_africa_data = self.data[self.data['location'].apply(lambda x: x['is_east_africa'])]
        
        # Create legend handles
        legend_elements = []
        diseases_plotted = set()
        
        # Plot outbreak locations
        for _, row in east_africa_data.iterrows():
            location = row['location']
            if location.get('latitude') and location.get('longitude'):
                x, y = m(location['longitude'], location['latitude'])
                disease = row['disease']
                color = self.disease_colors.get(disease, '#808080')
                size = 100 if row['severity'] == 'High' else 50
                
                m.scatter(x, y, s=size, c=color, alpha=0.6, edgecolor='black', linewidth=1)
                
                # Add to legend if disease not yet included
                if disease not in diseases_plotted:
                    legend_elements.append(plt.scatter([], [], c=color, label=disease))
                    diseases_plotted.add(disease)
        
        plt.legend(handles=legend_elements, title='Diseases', 
                  bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.title(title or 'Disease Outbreaks in East Africa')
        plt.tight_layout()
        plt.savefig('east_africa_map.png')
        plt.close()
        
    def plot_disease_severity_heatmap(self,
                                    region: str = 'uganda',
                                    title: Optional[str] = None,
                                    figsize: Tuple[int, int] = (12, 8)) -> None:
        """Plot disease severity heatmap."""
        if region == 'uganda':
            data = self.data[self.data['location'].apply(lambda x: x['is_uganda'])]
        elif region == 'east_africa':
            data = self.data[self.data['location'].apply(lambda x: x['is_east_africa'])]
        else:
            data = self.data
            
        # Create severity-disease matrix
        pivot_data = pd.crosstab(data['disease'], data['severity'])
        
        plt.figure(figsize=figsize)
        sns.heatmap(pivot_data, cmap='YlOrRd', annot=True, fmt='d', 
                   cbar_kws={'label': 'Number of Outbreaks'})
        
        plt.title(title or f'Disease Severity Heatmap - {region.title()}')
        plt.xlabel('Severity Level')
        plt.ylabel('Disease')
        plt.tight_layout()
        plt.savefig(f'disease_severity_heatmap_{region}.png')
        plt.close()
