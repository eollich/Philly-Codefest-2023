#!/bin/bash

# Generate random samples of .ics files

python3 ./ics_control.py generate "Software Developer" 4
python3 ./ics_control.py generate "UI_UX Designer" 4
python3 ./ics_control.py generate "Product Manager" 1
python3 ./ics_control.py generate "Software Test Engineer" 4

rm ./ics_files/*
mv *.ics ./ics_files
