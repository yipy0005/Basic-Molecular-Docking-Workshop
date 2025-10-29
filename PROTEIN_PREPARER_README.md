# Protein Structure Preparer

A Python CLI tool to prepare protein structures for molecular docking by removing water molecules and ligands.

## Purpose

Before molecular docking, protein structures often need to be cleaned:
- Remove water molecules (HOH, WAT, etc.)
- Remove ligands and other heteroatoms
- Keep only protein atoms (ATOM records)
- Optionally keep specific cofactors or ions

This tool automates the cleaning process for both PDB and mmCIF files.

## Features

- ✅ Supports both PDB and mmCIF file formats
- ✅ Removes all water molecules automatically
- ✅ Removes ligands and heteroatoms
- ✅ Option to keep specific heteroatoms (cofactors, ions)
- ✅ Interactive mode with preview and confirmation
- ✅ Detailed summary of what was removed
- ✅ Preserves header and structural information

## Installation

No additional dependencies required beyond standard Python libraries.

```bash
# Make the script executable
chmod +x prepare_protein.py
```

## Usage

### Basic Usage - Remove All Waters and Ligands

```bash
python prepare_protein.py -i protein.pdb -o protein_clean.pdb
```

This will:
1. Read the input PDB file
2. Keep only ATOM records (protein)
3. Remove all HETATM records (waters, ligands, ions)
4. Write cleaned protein to output file
5. Show summary of what was removed

### Keep Specific Heteroatoms

```bash
# Keep heme group and NAD cofactor
python prepare_protein.py -i protein.pdb -o protein_clean.pdb --keep HEM NAD

# Keep multiple ions
python prepare_protein.py -i protein.pdb -o protein_clean.pdb --keep ZN MG CA
```

Use `--keep` to preserve specific heteroatoms like:
- Cofactors: HEM (heme), NAD, FAD, FMN, ATP, ADP
- Metal ions: ZN, MG, CA, FE, CU, MN
- Other important groups specific to your protein

### Interactive Mode

```bash
python prepare_protein.py -i protein.pdb -o protein_clean.pdb --interactive
```

Interactive mode will:
1. Process the file
2. Show a preview of what will be removed
3. Ask for confirmation before writing output
4. Allow you to cancel if needed

### Quiet Mode

```bash
python prepare_protein.py -i protein.pdb -o protein_clean.pdb --quiet
```

Suppresses all output messages (useful for scripting).

### Process CIF Files

```bash
python prepare_protein.py -i protein.cif -o protein_clean.cif
```

Works the same way with mmCIF files.

## Example Output

```
Processing input_files/1iep_full.pdb...

================================================================================
Protein Preparation Summary
================================================================================
Input file: input_files/1iep_full.pdb
Format: PDB

Protein atoms: 4458

Removed water molecules: 172

Removed ligands:
  CL: 6 atoms
  STI: 74 atoms
================================================================================

Output written to: input_files/1iep_protein_only.pdb

Next steps:
1. Add hydrogens (if needed):
   reduce input_files/1iep_protein_only.pdb > 1iep_protein_only_H.pdb
2. Prepare for docking:
   mk_prepare_receptor.py -i 1iep_protein_only_H.pdb -o receptor_prepared
```

## Command-Line Options

| Option | Description |
|--------|-------------|
| `-i, --input` | Input PDB or CIF file (required) |
| `-o, --output` | Output file for cleaned protein (required) |
| `--keep` | Heteroatom residue names to keep (e.g., HEM NAD FAD) |
| `--interactive` | Show preview and ask for confirmation |
| `--quiet` | Suppress output messages |

## Workflow Integration

This tool fits into the molecular docking workflow:

### Complete Workflow

```bash
# Step 1: Clean protein structure
python prepare_protein.py -i protein.pdb -o protein_clean.pdb

# Step 2: Add hydrogens (if needed)
reduce protein_clean.pdb > protein_clean_H.pdb

# Step 3: Extract ligand center coordinates
python extract_ligand_center.py -i protein.pdb -s 1

# Step 4: Prepare receptor for docking
mk_prepare_receptor.py \
  -i protein_clean_H.pdb \
  -o receptor_prepared \
  -p -v \
  --box_size 20 20 20 \
  --box_center 15.6 53.4 15.5

# Step 5: Prepare ligand
mk_prepare_ligand.py -i ligand.sdf -o ligand.pdbqt

# Step 6: Run docking
vina --receptor receptor_prepared.pdbqt \
     --ligand ligand.pdbqt \
     --config receptor_prepared.box.txt \
     --exhaustiveness=32 \
     --out docked.pdbqt
```

