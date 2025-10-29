# Histidine Protonation Troubleshooting Guide

## The Problem

When preparing proteins for docking, you may encounter this error:

```
RuntimeError: for residue_key='A:246', 3 have passed: ['HIE', 'HID', 'HIP'] 
and tied for fewest missing and excess H: HIE HID
```

This occurs because histidine can exist in three different protonation states, and the software cannot automatically determine which one is correct.

---

## Understanding Histidine Protonation States

Histidine has an imidazole ring with two nitrogen atoms that can be protonated:

### HIE (Epsilon Protonation)
- Hydrogen on **epsilon nitrogen (NE2)**
- Most common form at neutral pH
- Often involved in catalysis

### HID (Delta Protonation)
- Hydrogen on **delta nitrogen (ND1)**
- Less common than HIE
- Depends on local environment

### HIP (Doubly Protonated)
- Hydrogens on **both nitrogens**
- Positively charged (+1)
- Occurs at low pH (~6.0 or below)
- Important in acidic environments

---

## Solutions

### Solution 1: Use reduce with FLIP Optimization (Recommended)

The `-FLIP` option tells reduce to optimize hydrogen placement by considering the local environment:

```bash
reduce -FLIP protein_clean.pdb > protein_clean_H.pdb
```

Then proceed with receptor preparation:

```bash
mk_prepare_receptor.py \
  -i protein_clean_H.pdb \
  -o receptor_prepared \
  --box_size 20 20 20 \
  --box_center 15.614 53.380 15.455
```

**Pros:**
- Automatic optimization
- Considers hydrogen bonding network
- Usually gives best results

**Cons:**
- Takes slightly longer
- May still have ambiguous cases

---

### Solution 2: Manually Specify Histidine Protonation

Use the `-n` or `--set_template` flag with `mk_prepare_receptor.py`:

```bash
mk_prepare_receptor.py \
  -i protein_H.pdb \
  -o receptor_prepared \
  -n A:246=HIE \
  --box_size 20 20 20 \
  --box_center 15.614 53.380 15.455
```

**For multiple histidines:**
```bash
mk_prepare_receptor.py \
  -i protein_H.pdb \
  -o receptor_prepared \
  -n A:246=HIE,B:15=HID,A:100=HIP \
  --box_size 20 20 20 \
  --box_center 15.614 53.380 15.455
```

**Pros:**
- Full control over protonation
- Can match experimental data
- Reproducible

**Cons:**
- Requires knowledge of structure
- Manual decision needed

---

### Solution 3: Use Pre-Prepared Files

If available, use receptor files that have already been prepared correctly:

```bash
mk_prepare_receptor.py \
  -i input_files/1iep_receptorH.pdb \
  -o receptor_prepared \
  --box_size 20 20 20 \
  --box_center 15.614 53.380 15.455
```

**Pros:**
- No ambiguity
- Known to work
- Fast

**Cons:**
- Not always available
- May not match your needs

---

## How to Choose the Right Protonation State

### 1. Check the pH of Your System

- **pH 7.0-7.4** (physiological): Use HIE (most common)
- **pH < 6.0** (acidic): Consider HIP
- **pH > 8.0** (basic): Use HIE or HID

### 2. Look at the Local Environment

**Use HIE if:**
- NE2 is exposed to solvent
- NE2 forms hydrogen bonds with other residues
- Part of catalytic triad (e.g., serine proteases)

**Use HID if:**
- ND1 is exposed to solvent
- ND1 forms hydrogen bonds
- Coordinating metal ions through ND1

**Use HIP if:**
- In acidic environment
- Both nitrogens form hydrogen bonds
- Near negatively charged residues

### 3. Check Crystal Structure Data

If your structure is from PDB:
1. Look at the original paper
2. Check for notes about histidine protonation
3. Look at hydrogen bonding patterns in the structure

### 4. Use Computational Tools

Tools like PROPKA can predict pKa values:
```bash
propka3 protein.pdb
```

This will suggest protonation states based on the local environment.

---

## Common Scenarios

### Scenario 1: Catalytic Histidine

**Example**: Serine protease catalytic triad (His-Asp-Ser)

**Solution**: Usually HIE
```bash
mk_prepare_receptor.py -i protein_H.pdb -o receptor -n A:57=HIE
```

### Scenario 2: Metal-Coordinating Histidine

**Example**: Zinc-binding site

**Solution**: Usually HID (coordinates through ND1)
```bash
mk_prepare_receptor.py -i protein_H.pdb -o receptor -n A:246=HID
```

### Scenario 3: Surface-Exposed Histidine

**Example**: Histidine on protein surface

**Solution**: Usually HIE at pH 7.4
```bash
mk_prepare_receptor.py -i protein_H.pdb -o receptor -n A:123=HIE
```

### Scenario 4: Buried Histidine

**Example**: Histidine in hydrophobic core

**Solution**: Check hydrogen bonding; usually HIE or HID
```bash
mk_prepare_receptor.py -i protein_H.pdb -o receptor -n A:89=HIE
```

---

## Quick Decision Tree

```
Is the histidine in the active site?
├─ Yes → Check literature/mechanism
│   ├─ Catalytic → Usually HIE
│   └─ Metal binding → Usually HID
│
└─ No → Is it surface exposed?
    ├─ Yes → Use HIE (most common at pH 7.4)
    └─ No → Check hydrogen bonding
        ├─ H-bond through NE2 → HIE
        ├─ H-bond through ND1 → HID
        └─ Both → HIP (rare at neutral pH)
```

---

## Testing Your Choice

After preparing the receptor, check:

1. **Visual inspection** (PyMOL):
   ```bash
   pymol protein_prepared.pdb
   ```
   Look at hydrogen bonding patterns

2. **Docking results**:
   - Run docking with different protonation states
   - Compare binding affinities
   - Check if poses make chemical sense

3. **Compare with crystal structure**:
   - If re-docking, compare with known ligand position
   - RMSD should be < 2 Å for correct protonation

---

## Example: Complete Workflow with Histidine Handling

```bash
# Step 1: Clean protein
python prepare_protein.py -i protein.pdb -o protein_clean.pdb

# Step 2: Add hydrogens with optimization
reduce -FLIP protein_clean.pdb > protein_clean_H.pdb

# Step 3: Try automatic preparation
mk_prepare_receptor.py \
  -i protein_clean_H.pdb \
  -o receptor_prepared \
  --box_size 20 20 20 \
  --box_center 15.6 53.4 15.5

# If error occurs, specify histidine protonation
mk_prepare_receptor.py \
  -i protein_clean_H.pdb \
  -o receptor_prepared \
  -n A:246=HIE,B:15=HID \
  --box_size 20 20 20 \
  --box_center 15.6 53.4 15.5

# Step 4: Verify and proceed with docking
```

---

## Additional Resources

- **reduce documentation**: http://kinemage.biochem.duke.edu/software/reduce.php
- **PROPKA**: https://github.com/jensengroup/propka
- **Histidine chemistry**: https://en.wikipedia.org/wiki/Histidine
- **pKa prediction**: H++ server (http://biophysics.cs.vt.edu/H++)

---

## Summary

**Quick Fix:**
```bash
reduce -FLIP protein.pdb > protein_H.pdb
```

**If that fails:**
```bash
mk_prepare_receptor.py -i protein_H.pdb -o receptor -n CHAIN:RES=HIE
```

**Default choice at pH 7.4:** HIE

**When in doubt:** Try all three and compare docking results!

---

**Last Updated**: 2025-10-29  
**Related**: PROTEIN_PREPARER_README.md, TUTORIAL.md
