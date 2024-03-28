#!/bin/bash

timestamp=$(date +%s)
project=boranga
output_folder=diagrams/erd
filename=$project$timestamp

echo "Generating ERD for $project"

python manage.py graph_models boranga -o $filename.dot
dot -Tpdf $filename.dot -o $output_folder/$filename.pdf
rm -f $filename.dot

echo "ERD file generated: $output_folder/$filename.pdf"
