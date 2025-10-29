# Molecular Docking Tutorial

After you have activated the `molecular_docking_workshop` environment, follow these steps to prepare your files and run a docking calculation using AutoDock Vina.

---

## 1. Navigate to the `input_files` Folder

In your terminal, make sure you are within the workshop repository, then change into the `input_files` directory:

```bash
cd input_files
```

This folder contains the receptor and ligand files needed for docking.

---

## 2. (Optional) Prepare Protein Structure

If you have a PDB or CIF file with waters and ligands that need to be removed, use the `prepare_protein.py` script:

```bash
# Remove all waters and ligands
python ../prepare_protein.py -i 1iep_full.pdb -o 1iep_protein_only.pdb

# Or keep specific cofactors (e.g., metal ions)
python ../prepare_protein.py -i 1iep_full.pdb -o 1iep_protein_only.pdb --keep ZN MG

# Interactive mode to preview what will be removed
python ../prepare_protein.py -i 1iep_full.pdb -o 1iep_protein_only.pdb --interactive
```

The script will:
- Remove all water molecules (HOH, WAT, etc.)
- Remove ligands and other heteroatoms
- Keep only protein atoms (ATOM records)
- Optionally keep specified cofactors or ions

---

## 3. (Optional) Extract Ligand Center Coordinates

If you have a PDB or CIF file with ligands and need to determine the docking box center coordinates, use the `extract_ligand_center.py` script:

```bash
# Interactive mode - lists ligands and prompts for selection and box size
python ../extract_ligand_center.py -i 1iep_full.pdb

# Or directly select a specific ligand with default 20 Å box
python ../extract_ligand_center.py -i 1iep_full.pdb -s 5

# Specify a custom box size
python ../extract_ligand_center.py -i 1iep_full.pdb -s 5 --box-size "25"

# Or use different dimensions for each axis
python ../extract_ligand_center.py -i 1iep_full.pdb -s 5 --box-size "25 30 20"
```

The script will:
- Identify all ligands in the structure (excluding water molecules)
- Let you interactively select a ligand (or use `-s` to select directly)
- Prompt for a custom box size or use default 20 Å
- Calculate the geometric center of the selected ligand
- Provide box size and center coordinates for docking

You can then use these coordinates in the next step with `mk_prepare_receptor.py`.

---

## 4. Prepare the Receptor File

Use the `mk_prepare_receptor.py` script to prepare the receptor. This includes adding hydrogens, assigning charges, and generating a box definition file.

```bash
mk_prepare_receptor.py \
  -i 1iep_receptorH.pdb \
  -o 1iep_receptor \
  -p -v \
  --box_size 20 20 20 \
  --box_center 15.190 53.903 16.917
```

- `-i`: input PDB file with hydrogens
- `-o`: base name for output files (`.pdbqt` and `.box.txt`)
- `-p`: add Gasteiger charges
- `-v`: verbose output
- `--box_size`: dimensions of the docking box (Å)
- `--box_center`: coordinates of the box center (Å)

This will produce:

- `1iep_receptor.pdbqt`
- `1iep_receptor.box.txt`

---

## 5. Prepare the Ligand File

Convert your ligand from SDF to PDBQT format:

```bash
mk_prepare_ligand.py \
  -i 1iep_ligand.sdf \
  -o 1iep_ligand.pdbqt
```

- `-i`: input ligand file in SDF format
- `-o`: output PDBQT filename

---

## 6. Run Molecular Docking with AutoDock Vina

Execute Vina using the prepared receptor and ligand, specifying the configuration file and desired exhaustiveness:

```bash
vina \
  --receptor 1iep_receptor.pdbqt \
  --ligand 1iep_ligand.pdbqt \
  --config 1iep_receptor.box.txt \
  --exhaustiveness=32 \
  --out 1iep_ligand_vina_out.pdbqt
```

- `--receptor`: receptor PDBQT file
- `--ligand`: ligand PDBQT file
- `--config`: box definition file
- `--exhaustiveness`: search thoroughness (higher = slower, more thorough)
- `--out`: output filename for docked poses

---

## 7. Extract Individual PDB Models

Once docking completes, use the provided script to split the multi‐model `.pdbqt` output into separate `.pdb` files:

```bash
# Make sure the script is executable (if not already):
chmod +x ../pdbqt2pdb.sh

# Run the script on the Vina output:
../pdbqt2pdb.sh 1iep_ligand_vina_out.pdbqt
```

This will:

1. Split each `MODEL` into `1iep_ligand_vina_out_modelN.pdbqt` files
2. Convert each to `1iep_ligand_vina_out_modelN.pdb`
3. Clean up intermediate `.pdbqt` files

You’ll find a set of `*.pdb` files, one per docked pose, ready for visualization or further analysis.

---

## 8. Visualize Docked Poses with PyMOL

1. Launch PyMOL from your terminal:

    ```bash
    pymol
    ```

2. In the PyMOL window, go to **File > Open...** and select the receptor file `1iep_receptorH.pdb`.

3. Again, go to **File > Open...** and select each docked model PDB file (e.g., `1iep_ligand_vina_out_model1.pdb`, `1iep_ligand_vina_out_model2.pdb`, etc.). These will load into the session, and you can toggle their visibility to compare poses.

---

Congratulations! You’ve successfully run a basic molecular docking workflow using AutoDock Vina. Feel free to explore different box sizes, exhaustiveness levels, or other receptor/ligand pairs.

---

## What's Next?

### Future Enhancements

We're continuously improving this workshop! Upcoming features include:

- **Automated Protein Preparation**: One-command hydrogen addition, charge assignment, and structure cleaning
- **Ligand Preparation from SMILES**: Convert SMILES strings directly to docking-ready ligands
- **Binding Site Detection**: Automatic identification of potential binding pockets
- **Batch Processing**: Process multiple ligands or structures at once

See [FUTURE_FEATURES.md](FUTURE_FEATURES.md) for the complete roadmap and detailed plans.

**Have suggestions?** We welcome your feedback! Open an issue on the repository to share your ideas.


---

## Troubleshooting

### Histidine Protonation Errors

If you encounter an error like this when running `mk_prepare_receptor.py`:

```
RuntimeError: for residue_key='A:246', 3 have passed: ['HIE', 'HID', 'HIP'] 
and tied for fewest missing and excess H: HIE HID
```

**Solution 1: Use reduce with FLIP optimization**
```bash
reduce -FLIP protein_clean.pdb > protein_clean_H.pdb
```

**Solution 2: Specify histidine protonation manually**
```bash
mk_prepare_receptor.py -i protein_H.pdb -o receptor \
  -n A:246=HIE \
  --box_size 20 20 20 \
  --box_center 15.614 53.380 15.455
```

Choose the appropriate histidine tautomer:
- **HIE**: Hydrogen on epsilon nitrogen (most common)
- **HID**: Hydrogen on delta nitrogen
- **HIP**: Protonated on both nitrogens (charged, at low pH)

**Solution 3: Use the provided prepared file**

The tutorial includes `1iep_receptorH.pdb` which is already prepared correctly.

### Other Common Issues

**"Command not found" errors:**
- Ensure the conda environment is activated: `conda activate molecular_docking_workshop`
- Verify the script is executable: `chmod +x script_name.py`

**"No ligands found":**
- Make sure you're using the original PDB file (with ligands), not the cleaned protein file
- Check that the file contains HETATM records: `grep "^HETATM" file.pdb`

**Box size too small/large:**
- Use `extract_ligand_center.py` to get appropriate box dimensions
- Default 20 Å is suitable for most ligands
- Adjust based on ligand size and desired flexibility
