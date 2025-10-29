# Complete Molecular Docking Workflow Example

This document demonstrates a complete molecular docking workflow using the 1IEP structure (HIV-1 protease with STI-571 inhibitor).

## Step-by-Step Example

### 1. Download the Structure from PDB

```bash
cd input_files
curl -O "https://files.rcsb.org/download/1IEP.pdb"
```

### 2. Identify Ligands and Get Docking Box Parameters

```bash
# Interactive mode - lists ligands and prompts for selection
python ../extract_ligand_center.py -i 1IEP.pdb

# Output shows:
# Found 8 ligand(s):
# 
# #    Ligand ID            Atoms    Center (x, y, z)               Box Size (x, y, z)
# -------------------------------------------------------------------------------------
# 1    CL_A_1               1        ( 14.21,  35.38,   1.66)   ( 0.00,  0.00,  0.00)
# 2    CL_A_2               1        ( 18.09,  42.38,  23.84)   ( 0.00,  0.00,  0.00)
# 3    CL_A_4               1        (  3.75,  59.16,   9.29)   ( 0.00,  0.00,  0.00)
# 4    CL_A_5               1        ( 12.29,  64.72,  15.10)   ( 0.00,  0.00,  0.00)
# 5    STI_A_201            37       ( 15.61,  53.38,  15.45)   ( 8.66, 16.74, 13.53)
# 6    CL_B_3               1        ( 10.21,  87.55,  69.26)   ( 0.00,  0.00,  0.00)
# 7    CL_B_6               1        ( 16.09,  98.00,  48.28)   ( 0.00,  0.00,  0.00)
# 8    STI_B_202            37       ( 12.55,  96.87,  59.27)   ( 8.37, 14.48, 15.96)
#
# Enter ligand number to get docking box parameters (or 'q' to quit): 5

# Or directly select the STI ligand in chain A (ligand #5)
python ../extract_ligand_center.py -i 1IEP.pdb -s 5

# Output provides:
# ================================================================================
# Selected Ligand: STI_A_201
# ================================================================================
# Number of atoms: 37
# Residue name: STI
# Chain: A
# Residue number: 201
# 
# Geometric center:
#   X: 15.614
#   Y: 53.380
#   Z: 15.455
# 
# Suggested docking box (with 8.0 Å padding):
#   Size: (24.664, 32.739, 29.526)
# 
# ================================================================================
# Use these parameters with mk_prepare_receptor.py:
# ================================================================================
# 
# mk_prepare_receptor.py \
#   -i your_receptor.pdb \
#   -o receptor_prepared \
#   -p -v \
#   --box_size 24.7 32.7 29.5 \
#   --box_center 15.614 53.380 15.455
```

### 3. Prepare the Receptor

First, add hydrogens to the receptor (if not already present):

```bash
# Using reduce (if available)
reduce 1IEP.pdb > 1IEP_H.pdb

# Or download a version with hydrogens already added
# (The 1iep_receptorH.pdb in this workshop already has hydrogens)
```

Then prepare the receptor with the calculated box parameters:

```bash
mk_prepare_receptor.py \
  -i 1iep_receptorH.pdb \
  -o 1iep_receptor \
  -p -v \
  --box_size 24.7 32.7 29.5 \
  --box_center 15.614 53.380 15.455
```

This creates:
- `1iep_receptor.pdbqt` - Receptor in PDBQT format
- `1iep_receptor.box.txt` - Box configuration for Vina

### 4. Prepare the Ligand

```bash
mk_prepare_ligand.py \
  -i 1iep_ligand.sdf \
  -o 1iep_ligand.pdbqt
```

### 5. Run Molecular Docking

```bash
vina \
  --receptor 1iep_receptor.pdbqt \
  --ligand 1iep_ligand.pdbqt \
  --config 1iep_receptor.box.txt \
  --exhaustiveness=32 \
  --out 1iep_ligand_vina_out.pdbqt
```

### 6. Convert Results to PDB Format

```bash
../pdbqt2pdb.sh 1iep_ligand_vina_out.pdbqt
```

This creates individual PDB files for each docked pose:
- `1iep_ligand_vina_out_model1.pdb`
- `1iep_ligand_vina_out_model2.pdb`
- etc.

### 7. Visualize Results

```bash
pymol 1iep_receptorH.pdb 1iep_ligand_vina_out_model*.pdb
```

## Tips for Different Scenarios

### Re-docking (Reproducing Known Binding Pose)

When you want to reproduce a known binding pose:

1. Use the original PDB structure with the ligand
2. Extract the ligand's center coordinates using `extract_ligand_center.py`
3. Use a smaller box (5-8 Å padding) centered on the ligand
4. Compare your docked poses with the crystal structure

### Blind Docking (Unknown Binding Site)

When the binding site is unknown:

1. Use a larger box that covers potential binding regions
2. Increase exhaustiveness (e.g., 64 or higher)
3. Consider multiple docking runs with different box positions
4. Analyze results for clustering of poses

### Virtual Screening (Multiple Ligands)

When screening a library of compounds:

1. Determine the binding site once using a known ligand or site prediction
2. Use the same box parameters for all ligands
3. Prepare all ligands in batch
4. Run docking for each ligand
5. Rank results by binding affinity

## Understanding the Output

Vina output shows binding affinities (kcal/mol) for each pose:

```
mode |   affinity | dist from best mode
     | (kcal/mol) | rmsd l.b.| rmsd u.b.
-----+------------+----------+----------
   1       -11.2      0.000      0.000
   2       -10.8      1.234      2.456
   3       -10.5      2.345      3.567
```

- **Lower (more negative) values** indicate stronger predicted binding
- **RMSD** shows how different each pose is from the best pose
- Typically, poses within 2 Å RMSD are considered similar

## Common Issues and Solutions

### Issue: No ligands found

**Solution**: Make sure you're using the original PDB file from the database, not a prepared receptor file that has ligands removed.

### Issue: Box too small

**Solution**: Increase the padding parameter:
```bash
python extract_ligand_center.py -i protein.pdb -s 1 --padding 10.0
```

### Issue: Docking takes too long

**Solution**: 
- Reduce exhaustiveness (try 16 or 8)
- Make the box smaller if appropriate
- Use fewer CPU cores with `--cpu` flag

### Issue: Poor docking results

**Solution**:
- Verify receptor preparation (hydrogens, charges)
- Check ligand protonation state
- Ensure box covers the binding site adequately
- Try increasing exhaustiveness
- Consider flexible residues if needed

## References

- AutoDock Vina: http://vina.scripps.edu/
- Meeko: https://github.com/forlilab/Meeko
- PDB: https://www.rcsb.org/
