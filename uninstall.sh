#!/usr/bin/env bash
set -euo pipefail

ENV_NAME="molecular_docking_workshop"
REPO_DIR="Basic-Molecular-Docking-Workshop"

# Where this script lives (parent of the repo)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_PATH="$SCRIPT_DIR/$REPO_DIR"

echo
echo "=== Uninstalling Molecular Docking Workshop ==="
echo

# 1. Remove conda environment if present and existing
eval "$(conda shell.bash hook)" 2>/dev/null || true
if command -v conda &>/dev/null; then
  # Check if the environment exists
  if conda env list | awk '{print $1}' | grep -qx "$ENV_NAME"; then
    if [ "${CONDA_DEFAULT_ENV:-}" = "$ENV_NAME" ]; then
      echo "-> Deactivating environment '$ENV_NAME'..."
      conda deactivate
    fi
    echo "-> Removing conda environment '$ENV_NAME'..."
    conda env remove --name "$ENV_NAME" -y
  else
    echo "-> Conda environment '$ENV_NAME' not found. Skipping environment removal."
  fi
else
  echo "Warning: 'conda' not found. Skipping environment removal."
fi

# 2. If inside the repo, cd out automatically
CURRENT_DIR="$(pwd)"
if [[ "$CURRENT_DIR" == "$REPO_PATH" ]] || [[ "$CURRENT_DIR" == "$REPO_PATH/"* ]]; then
  echo "-> You are inside '$REPO_PATH'. Moving up to home directory to proceed..."
  cd ~
fi

# 3. Remove the repository directory
if [ -d "$REPO_PATH" ]; then
  echo "-> Deleting directory '$REPO_PATH'..."
  rm -rf "$REPO_PATH"
else
  echo "-> Directory '$REPO_PATH' not found. Nothing to remove."
fi

echo
echo "✅ Uninstallation complete."
echo
