# Ligand Center Extractor

A Python CLI tool to identify ligands in PDB/CIF files and calculate center coordinates for molecular docking.

## Purpose

When preparing for molecular docking with AutoDock Vina, you need to specify:
1. The center coordinates of the docking box
2. The size of the docking box

This tool automates the process of finding ligands in a protein structure and calculating appropriate docking box parameters.

## Features

- ✅ Supports both PDB and mmCIF file formats
- ✅ Automatically identifies all ligands (HETATM records)
- ✅ Excludes water molecules automatically
- ✅ Calculates geometric center of ligands
- ✅ Suggests docking box sizes with customizable padding
- ✅ Provides ready-to-use command for `mk_prepare_receptor.py`

## Installation

No additional dependencies required beyond standard Python libraries:
- numpy (usually included with scientific Python distributions)

```bash
# Make the script executable
chmod +x extract_ligand_center.py
```

## Usage

### Interactive Mode (Recommended)

```bash
python extract_ligand_center.py -i protein.pdb
```

This will:
1. Display all ligands found in the structure with their details
2. Prompt you to enter a ligand number
3. Ask for a custom box size (or press Enter for default 20 Å)
4. Show detailed docking box parameters for your selection

Simply enter the number of the ligand you want to analyze, or 'q' to quit.

**Example interaction:**
```
Found 8 ligand(s):

#    Ligand ID            Atoms    Center (x, y, z)               Box Size (x, y, z)
----------------------------------------------------------------------------------------------------
1    CL_A_1               1        ( 14.21,  35.38,   1.66)   ( 0.00,  0.00,  0.00)
5    STI_A_201            37       ( 15.61,  53.38,  15.45)   ( 8.66, 16.74, 13.53)
...

Enter ligand number to get docking box parameters (or 'q' to quit): 5

Enter custom box size in Å (e.g., 25 or 20 20 20), or press Enter for default (20 20 20): 25
```

### Direct Selection

```bash
# With default 20 Å box
python extract_ligand_center.py -i protein.pdb -s 1

# With custom box size
python extract_ligand_center.py -i protein.pdb -s 1 --box-size "25"

# With different dimensions
python extract_ligand_center.py -i protein.pdb -s 1 --box-size "25 30 20"
```

Skip the interactive prompt and directly show detailed information for ligand #1, including:
- Geometric center coordinates
- Ligand bounding box
- Docking box size (default 20 Å or custom)
- Ready-to-use `mk_prepare_receptor.py` command

### Auto-Select (Single Ligand)

```bash
# With default box size
python extract_ligand_center.py -i protein.pdb -a

# With custom box size
python extract_ligand_center.py -i protein.pdb -a --box-size "30"
```

If the structure contains only one ligand, this will automatically select it.

## Example Output

```
Parsing 1iep_full.pdb...

Found 8 ligand(s):

#    Ligand ID            Atoms    Center (x, y, z)               Box Size (x, y, z)
----------------------------------------------------------------------------------------------------
1    CL_A_1               1        ( 14.21,  35.38,   1.66)   ( 0.00,  0.00,  0.00)
2    CL_A_2               1        ( 18.09,  42.38,  23.84)   ( 0.00,  0.00,  0.00)
5    STI_A_201            37       ( 15.61,  53.38,  15.45)   ( 8.66, 16.74, 13.53)
...

Enter ligand number to get docking box parameters (or 'q' to quit): 5

Enter custom box size in Å (e.g., 25 or 20 20 20), or press Enter for default (20 20 20): 

================================================================================
Selected Ligand: STI_A_201
================================================================================
Number of atoms: 37
Residue name: STI
Chain: A
Residue number: 201

Geometric center:
  X: 15.614
  Y: 53.380
  Z: 15.455

Docking box (default size: 20 Å):
  Size: (20.000, 20.000, 20.000)

================================================================================
Use these parameters with mk_prepare_receptor.py:
================================================================================

mk_prepare_receptor.py \
  -i your_receptor.pdb \
  -o receptor_prepared \
  -p -v \
  --box_size 20.0 20.0 20.0 \
  --box_center 15.614 53.380 15.455
```

## Command-Line Options

| Option | Description |
|--------|-------------|
| `-i, --input` | Input PDB or CIF file (required) |
| `-s, --select` | Select ligand by number directly (skips interactive prompt) |
| `-a, --auto` | Automatically select if only one ligand exists |
| `--box-size` | Custom box size in Å (e.g., "25" or "20 20 20"). Default: 20 20 20 |
| `-o, --output` | Output file to save ligand coordinates (future feature) |

