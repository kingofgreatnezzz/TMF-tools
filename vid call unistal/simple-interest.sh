#!/bin/bash
# Simple Interest Calculator

principal=$1
rate=$2
time=$3

interest=$(echo "$principal * $rate * $time / 100" | bc)
echo "Simple Interest: $interest"
