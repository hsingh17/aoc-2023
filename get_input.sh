#!/bin/bash

print_usage() {
    echo "Usage: ./get_input.sh --day <day> --output <path-to-output>"    
}

for arg in "$@"; do
  shift
  case "$arg" in
    '--day')   set -- "$@" '-d'   ;;
    '--output') set -- "$@" '-o'   ;;
    '--help')   set -- "$@" '-h'   ;;
    *)          set -- "$@" "$arg" ;;
  esac
done


day=0
output=""
while getopts "d:o:h" opt
do
  case "$opt" in
    'd') day=$OPTARG ;;
    'o') output=$OPTARG ;;
    'h') print_usage; exit 1;;
    '?') print_usage; exit 1 ;;
    '*') print_usage; exit 1 ;;
  esac
done

if [ $day -eq 0 ] || [ -z "$output" ]; then
    print_usage
    exit 1
fi


cookie=$(cat .cookie)
if [ -z "$cookie" ]; then
    echo "No .cookie file found! Please place your session cookie from the AOC website into a .cookie file!"
    exit 1
fi

url="https://adventofcode.com/2023/day/$day/input"
curl --get "$url" --cookie "session=$cookie" --output "$output"
echo "Got input for day $day and placed into $output"