**Notes**: 
- If you don't specify `-s` or `-a`, the tool will run in interactive mode and prompt you to select a ligand
- In interactive mode, you'll also be prompted for a custom box size (or press Enter for default 20 Å)
- Use `--box-size` to specify box size via command line when using `-s` or `-a` flags

## Workflow Integration

This tool fits into the molecular docking workflow as follows:

1. **Extract ligand coordinates** (this tool)
   ```bash
   python extract_ligand_center.py -i protein.pdb -s 1
   ```

2. **Prepare receptor** with the calculated coordinates
   ```bash
   mk_prepare_receptor.py \
     -i protein.pdb \
     -o receptor_prepared \
     -p -v \
     --box_size 24.7 32.7 29.5 \
     --box_center 15.614 53.380 15.455
   ```

3. **Prepare ligand**
   ```bash
   mk_prepare_ligand.py -i ligand.sdf -o ligand.pdbqt
   ```

4. **Run docking**
   ```bash
   vina --receptor receptor_prepared.pdbqt \
        --ligand ligand.pdbqt \
        --config receptor_prepared.box.txt \
        --exhaustiveness=32 \
        --out docked.pdbqt
   ```

## Notes

- Water molecules (HOH, WAT, H2O, TIP, TIP3, SOL) are automatically excluded
- The geometric center is calculated as the mean of all atom coordinates
- Suggested box sizes include padding on all sides to allow ligand flexibility
- For re-docking studies, use the original ligand's coordinates
- For blind docking, you may need to manually adjust the box to cover the entire binding site
- **Important**: Use the original PDB file from the PDB database (with ligands intact), not the prepared receptor file which has ligands removed

## Troubleshooting

**No ligands found:**
- Check if your PDB file contains HETATM records
- Ensure the file is properly formatted
- Water molecules are excluded by default

**Coordinates don't match expected values:**
- Different structures may have different coordinate systems
- Verify you're using the correct chain and residue number
- Check if the structure has been transformed or aligned

## Future Features

### Planned Enhancements

The following features are planned for future releases to create a comprehensive docking preparation toolkit:

#### 1. Automated Protein Structure Preparation
- **Hydrogen Addition**: Automatically add hydrogens to protein structures
- **Charge Assignment**: Add Gasteiger charges for docking
- **Structure Cleaning**: Remove water molecules, fix missing atoms
- **Chain Selection**: Select specific chains for multi-chain proteins
- **Missing Residue Handling**: Detect and handle missing residues
- **Integration**: Direct preparation without external tools

#### 2. Automated Ligand Structure Preparation
- **Format Conversion**: Convert between SDF, MOL2, PDB, SMILES formats
- **3D Structure Generation**: Generate 3D coordinates from SMILES strings
- **Protonation States**: Predict and assign correct protonation at pH 7.4
- **Tautomer Generation**: Generate relevant tautomeric forms
- **Conformer Generation**: Create multiple starting conformations
- **Charge Calculation**: Automatic partial charge assignment

#### 3. Additional Workflow Enhancements
- **Export Ligand Coordinates**: Save extracted ligands to SDF/MOL2 format
- **Flexible Residue Identification**: Suggest flexible residues near binding site
- **Batch Processing**: Process multiple structures in one command
- **PyMOL Integration**: Visualize binding sites and boxes directly
- **Protein-Protein Docking**: Support for protein-protein interface preparation
- **Binding Site Detection**: Automatic cavity/pocket detection
- **Water Placement**: Identify conserved water molecules in binding site

### Why These Features?

**Current Workflow** (requires multiple tools):
1. Download structures from PDB
2. Add hydrogens using external tools (reduce, OpenBabel)
3. Prepare ligands using separate scripts (mk_prepare_ligand.py)
4. Convert between file formats manually
5. Identify binding sites visually

**Future Vision** (one integrated tool):
1. Input: Raw PDB file or SMILES string
2. Output: Docking-ready receptor and ligand files with optimal parameters
3. All preparation steps automated and validated

### Benefits of Integrated Preparation

- ✅ **Simplified Workflow**: One tool instead of many
- ✅ **Reduced Errors**: Automated validation and error checking
- ✅ **Reproducibility**: Consistent preparation methodology
- ✅ **Beginner-Friendly**: Less expertise required
- ✅ **Time-Saving**: Batch processing and automation
- ✅ **Best Practices**: Built-in validation and recommendations

### Timeline & Feedback

These features are under active consideration and will be implemented based on:
- User feedback and feature requests
- Community needs and priorities
- Available development resources

**Have suggestions?** We welcome feedback! If you have specific requirements or ideas for these features, please:
- Open an issue on the repository
- Share your use cases and workflows
- Contribute to the discussion

## License

This tool is part of the Basic Molecular Docking Workshop and follows the same license.
