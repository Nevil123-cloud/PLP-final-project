import pandas as pd
from disease_parser import DiseaseOutbreakParser
from africa_analyzer import AfricaOutbreakAnalyzer
from visualizer import OutbreakVisualizer

def main():
    # Initialize parser
    parser = DiseaseOutbreakParser()
    
    # Read headlines from file
    with open("../data/headlines.txt", "r") as f:
        headlines = f.readlines()
    
    # Parse headlines
    print("Parsing headlines...")
    df = parser.process_headlines(headlines)
    
    # Initialize analyzer
    print("\nInitializing analyzer...")
    analyzer = AfricaOutbreakAnalyzer(df)
    
    # Get summary statistics for different regions
    print("\nSummary Statistics:")
    print("\nUganda:")
    uganda_stats = analyzer.get_summary_statistics(region='uganda')
    for key, value in uganda_stats.items():
        print(f"{key}: {value}")
        
    print("\nEast Africa:")
    ea_stats = analyzer.get_summary_statistics(region='east_africa')
    for key, value in ea_stats.items():
        print(f"{key}: {value}")
    
    # Get high priority outbreaks in Uganda
    print("\nHigh Priority Outbreaks in Uganda:")
    high_priority_ug = analyzer.get_high_priority_outbreaks(region='uganda')
    if not high_priority_ug.empty:
        print(high_priority_ug[['headline', 'disease', 'severity', 'date']])
    else:
        print("No high priority outbreaks found in Uganda")
    
    # Initialize visualizer
    print("\nGenerating visualizations...")
    visualizer = OutbreakVisualizer(df)
    
    # Create visualizations
    print("1. Disease Distribution in East Africa")
    visualizer.plot_disease_distribution(region='east_africa')
    
    print("2. Outbreak Severity in Uganda")
    visualizer.plot_severity_distribution(region='uganda')
    
    print("3. Temporal Trends in East Africa")
    visualizer.plot_temporal_trends(region='east_africa')
    
    print("4. East Africa Map")
    visualizer.plot_east_africa_map()
    
    print("5. Disease Severity Heatmap for Uganda")
    visualizer.plot_disease_severity_heatmap(region='uganda')
    
    print("\nAnalysis complete. Visualizations have been generated.")

if __name__ == "__main__":
    main()
