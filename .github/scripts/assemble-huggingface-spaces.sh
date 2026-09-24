#!/usr/bin/env bash
set -euo pipefail

full_dir=".space-deploy"

for target in "$full_dir"; do
  mkdir -p "$target/II_statistical_analysis/gradio" "$target/_data"
  cp II_statistical_analysis/gradio/app.py "$target/II_statistical_analysis/gradio/app.py"
  cp II_statistical_analysis/gradio/requirements.txt "$target/requirements.txt"
  cp _data/speeches.parquet "$target/_data/speeches.parquet"
  cp _data/interruptions.parquet "$target/_data/interruptions.parquet"
  cp _data/interruptions_labeled.parquet "$target/_data/interruptions_labeled.parquet"
  cp _data/bt_period_data.json "$target/_data/bt_period_data.json"
done

cp II_statistical_analysis/gradio/README.space.md "$full_dir/README.md"
