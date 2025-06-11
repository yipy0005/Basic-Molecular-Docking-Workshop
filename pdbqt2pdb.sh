#!/bin/bash

if [ "$#" -ne 1 ]; then
  echo "Usage: $0 <input_file.pdbqt>"
  exit 1
fi

input_file="$1"
base_name="${input_file%.*}"    # strip off the .pdbqt

if [ ! -f "$input_file" ]; then
  echo "File $input_file not found!"
  exit 1
fi

# Split out each MODEL into base_name_model1.pdbqt, base_name_model2.pdbqt, …
awk -v base="$base_name" '
    /^MODEL/ {
        if (NR > 1) {
            close(outfile)
        }
        outfile = base "_model" ++model_num ".pdbqt"
        print > outfile
        next
    }
    { print > outfile }
    END {
        close(outfile)
    }
' "$input_file"

echo "Models have been extracted to ${base_name}_model*.pdbqt."

# Convert each .pdbqt to .pdb (first 66 columns), then remove the .pdbqt
for f in "${base_name}"_model*.pdbqt; do
  pdb="${f%.pdbqt}.pdb"
  cut -c-66 "$f" > "$pdb"
  rm -f "$f"
  echo "  → Converted to $pdb and removed $f"
done

echo "All models converted to .pdb and intermediate .pdbqt files cleaned up."
