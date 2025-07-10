#!/usr/bin/env bash
set -euo pipefail

# Resolve work dir to absolute path (default ~/Documents)
WORK_DIR="."
#WORK_DIR="${1:-$HOME/Documents}"
WORK_DIR="$(realpath "$WORK_DIR")"
REPO_URL="https://github.com/yipy0005/Basic-Molecular-Docking-Workshop.git"
#REPO_DIR="Basic-Molecular-Docking-Workshop"
#REPO_PATH="$WORK_DIR/$REPO_DIR"
ENV_NAME="molecular_docking_workshop"
MEEKO_URL="https://github.com/forlilab/Meeko.git"
CHEM_URL="https://github.com/yipy0005/chemdraw.git"

echo
echo "=== Basic Molecular Docking Workshop Setup ==="
echo

# 1. Check for conda
if ! command -v conda &>/dev/null; then
  echo "Error: 'conda' not found. Please install Anaconda first:"
  echo "  https://www.anaconda.com/products/distribution"
  exit 1
fi
eval "$(conda shell.bash hook)"

# 2. Clone or update workshop repo
#$echo "-> Cloning/updating workshop repository in $WORK_DIR"
#$cd "$WORK_DIR"
#$if [ -d "$REPO_PATH/.git" ]; then
#$  git -C "$REPO_PATH" pull
#$else
#$  git clone "$REPO_URL"
#$fi

# 3. Create the conda env if needed
echo
echo "-> Ensuring conda env '$ENV_NAME' exists"
if conda env list | awk '{print $1}' | grep -qx "$ENV_NAME"; then
  echo "   Environment already exists."
else
  conda env create -f "$WORK_DIR/environment.yml"
fi

# 4. Activate it
echo
echo "-> Activating '$ENV_NAME'"
conda activate "$ENV_NAME"

# 5. Install Meeko & ProDy
echo
echo "-> Installing Meeko (develop) & ProDy"
# if Meeko isn't already cloned, git clone creates the folder
if [ ! -d "$WORK_DIR/Meeko/.git" ]; then
  git clone "$MEEKO_URL" "$WORK_DIR/Meeko"
fi
cd "$WORK_DIR/Meeko"
git fetch --all
git checkout develop
pip install -e .
pip install prody

# 6. Install chemical editor (chemdraw)
echo
echo "-> Installing chemical editor 'chemdraw'"
if [ ! -d "$WORK_DIR/chemdraw/.git" ]; then
  git clone "$CHEM_URL" "$WORK_DIR/chemdraw"
fi
cd "$WORK_DIR/chemdraw"
pip install -e .
echo "-> 'chemdraw' installed. You can now launch it by typing 'chemdraw'"

# 7. Verify tools
echo
echo "-> Verifying your setup"
echo -n "   vina:   " && which vina || echo "NOT FOUND"
echo -n "   reduce: " && which reduce || echo "NOT FOUND"
echo -n "   python: " && python --version

# 8. Make pdbqt2pdb.sh executable
echo
echo "-> Making pdbqt2pdb.sh executable"
chmod +x "$WORK_DIR/pdbqt2pdb.sh"

echo
echo "✅  Setup complete!"
echo "    cd $WORK_DIR"
echo "    conda activate $ENV_NAME"
echo "    bash TUTORIAL.md"
echo
