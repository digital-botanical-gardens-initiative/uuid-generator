#!/bin/bash

# Help function
show_help() {
    cat << EOF
Usage: $(basename "$0") [--uuid y|n] [--organs y|n]

Options:
  --uuid y|n       Add a UUID qr code on the label (default: 'y')
  --organs y|n     Include checkboxes for organs (default: 'y')
  --number <num>   Number of labels to generate (default: 10)
  --path <path>    Path to save the labels (default: current directory)
  -h, --help       Show help

Example to generate a label with a UUID and no organs checkboxes:
  ./$(basename "$0") --uuid y --organs n
EOF
}

# Run a script and check its return code
run_script() {
    script=$1.py
    number=$2
    path=$3
    uuid=$4
    organs=$5

    poetry run python3 $script $number $path $uuid $organs

    if [ $? -ne 0 ]; then
        echo "$script_name failed"
        exit 1
    fi
}

# Show help if requested
if [[ "$1" == "-h" || "$1" == "--help" ]]; then
    show_help
    exit 0
fi

# Default values
uuid="y"
organs="y"
number=15
path="../output"

# Parse arguments
while [[ $# -gt 0 ]]; do
    key="$1"

    case $key in
        --uuid)
            uuid="$2"
            shift # past argument
            shift # past value
            ;;
        --organs)
            organs="$2"
            shift
            shift
            ;;
        --number)
            number="$2"
            shift
            shift
            ;;
        --path)
            path="$2"
            shift
            shift
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Validate uuid input
if [[ "$uuid" != "y" && "$uuid" != "n" ]]; then
    echo "Error: --uuid must be 'y' or 'n'"
    exit 1
fi

# Validate organs input
if [[ "$organs" != "y" && "$organs" != "n" ]]; then
    echo "Error: --organs must be 'y' or 'n'"
    exit 1
fi

# Validate number input (must be a strictly positive integer)
if ! [[ "$number" =~ ^[1-9][0-9]*$ ]]; then
    echo "Error: --number must be a strictly positive integer"
    exit 1
fi

# Validate path input (must exist and be a directory)
if [[ ! -d "$path" ]]; then
    echo "Error: --path '$path' does not exist or is not a directory"
    exit 1
fi

# Launch script
if [[ "$uuid" == "y" || "$organs" == "y" ]]; then
    run_script label_generator $number $path $uuid $organs
fi

# If both options are 'n', show an error message
if [[ "$uuid" == "n" && "$organs" == "n" ]]; then
    echo "You need to select at least one option."
    exit 1
fi
