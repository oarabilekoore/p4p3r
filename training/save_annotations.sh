#!/bin/bash
set -e

REPO=~/Projects/Paper.md
JSON_SRC=~/.local/share/label-studio/export  # update if different
JSON_DEST=$REPO/dataset/labels/json
COUNT=$(ls $JSON_DEST | wc -l)

cp -r $JSON_SRC/* $JSON_DEST/ 2>/dev/null || true

cd $REPO
dvc add dataset/labels
git add dataset/labels.dvc
git commit -m "annotations: $(date +%Y%m%d_%H%M) — $COUNT files"
git push
dvc push

echo "✓ Annotations saved ($COUNT files)"
