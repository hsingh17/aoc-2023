#!/bin/bash

print_usage() {
    echo "Usage: ./setup_day.sh --day <day>"    
}

for arg in "$@"; do
  shift
  case "$arg" in
    '--day')   set -- "$@" '-d'   ;;
    '--help')   set -- "$@" '-h'   ;;
    *)          set -- "$@" "$arg" ;;
  esac
done


day=0
while getopts "d:o:h" opt
do
  case "$opt" in
    'd') day=$OPTARG ;;
    'h') print_usage; exit 1;;
    '?') print_usage; exit 1 ;;
    '*') print_usage; exit 1 ;;
  esac
done

if [ $day -eq 0 ]; then
    print_usage
    exit 1
fi

# Create folder structure
mkdir "$day"
mkdir "$day/input" "$day/sol"
touch "$day/input/sample.txt"
cp "template.py" "$day/sol/$day.py"

# Get input for the day's challenge
cookie=$(cat .cookie)
if [ -z "$cookie" ]; then
    echo "No .cookie file found! Please place your session cookie from the AOC website into a .cookie file!"
    exit 1
fi

output=$day/input/input.txt
url="https://adventofcode.com/2023/day/$day/input"
curl --get "$url" --cookie "session=$cookie" --output "$output"
echo "Got input for day $day and placed into $output"