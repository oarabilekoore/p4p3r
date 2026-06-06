source .venv/bin/activate
rm -rf my_backend
label-studio-ml init backend
cp ../models/latest.pt ./backend/
LABEL_STUDIO_LOCAL_FILES_DOCUMENT_ROOT=/home/vaseline/mnt/gdrive/PaperMdDataset/ label-studio-ml start ./backend
