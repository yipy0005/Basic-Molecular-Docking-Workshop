# Changelog - Ligand Center Extractor Tool

## New Feature: Ligand Center Coordinate Extraction

### Summary

Added a Python CLI tool (`extract_ligand_center.py`) that automates the process of identifying ligands in PDB/CIF files and calculating appropriate docking box parameters for AutoDock Vina.

### What Was Added

1. **Main Script**: `extract_ligand_center.py`
   - Parses PDB and mmCIF file formats
   - Identifies all ligands (HETATM records) in a structure
   - Automatically excludes water molecules
   - Calculates geometric center coordinates
   - Suggests docking box sizes with customizable padding
   - Provides ready-to-use commands for `mk_prepare_receptor.py`

2. **Documentation**:
   - `LIGAND_EXTRACTOR_README.md` - Detailed usage guide
   - `EXAMPLE_WORKFLOW.md` - Complete end-to-end workflow example
   - Updated `TUTORIAL.md` - Added section on ligand extraction (Step 2)
   - Updated `README.md` - Added quick reference to the new tool

3. **Test Files**:
   - `input_files/1iep_full.pdb` - Full PDB structure with ligands for testing
   - `input_files/1iep_full.cif` - mmCIF version for format testing

### Features

- ✅ **Multi-format support**: Works with both PDB and mmCIF files
- ✅ **Automatic ligand detection**: Finds all HETATM records
- ✅ **Water exclusion**: Automatically filters out water molecules
- ✅ **Interactive selection**: List all ligands and select one
- ✅ **Auto-select mode**: Automatically selects if only one ligand exists
- ✅ **Customizable padding**: Adjust box size padding (default 8.0 Å)
- ✅ **Detailed output**: Shows center, bounding box, and suggested parameters
- ✅ **Error handling**: Validates input files and selections
- ✅ **Ready-to-use commands**: Generates exact command for next step

### Usage Examples

```bash
# List all ligands
python extract_ligand_center.py -i protein.pdb

# Select a specific ligand
python extract_ligand_center.py -i protein.pdb -s 1

# Auto-select (single ligand)
python extract_ligand_center.py -i protein.pdb -a

# Custom padding
python extract_ligand_center.py -i protein.pdb -s 1 --padding 5.0
```

### Integration with Existing Workflow

The tool fits seamlessly into the existing molecular docking workflow:

**Before** (manual process):
1. Open PDB file in visualization software
2. Manually identify ligand
3. Manually calculate center coordinates
4. Estimate appropriate box size
5. Prepare receptor with guessed parameters

**After** (automated):
1. Run `extract_ligand_center.py` to identify ligands
2. Select ligand of interest
3. Copy provided command with exact parameters
4. Prepare receptor with calculated parameters

### Benefits

1. **Saves time**: Eliminates manual coordinate calculation
2. **Reduces errors**: Automated calculation is more accurate
3. **Improves reproducibility**: Consistent methodology
4. **Beginner-friendly**: Clear output and instructions
5. **Flexible**: Works with various file formats and scenarios

### Testing

The tool has been tested with:
- ✅ PDB format files (1IEP structure)
- ✅ mmCIF format files (1IEP structure)
- ✅ Multiple ligands in one structure
- ✅ Single ligand structures
- ✅ Structures with no ligands
- ✅ Invalid file paths
- ✅ Invalid selections
- ✅ Various padding values

### Future Enhancements (Potential)

- Export ligand coordinates to SDF format
- Support for flexible residue identification
- Batch processing of multiple structures
- Integration with PyMOL for visualization
- Support for protein-protein docking interfaces

### Files Modified

- `TUTORIAL.md` - Added Step 2 for ligand extraction
- `README.md` - Added section 8 and updated table of contents

### Files Created

- `extract_ligand_center.py` - Main script
- `LIGAND_EXTRACTOR_README.md` - Detailed documentation
- `EXAMPLE_WORKFLOW.md` - Complete workflow example
- `CHANGELOG_LIGAND_EXTRACTOR.md` - This file
- `input_files/1iep_full.pdb` - Test file with ligands
- `input_files/1iep_full.cif` - Test file in CIF format

### Dependencies

No new dependencies required. Uses only standard Python libraries:
- `argparse` - Command-line interface
- `pathlib` - File path handling
- `collections` - Data structures
- `numpy` - Coordinate calculations
- `sys` - System operations

### Compatibility

- Python 3.6+
- Works on Windows, macOS, and Linux
- Compatible with existing workshop environment

---

**Date Added**: 2025-10-29
**Version**: 1.0.0
**Status**: Production Ready
