# Box Size Update Summary

## Changes Made: Default 20 Å Box with Interactive Customization

### Overview

Updated the `extract_ligand_center.py` script to use a **default box size of 20 Å** (instead of calculating based on ligand size + padding) and added interactive prompts for custom box sizes.

---

## Key Changes

### 1. Default Box Size: 20 Å

**Before**: Box size was calculated as `ligand_dimensions + (2 × padding)`
- Default padding: 8.0 Å
- Result: Variable box sizes depending on ligand size

**After**: Fixed default box size of 20 Å in all dimensions
- Consistent across all ligands
- Standard size suitable for most docking scenarios
- Users can customize if needed

### 2. Interactive Box Size Prompt

In interactive mode, users are now prompted to enter a custom box size:

```
Enter custom box size in Å (e.g., 25 or 20 20 20), or press Enter for default (20 20 20):
```

**Options**:
- Press Enter → Use default 20 Å
- Enter single value (e.g., `25`) → Use 25 Å in all dimensions
- Enter three values (e.g., `25 30 20`) → Use different size for each axis

### 3. Command-Line Box Size Option

Added `--box-size` argument to specify box size via command line:

```bash
# Uniform box size
python extract_ligand_center.py -i protein.pdb -s 5 --box-size "25"

# Different dimensions
python extract_ligand_center.py -i protein.pdb -s 5 --box-size "25 30 20"
```

### 4. Removed Padding Argument

**Removed**: `--padding` argument (no longer needed)
**Replaced with**: `--box-size` argument (more intuitive)

---

## Usage Examples

### Interactive Mode (Default Behavior)

```bash
$ python extract_ligand_center.py -i protein.pdb

Found 8 ligand(s):
...
Enter ligand number to get docking box parameters (or 'q' to quit): 5

Enter custom box size in Å (e.g., 25 or 20 20 20), or press Enter for default (20 20 20): 

# User presses Enter for default

Docking box (default size: 20 Å):
  Size: (20.000, 20.000, 20.000)
```

### Interactive Mode with Custom Size

```bash
$ python extract_ligand_center.py -i protein.pdb

Enter ligand number to get docking box parameters (or 'q' to quit): 5

Enter custom box size in Å (e.g., 25 or 20 20 20), or press Enter for default (20 20 20): 30

Docking box (custom size):
  Size: (30.000, 30.000, 30.000)
```

### Direct Selection with Command-Line Box Size

```bash
$ python extract_ligand_center.py -i protein.pdb -s 5 --box-size "25"

Docking box (custom size):
  Size: (25.000, 25.000, 25.000)
```

### Different Dimensions

```bash
$ python extract_ligand_center.py -i protein.pdb -s 5 --box-size "25 30 20"

Docking box (custom size):
  Size: (25.000, 30.000, 20.000)
```

---

## Rationale

### Why 20 Å Default?

1. **Standard Practice**: 20 Å is a commonly used box size in molecular docking
2. **Suitable for Most Cases**: Large enough for ligand flexibility, small enough for efficiency
3. **Consistent**: Same size regardless of ligand, making results more comparable
4. **Adjustable**: Users can easily customize when needed

### Why Remove Padding?

1. **More Intuitive**: Users think in terms of "box size" not "padding"
2. **Direct Control**: Specify exactly what you want
3. **Clearer**: "20 Å box" is clearer than "ligand + 8 Å padding"
4. **Standard**: Matches how other docking tools specify box dimensions

---

## Box Size Guidelines

### General Recommendations

| Scenario | Recommended Box Size | Rationale |
|----------|---------------------|-----------|
| Re-docking | 15-20 Å | Focused search around known binding site |
| Virtual Screening | 20-25 Å | Standard size for most ligands |
| Large Ligands | 25-30 Å | More space for conformational changes |
| Blind Docking | 30+ Å | Cover larger binding region |
| Small Molecules | 15-18 Å | Faster, sufficient space |

### How to Choose

1. **Start with default (20 Å)** - Good for most cases
2. **Check ligand size** - Displayed in the output
3. **Consider flexibility** - Larger ligands may need more space
4. **Balance speed vs. thoroughness** - Larger boxes take longer

---

## Code Changes

### Modified Functions

1. **main()** - Added box size prompt and parsing logic
2. **Command-line arguments** - Replaced `--padding` with `--box-size`
3. **Output display** - Shows "default" or "custom" box type

### New Logic Flow

```
1. User selects ligand
2. If interactive mode:
   - Prompt for custom box size
   - Parse input (single value or three values)
   - Validate input
3. If --box-size provided:
   - Parse command-line argument
4. Otherwise:
   - Use default 20 Å
5. Display box parameters
```

---

## Documentation Updates

Updated all documentation files:

- ✅ `extract_ligand_center.py` - Help text and examples
- ✅ `README.md` - Quick start guide
- ✅ `LIGAND_EXTRACTOR_README.md` - Full usage documentation
- ✅ `TUTORIAL.md` - Tutorial examples
- ✅ `QUICK_START_GUIDE.md` - Comprehensive guide
- ✅ `EXAMPLE_WORKFLOW.md` - Workflow examples

---

## Testing

All scenarios tested and working:

✅ Interactive mode with default (press Enter)
✅ Interactive mode with single value (e.g., 25)
✅ Interactive mode with three values (e.g., 25 30 20)
✅ Direct selection with --box-size (single value)
✅ Direct selection with --box-size (three values)
✅ Auto-select mode with default
✅ Auto-select mode with --box-size
✅ Invalid input handling
✅ Keyboard interrupt (Ctrl+C)

---

## Backward Compatibility

### Breaking Changes

⚠️ **Removed**: `--padding` argument
- **Migration**: Use `--box-size` instead
- **Old**: `--padding 8.0` (resulted in variable box sizes)
- **New**: `--box-size "20"` (explicit box size)

### Non-Breaking Changes

✅ All other command-line options work the same
✅ Interactive mode enhanced (now prompts for box size)
✅ Output format similar (just different box size values)

---

## Benefits

1. ✅ **Simpler**: Default 20 Å is easy to remember
2. ✅ **More Control**: Users specify exact box size
3. ✅ **Consistent**: Same default for all ligands
4. ✅ **Flexible**: Easy to customize when needed
5. ✅ **Standard**: Aligns with common docking practices
6. ✅ **Interactive**: Prompts guide users through choices

---

## Example Complete Workflow

```bash
# Step 1: Extract ligand center with custom box
$ python extract_ligand_center.py -i 1iep.pdb

Found 8 ligand(s):
...
Enter ligand number: 5
Enter custom box size (or press Enter for default 20 Å): 25

Docking box (custom size):
  Size: (25.000, 25.000, 25.000)

Use these parameters:
mk_prepare_receptor.py \
  -i receptor.pdb \
  -o receptor_prepared \
  -p -v \
  --box_size 25.0 25.0 25.0 \
  --box_center 15.614 53.380 15.455

# Step 2: Prepare receptor (copy-paste from above)
$ mk_prepare_receptor.py -i receptor.pdb -o receptor_prepared -p -v \
    --box_size 25.0 25.0 25.0 --box_center 15.614 53.380 15.455

# Step 3: Prepare ligand
$ mk_prepare_ligand.py -i ligand.sdf -o ligand.pdbqt

# Step 4: Run docking
$ vina --receptor receptor_prepared.pdbqt \
       --ligand ligand.pdbqt \
       --config receptor_prepared.box.txt \
       --exhaustiveness=32 \
       --out docked.pdbqt
```

---

**Date**: 2025-10-29  
**Version**: 1.2.0  
**Status**: Complete and Tested
