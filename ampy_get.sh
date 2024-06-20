#!/bin/bash

# Check if at least one argument (the first file name) is provided
if [ -z "$1" ]; then
  echo "Usage: $0 <source_file> [destination_file]"
  exit 1
fi

# Assign the first parameter to the source file variable
SOURCE_FILE=$1

# Run the ampy command with sudo
sudo ampy --port /dev/ttyUSB0 --baud 115200 get "$SOURCE_FILE"
