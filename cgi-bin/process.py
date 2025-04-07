#!/usr/bin/env python3

# This file takes an input file name, output filename, and column name, and then does fake geocoding on the file, and returns it.
# generated by ChatGPT 2025-04-07 

import sys
import pandas as pd
import random

def main():
    if len(sys.argv) != 4:
        print("Usage: process.py input.csv output.csv address_column", file=sys.stderr)
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]
    address_col = sys.argv[3]

    try:
        df = pd.read_csv(input_path)

        if address_col not in df.columns:
            print(f"Error: Column '{address_col}' not found in input CSV.", file=sys.stderr)
            sys.exit(2)

        # Generate fake lat/lon values
        df["lat"] = [round(random.uniform(40.5, 40.9), 6) for _ in range(len(df))]
        df["lon"] = [round(random.uniform(-74.25, -73.7), 6) for _ in range(len(df))]

        df.to_csv(output_path, index=False)
        print(f"Saved processed file to {output_path}")

    except Exception as e:
        print(f"Error processing file: {e}", file=sys.stderr)
        sys.exit(3)

if __name__ == "__main__":
    main()
