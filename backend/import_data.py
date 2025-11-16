"""
Import university ranking data from CSV file
"""
import csv
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models import Database

def import_from_csv(csv_file, db_path='rankings.db'):
    """
    Import university rankings from CSV file

    CSV format:
    university,country,qs_rank,qs_score,the_rank,the_score,usnews_rank,usnews_score,arwu_rank,arwu_score,cs_rank,cs_score
    """
    print(f"Importing data from {csv_file}...")

    db = Database(db_path)
    count = 0

    try:
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)

            for row in reader:
                # Convert empty strings to None
                data = {}
                for key, value in row.items():
                    if key == 'university':
                        continue  # Skip, will use as name
                    if key == 'country':
                        data['country'] = value if value else None
                    elif value and value.strip():
                        try:
                            # Try to convert to appropriate type
                            if 'rank' in key:
                                data[key] = int(float(value))
                            elif 'score' in key:
                                data[key] = float(value)
                            else:
                                data[key] = value
                        except ValueError:
                            data[key] = None
                    else:
                        data[key] = None

                # Add or update university
                name = row['university']
                db.add_or_update_university(name, **data)
                count += 1
                print(f"  Imported: {name}")

        print(f"\n✓ Successfully imported {count} universities")

    except FileNotFoundError:
        print(f"✗ Error: File {csv_file} not found")
        sys.exit(1)
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        db.close()

if __name__ == '__main__':
    # Get CSV file path from command line or use default
    if len(sys.argv) > 1:
        csv_file = sys.argv[1]
    else:
        csv_file = 'data/sample_rankings.csv'

    if len(sys.argv) > 2:
        db_path = sys.argv[2]
    else:
        db_path = 'rankings.db'

    print("=" * 60)
    print("University Rankings Data Importer")
    print("=" * 60)
    print()

    import_from_csv(csv_file, db_path)

    print()
    print("=" * 60)
    print("Import complete! You can now start the application.")
    print("=" * 60)
