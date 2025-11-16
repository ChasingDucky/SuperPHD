"""
Centralized data loader for sample university rankings
"""
import csv
import os

def load_sample_data_from_csv():
    """
    Load sample university rankings from CSV file
    Returns: dict with all ranking data organized by source
    """
    csv_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'sample_rankings.csv')

    data = {
        'qs': [],
        'the': [],
        'usnews': [],
        'arwu': [],
        'cs': []
    }

    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)

            for row in reader:
                name = row['university']
                country = row['country']

                # QS data
                if row.get('qs_rank'):
                    data['qs'].append({
                        'name': name,
                        'qs_rank': int(float(row['qs_rank'])),
                        'qs_score': float(row['qs_score']) if row.get('qs_score') else None,
                        'country': country
                    })

                # THE data
                if row.get('the_rank'):
                    data['the'].append({
                        'name': name,
                        'the_rank': int(float(row['the_rank'])),
                        'the_score': float(row['the_score']) if row.get('the_score') else None,
                        'country': country
                    })

                # US News data
                if row.get('usnews_rank'):
                    data['usnews'].append({
                        'name': name,
                        'usnews_rank': int(float(row['usnews_rank'])),
                        'usnews_score': float(row['usnews_score']) if row.get('usnews_score') else None,
                        'country': country
                    })

                # ARWU data
                if row.get('arwu_rank'):
                    data['arwu'].append({
                        'name': name,
                        'arwu_rank': int(float(row['arwu_rank'])),
                        'arwu_score': float(row['arwu_score']) if row.get('arwu_score') else None,
                        'country': country
                    })

                # CS Rankings data
                if row.get('cs_rank'):
                    data['cs'].append({
                        'name': name,
                        'cs_rank': int(float(row['cs_rank'])),
                        'cs_score': float(row['cs_score']) if row.get('cs_score') else None,
                        'country': country
                    })

        print(f"Loaded sample data: QS={len(data['qs'])}, THE={len(data['the'])}, "
              f"US News={len(data['usnews'])}, ARWU={len(data['arwu'])}, CS={len(data['cs'])}")

    except FileNotFoundError:
        print(f"Warning: Sample data CSV not found at {csv_path}")
        print("Using minimal fallback data")
        return get_minimal_fallback_data()
    except Exception as e:
        print(f"Error loading sample data: {e}")
        return get_minimal_fallback_data()

    return data

def get_minimal_fallback_data():
    """
    Minimal fallback data in case CSV is not available
    """
    return {
        'qs': [
            {'name': 'Massachusetts Institute of Technology (MIT)', 'qs_rank': 1, 'qs_score': 100.0, 'country': 'United States'},
            {'name': 'University of Cambridge', 'qs_rank': 2, 'qs_score': 99.2, 'country': 'United Kingdom'},
            {'name': 'Stanford University', 'qs_rank': 5, 'qs_score': 98.5, 'country': 'United States'},
        ],
        'the': [
            {'name': 'University of Oxford', 'the_rank': 1, 'the_score': 96.5, 'country': 'United Kingdom'},
            {'name': 'Stanford University', 'the_rank': 2, 'the_score': 95.8, 'country': 'United States'},
        ],
        'usnews': [
            {'name': 'Harvard University', 'usnews_rank': 1, 'usnews_score': 100.0, 'country': 'United States'},
            {'name': 'Massachusetts Institute of Technology (MIT)', 'usnews_rank': 2, 'usnews_score': 98.5, 'country': 'United States'},
        ],
        'arwu': [
            {'name': 'Harvard University', 'arwu_rank': 1, 'arwu_score': 100.0, 'country': 'United States'},
            {'name': 'Stanford University', 'arwu_rank': 2, 'arwu_score': 76.5, 'country': 'United States'},
        ],
        'cs': [
            {'name': 'Carnegie Mellon University', 'cs_rank': 1, 'cs_score': 7.2, 'country': 'United States'},
            {'name': 'Massachusetts Institute of Technology (MIT)', 'cs_rank': 2, 'cs_score': 6.8, 'country': 'United States'},
        ]
    }

# Load data once when module is imported
_SAMPLE_DATA = load_sample_data_from_csv()

def get_qs_sample_data():
    return _SAMPLE_DATA['qs']

def get_the_sample_data():
    return _SAMPLE_DATA['the']

def get_usnews_sample_data():
    return _SAMPLE_DATA['usnews']

def get_arwu_sample_data():
    return _SAMPLE_DATA['arwu']

def get_cs_sample_data():
    return _SAMPLE_DATA['cs']
