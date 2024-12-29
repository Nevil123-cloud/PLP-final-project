# Disease Outbreak Tracker
## Focus: Africa, East Africa, and Uganda

This project analyzes disease outbreak data with a specific focus on African regions, particularly East Africa and Uganda. It provides tools for parsing news headlines, analyzing outbreak patterns, and visualizing the data.

## Features

### 1. Disease Parsing
- Intelligent parsing of news headlines
- Region classification (Africa, East Africa, Uganda)
- Disease type categorization
- Severity analysis
- Temporal data extraction

### 2. Africa-Focused Analysis
- Specialized analysis for:
  - Uganda-specific outbreaks
  - East African regional patterns
  - Disease distribution analysis
  - Severity trend analysis
  - Temporal pattern recognition

### 3. Visualization Capabilities
- Geographic heat maps of outbreaks
- Disease distribution charts
- Severity distribution visualizations
- Temporal trend analysis
- East Africa regional mapping

## Project Structure

```
discovering-disease-outbreaks/
├── data/
│   └── headlines.txt         # Raw headline data
├── src/
│   ├── disease_parser.py     # Headline parsing and classification
│   ├── africa_analyzer.py    # Africa-focused analysis tools
│   ├── visualizer.py         # Data visualization tools
│   └── main.py              # Main execution script
├── environment.yml          # Conda environment configuration
└── README.md               # Project documentation
```

## Setup and Installation

1. Create conda environment:
```bash
conda env create -f environment.yml
```

2. Activate environment:
```bash
conda activate discovering-disease-outbreaks
```

3. Run the analysis:
```bash
python src/main.py
```

## Key Components

### Disease Parser
- Processes news headlines
- Classifies regions and diseases
- Analyzes outbreak severity
- Extracts temporal information

### Africa Analyzer
- Filters data for African regions
- Analyzes disease patterns
- Generates statistical summaries
- Tracks high-priority outbreaks

### Visualizer
- Creates geographic visualizations
- Generates statistical plots
- Produces temporal trend analysis
- Displays regional distributions

## Data Analysis Features

### Regional Focus
- Uganda-specific analysis
- East African regional patterns
- Pan-African context

### Disease Categories
- High Priority: Ebola, Malaria, Cholera, Tuberculosis
- Medium Priority: HIV, Measles, Meningitis
- Low Priority: Influenza, Hepatitis

### Analysis Types
1. Geographic Distribution
   - Country-level analysis
   - Regional patterns
   - Outbreak clusters

2. Temporal Analysis
   - Outbreak trends
   - Seasonal patterns
   - Historical comparisons

3. Severity Assessment
   - High-priority outbreaks
   - Risk level classification
   - Impact analysis

## Usage Examples

```python
# Initialize parser and process headlines
parser = DiseaseOutbreakParser()
df = parser.process_headlines(headlines)

# Analyze Uganda-specific outbreaks
analyzer = AfricaOutbreakAnalyzer(df)
uganda_stats = analyzer.get_summary_statistics(region='uganda')

# Create visualizations
visualizer = OutbreakVisualizer(df)
visualizer.plot_east_africa_map()
visualizer.plot_disease_distribution(region='uganda')
```

## Dependencies
- Python 3.7
- pandas 0.25.0
- numpy 1.16.0
- matplotlib 3.1.1
- seaborn 0.9.0
- basemap 1.2.1
- scikit-learn 0.20.3

## Future Improvements
1. Real-time data integration
2. Machine learning for outbreak prediction
3. Interactive web dashboard
4. Mobile alerts system
5. API integration for live data
