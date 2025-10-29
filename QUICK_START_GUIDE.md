# Quick Start Guide: Ligand Center Extractor

## 🚀 Fastest Way to Get Started

### Step 1: Run the Tool
```bash
python extract_ligand_center.py -i your_protein.pdb
```

### Step 2: Pick Your Ligand
The tool will show you all ligands found:
```
Found 8 ligand(s):

#    Ligand ID            Atoms    Center (x, y, z)               Box Size (x, y, z)
----------------------------------------------------------------------------------------------------
1    CL_A_1               1        ( 14.21,  35.38,   1.66)   ( 0.00,  0.00,  0.00)
5    STI_A_201            37       ( 15.61,  53.38,  15.45)   ( 8.66, 16.74, 13.53)
...

Enter ligand number to get docking box parameters (or 'q' to quit): 5

Enter custom box size in Å (e.g., 25 or 20 20 20), or press Enter for default (20 20 20): 
```

1. Type the number of the ligand you want (e.g., `5`) and press Enter
2. Enter a custom box size (e.g., `25`) or press Enter for default 20 Å

### Step 3: Copy the Command
The tool gives you a ready-to-use command:
```bash
mk_prepare_receptor.py \
  -i your_receptor.pdb \
  -o receptor_prepared \
  -p -v \
  --box_size 20.0 20.0 20.0 \
  --box_center 15.614 53.380 15.455
```

Just copy and paste it!

---

## 💡 Tips

### Want to skip the prompt?
```bash
# If you already know it's ligand #5 with default 20 Å box
python extract_ligand_center.py -i protein.pdb -s 5

# Or with a custom box size
python extract_ligand_center.py -i protein.pdb -s 5 --box-size "25"
```

### Need a bigger/smaller box?
```bash
# Use a uniform box size (e.g., 30 Å in all dimensions)
python extract_ligand_center.py -i protein.pdb -s 5 --box-size "30"

# Or specify different dimensions for each axis
python extract_ligand_center.py -i protein.pdb -s 5 --box-size "25 30 20"
```

### Only one ligand in your structure?
```bash
# Auto-select it
python extract_ligand_center.py -i protein.pdb -a
```

---

## 📋 Common Scenarios

### Scenario 1: Re-docking (Reproducing Known Pose)
You have a crystal structure with a ligand and want to reproduce the binding pose.

```bash
# Use the original PDB file (with ligand)
python extract_ligand_center.py -i 1iep.pdb

# Select the ligand when prompted
# Use smaller box for focused search (e.g., 15-20 Å)
python extract_ligand_center.py -i 1iep.pdb -s 1 --box-size "18"
```

### Scenario 2: Virtual Screening
You know the binding site and want to dock many ligands.

```bash
# Determine box parameters once
python extract_ligand_center.py -i reference_complex.pdb -s 1

# Use the same parameters for all ligands in your library
```

### Scenario 3: Exploring Multiple Binding Sites
Your protein has multiple ligands in different sites.

```bash
# Interactive mode lets you explore each one
python extract_ligand_center.py -i protein.pdb

# Try ligand 1, then run again and try ligand 2, etc.
```

---

## ⚠️ Important Notes

1. **Use the original PDB file** - The one with ligands intact, not the prepared receptor
2. **Water is excluded** - HOH, WAT, etc. are automatically filtered out
3. **Check the ligand** - Make sure you're selecting the right one (check chain and residue number)
4. **Padding matters** - Larger padding = more flexibility, but slower docking

---

## 🔍 What the Numbers Mean

### Center Coordinates (x, y, z)
- The geometric center of your ligand
- This is where the docking box will be centered

### Box Size
- Dimensions of the search space in Ångströms
- Default: 20 Å in all dimensions (good for most cases)
- Typical range: 15-30 Å per dimension
- Smaller (15-18 Å): Focused search, faster, good for re-docking
- Larger (25-30 Å): More flexibility, slower, good for virtual screening

---

## 🆘 Troubleshooting

**"No ligands found"**
- Check if you're using the right file (should have HETATM records)
- Make sure it's not a prepared receptor (ligands removed)

**"Invalid selection"**
- Enter a number from the list (1-8 in the example)
- Or type 'q' to quit

**"File not found"**
- Check the file path
- Make sure you're in the right directory

---

## 📚 Next Steps

After getting your box parameters:

1. **Prepare the receptor**
   ```bash
   mk_prepare_receptor.py -i receptor.pdb -o receptor_prepared -p -v \
     --box_size [from tool] --box_center [from tool]
   ```

2. **Prepare the ligand**
   ```bash
   mk_prepare_ligand.py -i ligand.sdf -o ligand.pdbqt
   ```

3. **Run docking**
   ```bash
   vina --receptor receptor_prepared.pdbqt \
        --ligand ligand.pdbqt \
        --config receptor_prepared.box.txt \
        --exhaustiveness=32 \
        --out docked.pdbqt
   ```

See [TUTORIAL.md](TUTORIAL.md) for the complete workflow!


---

## 🚀 Coming Soon: Future Features

We're working on making molecular docking even easier! Planned features include:

### Automated Preparation Tools
- **Protein Prep**: One command to add hydrogens, assign charges, and clean structures
- **Ligand Prep**: Convert SMILES to 3D structures with proper protonation
- **Integrated Workflow**: From raw files to docking-ready in seconds

### Smart Analysis
- **Binding Site Detection**: Automatically find potential binding pockets
- **Flexible Residues**: Suggest which residues to make flexible
- **Batch Processing**: Screen hundreds of ligands at once

### Enhanced Visualization
- **PyMOL Integration**: Automatic visualization of results
- **Interaction Analysis**: Identify key protein-ligand interactions
- **Pose Comparison**: Compare multiple docking results

**Want to help shape these features?** Check out [FUTURE_FEATURES.md](FUTURE_FEATURES.md) for the full roadmap and share your feedback!
