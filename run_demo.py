import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def show_test_sites() -> None:
    """Prints the configured test websites from data/test_sites.csv."""
    csv_path = ROOT / "data" / "test_sites.csv"
    print(f"Reading test sites from: {csv_path}\n")

    with csv_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        print("Configured test sites:")
        for row in reader:
            print(
                f"- {row['site_name']} ({row['category']}): {row['url']}\n"
                f"  Pages to test: {row['pages_to_test']}\n"
                f"  Expected: {row['expected_functionality']}\n"
            )


def show_annotation_schema() -> None:
    """Prints the required fields from data/annotation_schema.json."""
    schema_path = ROOT / "data" / "annotation_schema.json"
    print(f"\nReading annotation schema from: {schema_path}\n")

    with schema_path.open(encoding="utf-8") as f:
        schema = json.load(f)

    required_fields = schema.get("required", [])
    print("Required annotation fields:")
    for field in required_fields:
        print(f"- {field}")


if __name__ == "__main__":
    show_test_sites()
    show_annotation_schema()
