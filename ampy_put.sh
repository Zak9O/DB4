#!/bin/bash

# Check if at least one argument (the first file name) is provided
if [ -z "$1" ]; then
  echo "Usage: $0 <source_file> [destination_file]"
  exit 1
fi

# Assign the first parameter to the source file variable
SOURCE_FILE=$1

# Assign the second parameter to the destination file variable if provided
# If not provided, set it to an empty string
DEST_FILE=${2:-}

# Run the ampy command with sudo
if [ -z "$DEST_FILE" ]; then
  sudo ampy --port /dev/ttyUSB0 --baud 115200 put "$SOURCE_FILE"
else
  sudo ampy --port /dev/ttyUSB0 --baud 115200 put "$SOURCE_FILE" "$DEST_FILE"
fi
