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

## 2. Prepare the Receptor File

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

## 3. Prepare the Ligand File

Convert your ligand from SDF to PDBQT format:

```bash
mk_prepare_ligand.py \
  -i 1iep_ligand.sdf \
  -o 1iep_ligand.pdbqt
```

- `-i`: input ligand file in SDF format
- `-o`: output PDBQT filename

---

## 4. Run Molecular Docking with AutoDock Vina

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

## 5. Extract Individual PDB Models

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

## 6. Visualize Docked Poses with PyMOL

1. Launch PyMOL from your terminal:

    ```bash
    pymol
    ```

2. In the PyMOL window, go to **File > Open...** and select the receptor file `1iep_receptorH.pdb`.

3. Again, go to **File > Open...** and select each docked model PDB file (e.g., `1iep_ligand_vina_out_model1.pdb`, `1iep_ligand_vina_out_model2.pdb`, etc.). These will load into the session, and you can toggle their visibility to compare poses.

---

Congratulations! You’ve successfully run a basic molecular docking workflow using AutoDock Vina. Feel free to explore different box sizes, exhaustiveness levels, or other receptor/ligand pairs.
