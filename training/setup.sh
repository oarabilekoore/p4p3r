#!/bin/bash
set -e

REPO=~/Projects/Paper.md
DATASET_SRC=~/PaperMdDataset/images/train
DATASET_DEST=$REPO/dataset

echo "=== PaperMd Fresh Setup ==="

# ── 1. Clean repo state ───────────────────────────────────────────────────────

cd $REPO

echo "\n[1/6] Cleaning repo..."

# Remove throwaway training scripts
rm -f training/d.py training/restore.py training/duplicate_finder.py

# Stage all intentional deletions
git add -A

# Commit clean state
git commit -m "chore: clean slate — remove website, layout-model, training scripts"
git push

echo "✓ Repo clean and pushed"

# ── 2. Create dataset folder structure ───────────────────────────────────────

echo "\n[2/6] Creating dataset structure..."

mkdir -p $DATASET_DEST/images/train
mkdir -p $DATASET_DEST/labels/json
mkdir -p $DATASET_DEST/models

echo "✓ Folders created"

# ── 3. Move images into repo ──────────────────────────────────────────────────

echo "\n[3/6] Moving images..."

cp $DATASET_SRC/* $DATASET_DEST/images/train/
echo "✓ $(ls $DATASET_DEST/images/train | wc -l) images copied to dataset/images/train"

# ── 4. Write data.yaml ────────────────────────────────────────────────────────

echo "\n[4/6] Writing data.yaml..."

cat > $DATASET_DEST/data.yaml << 'YAML'
path: /content/drive/MyDrive/PaperMdDataset
train: images/train
val: images/train

nc: 7
names:
  0: Abandon
  1: Plain_Text
  2: Formula
  3: Figure
  4: Table
  5: Link
  6: Callout
YAML

echo "✓ data.yaml written"

# ── 5. Initialise DVC ─────────────────────────────────────────────────────────

echo "\n[5/6] Initialising DVC..."

cd $REPO

# Init DVC if not already
if [ ! -d ".dvc" ]; then
  dvc init
fi

# Add Google Drive remote (PaperMdDataset folder)
dvc remote add -d gdrive gdrive://1lKTj3v2ctJC-1shLUAsvIy5l3o-FEuJ8 2>/dev/null || \
dvc remote modify gdrive url gdrive://1lKTj3v2ctJC-1shLUAsvIy5l3o-FEuJ8

# Track dataset folders
dvc add dataset/images
dvc add dataset/labels
dvc add dataset/models

# Add .dvc pointers and config to git
git add .dvc/config
git add dataset/images.dvc
git add dataset/labels.dvc
git add dataset/models.dvc
git add dataset/.gitignore
git add dataset/data.yaml
git commit -m "chore: init DVC, track dataset folders"
git push

echo "✓ DVC initialised"

# ── 6. Push data to Drive ─────────────────────────────────────────────────────

echo "\n[6/6] Pushing dataset to Google Drive..."
dvc push

echo "\n=== Done ==="
echo "Images  : $(ls $DATASET_DEST/images/train | wc -l)"
echo "Labels  : $(ls $DATASET_DEST/labels/json | wc -l)"
echo ""
echo "Next steps:"
echo "  1. Wipe Label Studio: rm ~/.local/share/label-studio/label_studio.sqlite3"
echo "  2. Start Label Studio and create a fresh project"
echo "  3. Add local storage pointing at: $DATASET_DEST/images/train"
echo "  4. After each annotation session run: ./training/scripts/save_annotations.sh"
