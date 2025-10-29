#!/usr/bin/env python3
"""
Extract ligand information from PDB/CIF files and calculate center coordinates.
This tool helps identify ligands in a structure and provides the center coordinates
needed for molecular docking with AutoDock Vina.
"""

import argparse
import sys
from pathlib import Path
from collections import defaultdict
import numpy as np


class LigandExtractor:
    """Extract and analyze ligands from PDB/CIF files."""

    def __init__(self, input_file):
        self.input_file = Path(input_file)
        self.ligands = defaultdict(list)
        self.file_format = self._detect_format()

    def _detect_format(self):
        """Detect file format based on extension."""
        suffix = self.input_file.suffix.lower()
        if suffix in [".pdb", ".ent"]:
            return "pdb"
        elif suffix in [".cif", ".mmcif"]:
            return "cif"
        else:
            raise ValueError(f"Unsupported file format: {suffix}. Use .pdb or .cif")

    def parse_pdb(self):
        """Parse PDB file and extract HETATM records (ligands)."""
        with open(self.input_file, "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("HETATM"):
                    try:
                        # PDB format specification
                        atom_name = line[12:16].strip()
                        res_name = line[17:20].strip()
                        chain_id = line[21:22].strip()
                        res_seq = line[22:26].strip()
                        x = float(line[30:38].strip())
                        y = float(line[38:46].strip())
                        z = float(line[46:54].strip())
                        element = (
                            line[76:78].strip() if len(line) > 76 else atom_name[0]
                        )

                        # Skip water molecules
                        if res_name in ["HOH", "WAT", "H2O", "TIP", "TIP3", "SOL"]:
                            continue

                        # Create unique ligand identifier
                        ligand_id = f"{res_name}_{chain_id}_{res_seq}"

                        self.ligands[ligand_id].append(
                            {
                                "atom_name": atom_name,
                                "res_name": res_name,
                                "chain_id": chain_id,
                                "res_seq": res_seq,
                                "x": x,
                                "y": y,
                                "z": z,
                                "element": element,
                            }
                        )
                    except (ValueError, IndexError):
                        print(
                            f"Warning: Could not parse line: {line.strip()}",
                            file=sys.stderr,
                        )
                        continue

    def parse_cif(self):
        """Parse mmCIF file and extract ligand records."""
        in_atom_site = False
        headers = []

        with open(self.input_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()

                # Start of atom_site loop
                if line.startswith("loop_"):
                    in_atom_site = False
                    headers = []
                elif line.startswith("_atom_site."):
                    in_atom_site = True
                    headers.append(line.split(".")[1])
                elif in_atom_site and headers and not line.startswith("_"):
                    if line.startswith("#") or not line:
                        in_atom_site = False
                        continue

                    try:
                        parts = line.split()
                        if len(parts) < len(headers):
                            continue

                        data = dict(zip(headers, parts))

                        # Only process HETATM records
                        if data.get("group_PDB") != "HETATM":
                            continue

                        res_name = data.get("label_comp_id", "")

                        # Skip water molecules
                        if res_name in ["HOH", "WAT", "H2O", "TIP", "TIP3", "SOL"]:
                            continue

                        chain_id = data.get(
                            "auth_asym_id", data.get("label_asym_id", "")
                        )
                        res_seq = data.get("auth_seq_id", data.get("label_seq_id", ""))

                        ligand_id = f"{res_name}_{chain_id}_{res_seq}"

                        self.ligands[ligand_id].append(
                            {
                                "atom_name": data.get("label_atom_id", ""),
                                "res_name": res_name,
                                "chain_id": chain_id,
                                "res_seq": res_seq,
                                "x": float(data.get("Cartn_x", 0)),
                                "y": float(data.get("Cartn_y", 0)),
                                "z": float(data.get("Cartn_z", 0)),
                                "element": data.get("type_symbol", ""),
                            }
                        )
                    except (ValueError, KeyError, IndexError):
                        continue

    def extract_ligands(self):
        """Extract ligands based on file format."""
        if self.file_format == "pdb":
            self.parse_pdb()
        elif self.file_format == "cif":
            self.parse_cif()

        return self.ligands

    def calculate_center(self, ligand_atoms):
        """Calculate geometric center of ligand atoms."""
        coords = np.array([[atom["x"], atom["y"], atom["z"]] for atom in ligand_atoms])
        center = np.mean(coords, axis=0)
        return center

    def calculate_bounding_box(self, ligand_atoms):
        """Calculate bounding box dimensions for the ligand."""
        coords = np.array([[atom["x"], atom["y"], atom["z"]] for atom in ligand_atoms])
        min_coords = np.min(coords, axis=0)
        max_coords = np.max(coords, axis=0)
        dimensions = max_coords - min_coords
        return dimensions, min_coords, max_coords


def display_ligands(ligands, extractor):
    """Display found ligands with details."""
    if not ligands:
        print("\nNo ligands found in the structure.")
        print("(Water molecules are automatically excluded)")
        return False

    print(f"\nFound {len(ligands)} ligand(s):\n")
    print(
        f"{'#':<4} {'Ligand ID':<20} {'Atoms':<8} {'Center (x, y, z)':<30} {'Box Size (x, y, z)'}"
    )
    print("-" * 100)

    for idx, (ligand_id, atoms) in enumerate(ligands.items(), 1):
        center = extractor.calculate_center(atoms)
        dimensions, _, _ = extractor.calculate_bounding_box(atoms)

        print(
            f"{idx:<4} {ligand_id:<20} {len(atoms):<8} "
            f"({center[0]:6.2f}, {center[1]:6.2f}, {center[2]:6.2f})   "
            f"({dimensions[0]:5.2f}, {dimensions[1]:5.2f}, {dimensions[2]:5.2f})"
        )

    return True


def main():
    parser = argparse.ArgumentParser(
        description="Extract ligand information and calculate center coordinates for molecular docking",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive mode - prompts for ligand selection and box size
  %(prog)s -i protein.pdb
  
  # Select a specific ligand directly (uses default 20 Å box)
  %(prog)s -i protein.pdb -s 1
  
  # Automatically select if only one ligand exists
  %(prog)s -i protein.pdb -a
        """,
    )

    parser.add_argument("-i", "--input", required=True, help="Input PDB or CIF file")
    parser.add_argument(
        "-s",
        "--select",
        type=int,
        help="Select ligand by number directly (skips interactive prompt)",
    )
    parser.add_argument(
        "-a",
        "--auto",
        action="store_true",
        help="Automatically select if only one ligand exists",
    )
    parser.add_argument(
        "--box-size",
        type=str,
        help='Custom box size in Å (e.g., "25" or "20 20 20"). Default: 20 20 20',
    )
    parser.add_argument(
        "-o", "--output", help="Output file to save ligand coordinates (SDF format)"
    )

    args = parser.parse_args()

    # Check if input file exists
    if not Path(args.input).exists():
        print(f"Error: Input file '{args.input}' not found.", file=sys.stderr)
        sys.exit(1)

    # Extract ligands
    print(f"Parsing {args.input}...")
    extractor = LigandExtractor(args.input)
    ligands = extractor.extract_ligands()

    # Display ligands
    if not display_ligands(ligands, extractor):
        sys.exit(1)

    # Handle selection
    selected_ligand = None
    ligand_list = list(ligands.items())

    if args.select:
        if 1 <= args.select <= len(ligands):
            selected_ligand = ligand_list[args.select - 1]
        else:
            print(
                f"\nError: Invalid selection. Choose a number between 1 and {len(ligands)}.",
                file=sys.stderr,
            )
            sys.exit(1)
    elif args.auto and len(ligands) == 1:
        selected_ligand = ligand_list[0]
        print(f"\nAuto-selected: {selected_ligand[0]}")
    elif not args.select:
        # Interactive selection
        print(
            "\nEnter ligand number to get docking box parameters (or 'q' to quit): ",
            end="",
        )
        try:
            user_input = input().strip()
            if user_input.lower() == "q":
                print("Exiting.")
                sys.exit(0)

            selection = int(user_input)
            if 1 <= selection <= len(ligands):
                selected_ligand = ligand_list[selection - 1]
            else:
                print(
                    f"\nError: Invalid selection. Choose a number between 1 and {len(ligands)}.",
                    file=sys.stderr,
                )
                sys.exit(1)
        except ValueError:
            print(
                "\nError: Please enter a valid number or 'q' to quit.", file=sys.stderr
            )
            sys.exit(1)
        except (KeyboardInterrupt, EOFError):
            print("\n\nExiting.")
            sys.exit(0)

    # Display detailed information for selected ligand
    if selected_ligand:
        ligand_id, atoms = selected_ligand
        center = extractor.calculate_center(atoms)
        dimensions, min_coords, max_coords = extractor.calculate_bounding_box(atoms)

        # Determine box size
        custom_box_size = None

        # Check if box size was provided via command line
        if args.box_size:
            try:
                parts = args.box_size.split()
                if len(parts) == 1:
                    size = float(parts[0])
                    custom_box_size = np.array([size, size, size])
                elif len(parts) == 3:
                    custom_box_size = np.array(
                        [float(parts[0]), float(parts[1]), float(parts[2])]
                    )
                else:
                    print(
                        "Warning: Invalid --box-size format. Using default.",
                        file=sys.stderr,
                    )
            except ValueError:
                print(
                    "Warning: Invalid --box-size value. Using default.",
                    file=sys.stderr,
                )
        elif not args.select and not args.auto:
            # Only prompt in interactive mode if not provided via command line
            print(
                "\nEnter custom box size in Å (e.g., 25 or 20 20 20), or press Enter for default (20 20 20): ",
                end="",
            )
            try:
                box_input = input().strip()
                if box_input:
                    # Parse box size input
                    parts = box_input.split()
                    if len(parts) == 1:
                        # Single value - use for all dimensions
                        size = float(parts[0])
                        custom_box_size = np.array([size, size, size])
                    elif len(parts) == 3:
                        # Three values - one for each dimension
                        custom_box_size = np.array(
                            [float(parts[0]), float(parts[1]), float(parts[2])]
                        )
                    else:
                        print(
                            "Warning: Invalid format. Using default box size.",
                            file=sys.stderr,
                        )
            except ValueError:
                print(
                    "Warning: Invalid box size. Using default box size.",
                    file=sys.stderr,
                )
            except (KeyboardInterrupt, EOFError):
                print("\n\nExiting.")
                sys.exit(0)

        # Determine final box size
        if custom_box_size is not None:
            suggested_box = custom_box_size
            box_type = "custom"
        else:
            # Default box size is 20 Å in all dimensions
            suggested_box = np.array([20.0, 20.0, 20.0])
            box_type = "default"

        print("\n" + "=" * 80)
        print(f"Selected Ligand: {ligand_id}")
        print("=" * 80)
        print(f"Number of atoms: {len(atoms)}")
        print(f"Residue name: {atoms[0]['res_name']}")
        print(f"Chain: {atoms[0]['chain_id']}")
        print(f"Residue number: {atoms[0]['res_seq']}")
        print("\nGeometric center:")
        print(f"  X: {center[0]:.3f}")
        print(f"  Y: {center[1]:.3f}")
        print(f"  Z: {center[2]:.3f}")
        print("\nLigand bounding box:")
        print(f"  Min: ({min_coords[0]:.3f}, {min_coords[1]:.3f}, {min_coords[2]:.3f})")
        print(f"  Max: ({max_coords[0]:.3f}, {max_coords[1]:.3f}, {max_coords[2]:.3f})")
        print(
            f"  Size: ({dimensions[0]:.3f}, {dimensions[1]:.3f}, {dimensions[2]:.3f})"
        )
        if box_type == "custom":
            print("\nDocking box (custom size):")
        else:
            print("\nDocking box (default size: 20 Å):")
        print(
            f"  Size: ({suggested_box[0]:.3f}, {suggested_box[1]:.3f}, {suggested_box[2]:.3f})"
        )
        print("\n" + "=" * 80)
        print("Use these parameters with mk_prepare_receptor.py:")
        print("=" * 80)
        print("\nmk_prepare_receptor.py \\")
        print("  -i your_receptor.pdb \\")
        print("  -o receptor_prepared \\")
        print("  -p -v \\")
        print(
            f"  --box_size {suggested_box[0]:.1f} {suggested_box[1]:.1f} {suggested_box[2]:.1f} \\"
        )
        print(f"  --box_center {center[0]:.3f} {center[1]:.3f} {center[2]:.3f}")
        print()


if __name__ == "__main__":
    main()
