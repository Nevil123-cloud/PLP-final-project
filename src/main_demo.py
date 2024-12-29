import pandas as pd
import matplotlib.pyplot as plt
from disease_parser import DiseaseOutbreakParser
from africa_analyzer import AfricaOutbreakAnalyzer
from visualizer import OutbreakVisualizer

def main():
    # Read headlines from file
    print("Reading headlines...")
    with open("data/headlines.txt", "r") as f:
        headlines = f.readlines()
    
    # Initialize parser
    print("\nInitializing parser...")
    parser = DiseaseOutbreakParser()
    
    # Parse headlines
    print("Parsing headlines...")
    df = parser.process_headlines(headlines)
    
    # Initialize analyzer
    print("\nAnalyzing data...")
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
    
    # Get high priority outbreaks in East Africa
    print("\nHigh Priority Outbreaks in East Africa:")
    high_priority_ea = analyzer.get_high_priority_outbreaks(region='east_africa')
    if not high_priority_ea.empty:
        print(high_priority_ea[['headline', 'disease', 'severity', 'date']])
    else:
        print("No high priority outbreaks found in East Africa")
    
    # Initialize visualizer
    print("\nGenerating visualizations...")
    visualizer = OutbreakVisualizer(df)
    
    # Create visualizations
    print("1. Disease Distribution in East Africa")
    visualizer.plot_disease_distribution(region='east_africa')
    plt.savefig('disease_distribution_ea.png')
    plt.close()
    
    print("2. Outbreak Severity in Uganda")
    visualizer.plot_severity_distribution(region='uganda')
    plt.savefig('severity_distribution_uganda.png')
    plt.close()
    
    print("3. Temporal Trends in East Africa")
    visualizer.plot_temporal_trends(region='east_africa')
    plt.savefig('temporal_trends_ea.png')
    plt.close()
    
    print("4. East Africa Map")
    visualizer.plot_east_africa_map()
    plt.savefig('east_africa_map.png')
    plt.close()
    
    print("5. Disease Severity Heatmap for Uganda")
    visualizer.plot_disease_severity_heatmap(region='uganda')
    plt.savefig('disease_severity_heatmap_uganda.png')
    plt.close()
    
    print("\nAnalysis complete. Visualizations have been saved as PNG files.")
    print("\nKey findings:")
    print(f"- Total outbreaks in East Africa: {ea_stats['total_outbreaks']}")
    print(f"- Most common disease in East Africa: {ea_stats['most_common_disease']}")
    print(f"- High severity outbreaks in East Africa: {ea_stats['high_severity_count']}")
    print(f"- Total outbreaks in Uganda: {uganda_stats['total_outbreaks']}")
    print(f"- Most common disease in Uganda: {uganda_stats['most_common_disease']}")
    print(f"- High severity outbreaks in Uganda: {uganda_stats['high_severity_count']}")

if __name__ == "__main__":
    main()
