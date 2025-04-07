#!/bin/bash
# handles file upload from py-upload.js on html page
# Runs the python script that processes the file
# got from ChatGPT 2025-03-12 14:00

# Set up temporary files
UPLOAD_DIR="/tmp"
INPUT_FILE=$(mktemp --suffix=.csv)
OUTPUT_FILE=$(mktemp --suffix=.csv)
TMP=$(mktemp)

# Read entire request into TMP
cat > "$TMP"

# Extract column name
column_name=$(grep -A 2 'name="column"' "$TMP" | tail -n 1 | tr -d '\r')

# Extract the CSV file content
# Assumes it's the first file field in the form
csvoffset=$(grep -n 'name="file"' "$TMP" | cut -d: -f1)
csvoffset=$((csvoffset + 2))
tail -n +"$csvoffset" "$TMP" | sed '/^--.*--$/q' > "$INPUT_FILE"

# Call the python script
python3 /var/www/cgi-bin/process.py "$INPUT_FILE" "$OUTPUT_FILE" "$column_name"
# (python3 is in /sbin/, you may need to add that.)

# Return the CSV
echo "Content-Type: text/csv"
echo "Content-Disposition: attachment; filename=processed.csv"
echo

cat "$OUTPUT_FILE"

# Cleanup
rm -f "$INPUT_FILE" "$OUTPUT_FILE" "$TMP"
