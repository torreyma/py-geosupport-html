#!/usr/bin/env python3

import cgi
import os
import sys
import tempfile
import subprocess
import shutil

def main():
    print("Content-Type: text/csv")
    print("Content-Disposition: attachment; filename=processed-py.csv")
    print()

    form = cgi.FieldStorage()

    required_fields = ["file", "building_col", "street_col", "zip_col"]
    if not all(field in form for field in required_fields):
        print("Missing one or more form fields.", file=sys.stderr)
        sys.exit(1)

    file_item = form["file"]
    building_col = form.getvalue("building_col")
    street_col = form.getvalue("street_col")
    zip_col = form.getvalue("zip_col")

    if not file_item.file or not building_col or not street_col or not zip_col:
        print("Empty form field received.", file=sys.stderr)
        sys.exit(1)

    # Save uploaded file to temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv", dir="/tmp") as input_file:
        shutil.copyfileobj(file_item.file, input_file)
        input_path = input_file.name

    # Set required Geosupport environment variables
    env = os.environ.copy()
    env["LD_LIBRARY_PATH"] = "/usr/share/R/library/geocoding_tests/version-24d_24.4/lib/"
    env["GEOFILES"] = "/usr/share/R/library/geocoding_tests/version-24d_24.4/fls/"

    # Call the process.py script using python3 from the conda environment that has pandas and geosupport installed
    try:
        subprocess.run(
            ["/opt/py-geosupport-conda-env/bin/python3", "/var/www/cgi-bin/process.py",
             input_path, building_col, street_col, zip_col],
            check=True,
            stdout=sys.stdout,
            stderr=sys.stderr,
            env=env
        )
    except subprocess.CalledProcessError as e:
        print(f"Error during processing: {e}", file=sys.stderr)

    # Cleanup temp file
    os.remove(input_path)

if __name__ == "__main__":
    main()