## What Gets Removed

### Always Removed
- Water molecules: HOH, WAT, H2O, TIP, TIP3, SOL
- All HETATM records (unless specified with --keep)

### What Gets Kept
- All ATOM records (protein backbone and sidechains)
- Header information (HEADER, TITLE, REMARK, etc.)
- Structural information (CRYST1, MODEL, TER, END)
- Specified heteroatoms (with --keep option)

## Common Use Cases

### Case 1: Standard Protein Cleaning

```bash
# Remove everything except protein
python prepare_protein.py -i 1abc.pdb -o 1abc_clean.pdb
```

**Use when**: You have a simple protein-ligand complex and want just the protein.

### Case 2: Keep Metal Ions

```bash
# Keep zinc ions (important for metalloenzymes)
python prepare_protein.py -i 1abc.pdb -o 1abc_clean.pdb --keep ZN
```

**Use when**: Your protein has catalytic metal ions that are part of the active site.

### Case 3: Keep Cofactors

```bash
# Keep heme group in hemoglobin
python prepare_protein.py -i hemoglobin.pdb -o hemoglobin_clean.pdb --keep HEM
```

**Use when**: Your protein requires a cofactor for function.

### Case 4: Interactive Cleaning

```bash
# Preview what will be removed
python prepare_protein.py -i complex.pdb -o clean.pdb --interactive
```

**Use when**: You're not sure what heteroatoms are in the file and want to review before cleaning.

### Case 5: Batch Processing

```bash
# Process multiple files
for file in *.pdb; do
    python prepare_protein.py -i "$file" -o "clean_${file}" --quiet
done
```

**Use when**: You have many structures to clean.

## Tips & Best Practices

### 1. Check What's in Your File First

Use the ligand extractor to see what heteroatoms are present:
```bash
python extract_ligand_center.py -i protein.pdb
```

### 2. Keep Important Cofactors

Some proteins need cofactors to maintain their structure:
- Metalloproteins: Keep metal ions (ZN, MG, FE, etc.)
- Enzymes: Keep cofactors (NAD, FAD, ATP, etc.)
- Heme proteins: Keep HEM

### 3. Use Interactive Mode for Unknown Structures

If you're not familiar with the structure:
```bash
python prepare_protein.py -i protein.pdb -o clean.pdb --interactive
```

### 4. Verify Output

Always check the output file:
```bash
# Count protein atoms
grep -c "^ATOM" protein_clean.pdb

# Check for remaining HETATM
grep "^HETATM" protein_clean.pdb
```

### 5. Add Hydrogens After Cleaning

Most docking programs need hydrogens:
```bash
reduce protein_clean.pdb > protein_clean_H.pdb
```

## Troubleshooting

**No output file created:**
- Check input file exists
- Verify you have write permissions
- Check for error messages

**Too many atoms removed:**
- Use `--interactive` to see what's being removed
- Use `--keep` to preserve important heteroatoms
- Check if your protein has unusual residue names

**Output file is empty:**
- Verify input file has ATOM records
- Check file format is correct (PDB or CIF)
- Try with `--interactive` to see what's happening

**Kept heteroatoms not in output:**
- Check spelling of residue names (case-sensitive)
- Verify residue names match those in the file
- Use ligand extractor to see exact residue names

## Notes

- Water molecules are always removed (HOH, WAT, H2O, TIP, TIP3, SOL)
- Residue names are case-sensitive
- Output format matches input format (PDB → PDB, CIF → CIF)
- Header information is preserved
- Original file is never modified

## Integration with Other Tools

### With extract_ligand_center.py

```bash
# First, identify ligands in original structure
python extract_ligand_center.py -i protein_complex.pdb

# Then clean protein
python prepare_protein.py -i protein_complex.pdb -o protein_only.pdb

# Use coordinates from step 1 for docking preparation
```

### With mk_prepare_receptor.py

```bash
# Clean protein
python prepare_protein.py -i protein.pdb -o protein_clean.pdb

# Add hydrogens
reduce protein_clean.pdb > protein_clean_H.pdb

# Prepare for docking
mk_prepare_receptor.py -i protein_clean_H.pdb -o receptor_prepared -p -v \
  --box_size 20 20 20 --box_center 15.6 53.4 15.5
```

## Future Enhancements

Planned features (see [FUTURE_FEATURES.md](FUTURE_FEATURES.md)):
- Automatic hydrogen addition
- Charge assignment
- Missing residue detection
- Structure validation
- Chain selection
- Automatic cofactor detection

## License

This tool is part of the Basic Molecular Docking Workshop and follows the same license.
