#!/usr/bin/env bash
set -e

# Run this from the root of paper.md/
# chmod +x restructure.sh && ./restructure.sh

echo "→ Creating new directory tree..."

mkdir -p apps/web/app/routes
mkdir -p apps/web/app/components/canvas
mkdir -p apps/web/app/components/upload
mkdir -p apps/web/app/components/ui
mkdir -p apps/web/app/workers
mkdir -p apps/web/app/hooks
mkdir -p apps/web/app/store
mkdir -p apps/web/public/models

mkdir -p packages/types/src
mkdir -p packages/layout-model/src
mkdir -p packages/figure-model/src
mkdir -p packages/ink-runtime/src/detectors
mkdir -p packages/ink-runtime/src/processors
mkdir -p packages/ink-runtime/src/ocr
mkdir -p packages/excalidraw-renderer/src/elements

mkdir -p training/notebooks
mkdir -p training/scripts
mkdir -p training/backend
mkdir -p training/research/scripts
mkdir -p training/research/test_data

echo "→ Moving Python scripts..."
mv annotation.sh     training/scripts/annotation.sh
mv label_images.py   training/scripts/label_images.py
mv model.py          training/scripts/model.py

echo "→ Moving model weights..."
mv models/           training/models/
[ -f latest.pt ] && mv latest.pt training/models/latest.pt

echo "→ Moving label-studio backend..."
[ -d my_backend ] && mv my_backend/ training/backend/

echo "→ Moving research..."
[ -f research/Research_Findings_Layout_Analysis.md ] && \
  mv research/Research_Findings_Layout_Analysis.md training/research/
[ -f research/Research_Findings_YOLOv11_Nano_Inference_Analysis_and_Data_Normalization_Protocols.md ] && \
  mv research/Research_Findings_YOLOv11_Nano_Inference_Analysis_and_Data_Normalization_Protocols.md training/research/
[ -d research/scripts ] && cp -r research/scripts/. training/research/scripts/
[ -d research/test_data ] && cp -r research/test_data/. training/research/test_data/
rm -rf research/

echo "→ Fixing ATTRIBBUTION.md typo..."
mv ATTRIBBUTION.md ATTRIBUTION.md

echo "→ Updating paths inside annotation.sh..."
sed -i \
  -e 's|cp latest.pt ./my_backend/|cp ../models/latest.pt ./backend/|g' \
  -e 's|label-studio-ml init my_backend|label-studio-ml init backend|g' \
  -e 's|label-studio-ml start ./my_backend|label-studio-ml start ./backend|g' \
  training/scripts/annotation.sh

echo "→ Cleaning pycache..."
find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
find . -name "*.pyc" -delete 2>/dev/null || true

echo "→ Writing .gitignore..."
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.pyc
*.pyo
.venv/
*.egg-info/

# Model weights (large files — use git-lfs or keep local)
*.pt
*.onnx
training/models/

# Node / Bun
node_modules/
.next/
dist/
build/
.turbo/

# Label Studio backend (generated)
training/backend/

# OS
.DS_Store
Thumbs.db

# Env
.env
.env.local
EOF

echo "→ Writing root package.json..."
cat > package.json << 'EOF'
{
  "name": "papermd",
  "private": true,
  "workspaces": [
    "apps/*",
    "packages/*"
  ],
  "scripts": {
    "dev":   "bun run --cwd apps/web dev",
    "build": "bun run --cwd apps/web build",
    "lint":  "bun run --cwd apps/web lint"
  }
}
EOF

echo "→ Writing tsconfig.base.json..."
cat > tsconfig.base.json << 'EOF'
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "strict": true,
    "declaration": true,
    "skipLibCheck": true,
    "paths": {
      "@papermd/types":                ["./packages/types/src/index.ts"],
      "@papermd/layout-model":         ["./packages/layout-model/src/index.ts"],
      "@papermd/figure-model":         ["./packages/figure-model/src/index.ts"],
      "@papermd/ink-runtime":          ["./packages/ink-runtime/src/index.ts"],
      "@papermd/excalidraw-renderer":  ["./packages/excalidraw-renderer/src/index.ts"]
    }
  }
}
EOF

echo "→ Writing stub package.json files for each package..."

for pkg in types layout-model figure-model ink-runtime excalidraw-renderer; do
cat > packages/$pkg/package.json << EOF
{
  "name": "@papermd/$pkg",
  "version": "0.0.1",
  "private": true,
  "main": "src/index.ts",
  "scripts": {
    "build": "bun build src/index.ts --outdir dist"
  }
}
EOF
touch packages/$pkg/src/index.ts
done

echo "→ Writing stub index files..."
echo "// AST types — Document, Page, Element, BBox etc." > packages/types/src/index.ts
echo "// YOLO inference — preprocess, run, postprocess"  > packages/layout-model/src/index.ts
echo "// Figure subclassifier — v2"                      > packages/figure-model/src/index.ts
echo "// Ink Runtime — crops to AST nodes"               > packages/ink-runtime/src/index.ts
echo "// AST to Excalidraw JSON"                         > packages/excalidraw-renderer/src/index.ts

echo ""
echo "✓ Done. Final structure:"
find . \
  -not -path "./.git/*" \
  -not -path "./node_modules/*" \
  | sort | sed 's|[^/]*/|  |g'
