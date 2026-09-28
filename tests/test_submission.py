import os
import json
import csv
import unittest
from jsonschema import validate, ValidationError

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCHEMA_PATH = os.path.join(BASE_DIR, "schemas", "sdk_schema.json")
SDK_DB_PATH = os.path.join(BASE_DIR, "sdk_database.json")
TEMPLATE_SDK_DB_PATH = os.path.join(BASE_DIR, "templates", "sdk_database_template.json")
APPS_ANALYSIS_PATH = os.path.join(BASE_DIR, "apps_analysis.csv")
TEMPLATE_APPS_ANALYSIS_PATH = os.path.join(BASE_DIR, "templates", "apps_analysis_template.csv")
REPORT_PATH = os.path.join(BASE_DIR, "REPORT.md")


class TestSDKAnalysisSubmission(unittest.TestCase):

    def _get_sdk_db_file(self):
        if os.path.exists(SDK_DB_PATH):
            return SDK_DB_PATH
        elif os.path.exists(TEMPLATE_SDK_DB_PATH):
            return TEMPLATE_SDK_DB_PATH
        self.fail("Neither sdk_database.json nor templates/sdk_database_template.json found.")

    def _get_apps_analysis_file(self):
        if os.path.exists(APPS_ANALYSIS_PATH):
            return APPS_ANALYSIS_PATH
        elif os.path.exists(TEMPLATE_APPS_ANALYSIS_PATH):
            return TEMPLATE_APPS_ANALYSIS_PATH
        self.fail("Neither apps_analysis.csv nor templates/apps_analysis_template.csv found.")

    def test_01_schema_exists(self):
        """Verify that JSON Schema file exists."""
        self.assertTrue(os.path.exists(SCHEMA_PATH), f"Schema file missing at {SCHEMA_PATH}")

    def test_02_sdk_database_schema_and_count(self):
        """Verify that sdk_database.json matches JSON schema and has >= 15 SDK entries."""
        db_file = self._get_sdk_db_file()
        
        with open(SCHEMA_PATH, "r", encoding="utf-8") as sf:
            schema = json.load(sf)
            
        with open(db_file, "r", encoding="utf-8") as df:
            db_data = json.load(df)

        try:
            validate(instance=db_data, schema=schema)
        except ValidationError as e:
            self.fail(f"SDK database validation failed against schema: {e.message}")

        sdks = db_data.get("sdks", [])
        self.assertGreaterEqual(len(sdks), 15, f"Expected at least 15 SDKs in database, found {len(sdks)}")

        # Check unique IDs
        sdk_ids = [sdk["id"] for sdk in sdks]
        self.assertEqual(len(sdk_ids), len(set(sdk_ids)), "Duplicate SDK IDs found in database")

        # Check category diversity
        categories = set(sdk["category"] for sdk in sdks)
        required_cats = {"analytics", "push", "payments"}
        missing_cats = required_cats - categories
        self.assertFalse(missing_cats, f"Database missing key SDK categories: {missing_cats}")

    def test_03_apps_analysis_structure(self):
        """Verify apps_analysis.csv contains >= 10 rows and valid references to SDK database."""
        db_file = self._get_sdk_db_file()
        with open(db_file, "r", encoding="utf-8") as df:
            db_data = json.load(df)
        valid_sdk_ids = set(sdk["id"] for sdk in db_data.get("sdks", []))

        csv_file = self._get_apps_analysis_file()
        with open(csv_file, "r", encoding="utf-8") as cf:
            reader = csv.DictReader(cf)
            rows = list(reader)

        self.assertGreaterEqual(len(rows), 10, f"Expected analysis of at least 10 APKs, found {len(rows)}")

        required_cols = {"app_name", "package_name", "category", "detected_sdks", "detection_evidence"}
        for i, row in enumerate(rows, 1):
            missing_cols = required_cols - set(row.keys())
            self.assertFalse(missing_cols, f"Row {i} missing columns: {missing_cols}")
            self.assertTrue(row["app_name"].strip(), f"Row {i} has empty app_name")
            self.assertTrue(row["package_name"].strip(), f"Row {i} has empty package_name")
            self.assertTrue(row["detection_evidence"].strip(), f"Row {i} has empty detection_evidence")

            # Check detected SDKs exist in database
            raw_sdks = [s.strip() for s in row["detected_sdks"].split(",") if s.strip()]
            self.assertGreater(len(raw_sdks), 0, f"Row {i} ({row['app_name']}) has no detected_sdks listed")
            for sdk_id in raw_sdks:
                self.assertIn(
                    sdk_id, valid_sdk_ids,
                    f"Row {i} ({row['app_name']}) references unknown SDK ID '{sdk_id}'. "
                    f"It must be present in sdk_database.json"
                )

    def test_04_report_content(self):
        """Verify REPORT.md exists and is substantive if present."""
        if os.path.exists(REPORT_PATH):
            with open(REPORT_PATH, "r", encoding="utf-8") as rf:
                content = rf.read().strip()
            self.assertGreater(len(content), 100, "REPORT.md is too short (fewer than 100 characters)")


if __name__ == "__main__":
    unittest.main()
