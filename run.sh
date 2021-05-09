#!/bin/bash

set -e

eval "$(conda shell.bash hook)"
conda activate env_for_wifi_location_dashboard

python plot_hiking_traces.py

open /Users/wuzhou_zhang/wuzhou-zhang.github.io/index.html
