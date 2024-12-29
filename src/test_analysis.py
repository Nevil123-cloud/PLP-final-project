import unittest
import pandas as pd
from disease_parser import DiseaseOutbreakParser
from africa_analyzer import AfricaOutbreakAnalyzer
from visualizer import OutbreakVisualizer

class TestDiseaseOutbreakAnalysis(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Sample test headlines with more diverse diseases
        cls.test_headlines = [
            "Ebola outbreak in Kampala",
            "Malaria is Spreading in Johannesburg",
            "Lower Hospitalization in Entebbe after Rabies Vaccine becomes Mandatory",
            "Tourist Perishes from Malaria in Arusha",
            "The Spread of Malaria in Zanzibar has been Confirmed",
            "Cholera outbreak in Dakar",
            "Ebola outbreak in Kampala claims more lives",
            "Tuberculosis cases rise in Nairobi",
            "HIV infections increase in Dar es Salaam"
        ]
        
        # Initialize parser
        cls.parser = DiseaseOutbreakParser()
        
        # Process headlines
        cls.df = cls.parser.process_headlines(cls.test_headlines)
        
        # Initialize analyzer and visualizer
        cls.analyzer = AfricaOutbreakAnalyzer(cls.df)
        cls.visualizer = OutbreakVisualizer(cls.df)

    def test_parser_functionality(self):
        """Test the parser's ability to extract relevant information."""
        result = self.parser.parse_headline("Ebola outbreak in Kampala")
        
        self.assertEqual(result['disease'], 'Ebola')
        self.assertTrue(result['location']['is_uganda'])
        self.assertTrue(result['location']['is_east_africa'])
        self.assertEqual(result['severity'], 'High')

    def test_uganda_filtering(self):
        """Test filtering of Uganda-specific data."""
        uganda_data = self.analyzer._filter_uganda_data()
        
        # Should contain Kampala and Entebbe entries
        self.assertGreater(len(uganda_data), 0)
        
        # Verify Uganda locations
        for _, row in uganda_data.iterrows():
            self.assertTrue(row['location']['is_uganda'])

    def test_east_africa_filtering(self):
        """Test filtering of East African data."""
        ea_data = self.analyzer._filter_east_africa_data()
        
        # Should contain entries from East African countries
        self.assertGreater(len(ea_data), 0)
        
        # Verify East African locations
        for _, row in ea_data.iterrows():
            self.assertTrue(row['location']['is_east_africa'])

    def test_disease_distribution(self):
        """Test disease distribution analysis."""
        distribution = self.analyzer.analyze_disease_distribution(region='east_africa')
        
        # Verify that we have disease counts
        self.assertGreater(len(distribution), 0)
        
        # Verify that Malaria and Ebola are present in the distribution
        self.assertIn('Malaria', distribution)
        self.assertIn('Ebola', distribution)

    def test_severity_analysis(self):
        """Test severity analysis functionality."""
        severity_trends = self.analyzer.analyze_severity_trends(region='uganda')
        
        # Verify that we have severity classifications
        self.assertGreater(len(severity_trends), 0)
        
        # Verify that we have some high severity cases
        self.assertIn('High', severity_trends)

    def test_high_priority_outbreaks(self):
        """Test identification of high priority outbreaks."""
        high_priority = self.analyzer.get_high_priority_outbreaks(region='east_africa')
        
        # Verify that high priority outbreaks are identified
        self.assertGreater(len(high_priority), 0)
        
        # Verify that all returned outbreaks are high severity
        for _, row in high_priority.iterrows():
            self.assertEqual(row['severity'], 'High')

    def test_summary_statistics(self):
        """Test generation of summary statistics."""
        stats = self.analyzer.get_summary_statistics(region='east_africa')
        
        # Verify that we have all expected statistical measures
        expected_keys = {'total_outbreaks', 'unique_diseases', 
                        'severity_distribution', 'most_common_disease', 
                        'high_severity_count'}
        self.assertTrue(all(key in stats for key in expected_keys))
        
        # Verify that statistics are reasonable
        self.assertGreater(stats['total_outbreaks'], 0)
        self.assertGreater(stats['unique_diseases'], 0)

def run_tests():
    unittest.main(argv=[''], verbosity=2)

if __name__ == '__main__':
    run_tests()
