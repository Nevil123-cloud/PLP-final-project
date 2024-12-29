import pandas as pd
from disease_parser import DiseaseOutbreakParser
from africa_analyzer import AfricaOutbreakAnalyzer
from visualizer import OutbreakVisualizer

def main():
    print("Disease Outbreak Analysis System for East Africa")
    print("=" * 50)
    
    # Initialize parser
    print("\n1. Initializing parser...")
    parser = DiseaseOutbreakParser()
    
    # Read headlines from file
    print("2. Reading headlines...")
    try:
        with open("data/headlines.txt", "r") as f:
            headlines = f.readlines()
        print(f"   Successfully loaded {len(headlines)} headlines")
    except FileNotFoundError:
        print("Error: headlines.txt not found in data directory")
        return
    
    # Parse headlines
    print("\n3. Parsing headlines and extracting information...")
    df = parser.process_headlines(headlines)
    print(f"   Processed {len(df)} entries")
    
    # Initialize analyzer
    print("\n4. Analyzing outbreak patterns...")
    analyzer = AfricaOutbreakAnalyzer(df)
    
    # Get summary statistics for different regions
    print("\n5. Summary Statistics:")
    
    regions = ['uganda', 'east_africa']
    for region in regions:
        print(f"\n{region.upper()}:")
        stats = analyzer.get_summary_statistics(region=region)
        
        print(f"   Total Outbreaks: {stats['total_outbreaks']}")
        print(f"   Unique Diseases: {stats['unique_diseases']}")
        print(f"   Date Range: {stats['date_range']['first_outbreak']} to {stats['date_range']['latest_outbreak']}")
        print("\n   Severity Distribution:")
        for severity, count in stats['severity_distribution'].items():
            print(f"   - {severity}: {count}")
    
    # Get high priority outbreaks
    print("\n6. High Priority Outbreaks in Uganda:")
    high_priority_ug = analyzer.get_high_priority_outbreaks(region='uganda')
    if not high_priority_ug.empty:
        print("\nRecent high-priority outbreaks:")
        for _, row in high_priority_ug.iterrows():
            print(f"   {row['date'].strftime('%Y-%m-%d')}: {row['disease']} - {row['severity']}")
            print(f"   Location: {row['location'].get('city', 'Unknown')}, {row['location'].get('country', 'Unknown')}")
            print(f"   Headline: {row['headline']}\n")
    else:
        print("   No high priority outbreaks found in Uganda")
    
    # Initialize visualizer and create visualizations
    print("\n7. Generating visualizations...")
    visualizer = OutbreakVisualizer(df)
    
    print("   Creating disease distribution plots...")
    visualizer.plot_disease_distribution(region='east_africa')
    visualizer.plot_disease_distribution(region='uganda')
    
    print("   Creating severity distribution plots...")
    visualizer.plot_severity_distribution(region='east_africa')
    visualizer.plot_severity_distribution(region='uganda')
    
    print("   Creating temporal trend plots...")
    visualizer.plot_temporal_trends(region='east_africa')
    visualizer.plot_temporal_trends(region='uganda')
    
    print("   Creating East Africa map...")
    visualizer.plot_east_africa_map()
    
    print("   Creating disease severity heatmaps...")
    visualizer.plot_disease_severity_heatmap(region='east_africa')
    visualizer.plot_disease_severity_heatmap(region='uganda')
    
    print("\n8. Analysis complete!")
    print("   Visualization files have been generated in the current directory:")
    print("   - disease_distribution_*.png")
    print("   - severity_distribution_*.png")
    print("   - temporal_trends_*.png")
    print("   - east_africa_map.png")
    print("   - disease_severity_heatmap_*.png")

if __name__ == "__main__":
    main()
