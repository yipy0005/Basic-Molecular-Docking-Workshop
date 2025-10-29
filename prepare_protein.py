#!/usr/bin/env python3
"""
Prepare protein structures for molecular docking by removing waters and ligands.
This tool extracts only the protein atoms (ATOM records) from PDB/CIF files.
"""

import argparse
import sys
from pathlib import Path
from collections import defaultdict


class ProteinPreparer:
    """Prepare protein structures by removing waters and ligands."""

    def __init__(self, input_file, keep_hetero=None):
        self.input_file = Path(input_file)
        self.keep_hetero = set(keep_hetero) if keep_hetero else set()
        self.file_format = self._detect_format()
        self.protein_atoms = []
        self.removed_waters = 0
        self.removed_ligands = defaultdict(int)
        self.kept_hetero = defaultdict(int)

    def _detect_format(self):
        """Detect file format based on extension."""
        suffix = self.input_file.suffix.lower()
        if suffix in [".pdb", ".ent"]:
            return "pdb"
        if suffix in [".cif", ".mmcif"]:
            return "cif"
        raise ValueError(f"Unsupported file format: {suffix}. Use .pdb or .cif")

    def process_pdb(self):
        """Process PDB file and extract protein atoms."""
        with open(self.input_file, "r", encoding="utf-8") as f:
            for line in f:
                # Keep ATOM records (protein)
                if line.startswith("ATOM"):
                    self.protein_atoms.append(line)

                # Handle HETATM records
                elif line.startswith("HETATM"):
                    res_name = line[17:20].strip()

                    # Count and skip water molecules
                    if res_name in ["HOH", "WAT", "H2O", "TIP", "TIP3", "SOL"]:
                        self.removed_waters += 1
                        continue

                    # Keep specified heteroatoms (e.g., cofactors)
                    if res_name in self.keep_hetero:
                        self.protein_atoms.append(line)
                        self.kept_hetero[res_name] += 1
                    else:
                        # Count removed ligands
                        self.removed_ligands[res_name] += 1

                # Keep header and structural information
                elif line.startswith(
                    (
                        "HEADER",
                        "TITLE",
                        "COMPND",
                        "SOURCE",
                        "KEYWDS",
                        "EXPDTA",
                        "AUTHOR",
                        "REVDAT",
                        "REMARK",
                        "SEQRES",
                        "CRYST1",
                        "MODEL",
                        "ENDMDL",
                        "TER",
                        "END",
                    )
                ):
                    self.protein_atoms.append(line)

    def process_cif(self):
        """Process mmCIF file and extract protein atoms."""
        in_atom_site = False
        headers = []
        header_lines = []

        with open(self.input_file, "r", encoding="utf-8") as f:
            for line in f:
                original_line = line
                line = line.strip()

                # Keep header information
                if not in_atom_site and not line.startswith("_atom_site."):
                    header_lines.append(original_line)

                # Start of atom_site loop
                if line.startswith("loop_"):
                    in_atom_site = False
                    headers = []
                    header_lines.append(original_line)
                elif line.startswith("_atom_site."):
                    in_atom_site = True
                    headers.append(line.split(".")[1])
                    header_lines.append(original_line)
                elif in_atom_site and headers and not line.startswith("_"):
                    if line.startswith("#") or not line:
                        in_atom_site = False
                        if line.startswith("#"):
                            header_lines.append(original_line)
                        continue

                    try:
                        parts = line.split()
                        if len(parts) < len(headers):
                            continue

                        data = dict(zip(headers, parts))
                        group_pdb = data.get("group_PDB", "")
                        res_name = data.get("label_comp_id", "")

                        # Keep ATOM records (protein)
                        if group_pdb == "ATOM":
                            self.protein_atoms.append(original_line)

                        # Handle HETATM records
                        elif group_pdb == "HETATM":
                            # Count and skip water molecules
                            if res_name in [
                                "HOH",
                                "WAT",
                                "H2O",
                                "TIP",
                                "TIP3",
                                "SOL",
                            ]:
                                self.removed_waters += 1
                                continue

                            # Keep specified heteroatoms
                            if res_name in self.keep_hetero:
                                self.protein_atoms.append(original_line)
                                self.kept_hetero[res_name] += 1
                            else:
                                # Count removed ligands
                                self.removed_ligands[res_name] += 1

                    except (ValueError, KeyError, IndexError):
                        continue

        # Add headers at the beginning
        self.protein_atoms = header_lines + self.protein_atoms

    def prepare(self):
        """Prepare protein structure based on file format."""
        if self.file_format == "pdb":
            self.process_pdb()
        elif self.file_format == "cif":
            self.process_cif()

    def write_output(self, output_file):
        """Write prepared protein structure to file."""
        output_path = Path(output_file)

        # Ensure output has same format as input
        if output_path.suffix.lower() not in [".pdb", ".ent", ".cif", ".mmcif"]:
            output_path = output_path.with_suffix(self.input_file.suffix)

        with open(output_path, "w", encoding="utf-8") as f:
            f.writelines(self.protein_atoms)

        return output_path

    def print_summary(self):
        """Print summary of preparation."""
        print("\n" + "=" * 80)
        print("Protein Preparation Summary")
        print("=" * 80)
        print(f"Input file: {self.input_file}")
        print(f"Format: {self.file_format.upper()}")
        protein_atom_count = len(
            [line for line in self.protein_atoms if line.startswith("ATOM")]
        )
        print(f"\nProtein atoms: {protein_atom_count}")

        if self.removed_waters > 0:
            print(f"\nRemoved water molecules: {self.removed_waters}")

        if self.removed_ligands:
            print("\nRemoved ligands:")
            for res_name, count in sorted(self.removed_ligands.items()):
                print(f"  {res_name}: {count} atoms")

        if self.kept_hetero:
            print("\nKept heteroatoms (as requested):")
            for res_name, count in sorted(self.kept_hetero.items()):
                print(f"  {res_name}: {count} atoms")

        print("=" * 80)


def main():
    parser = argparse.ArgumentParser(
        description="Prepare protein structures by removing waters and ligands",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Remove all waters and ligands
  %(prog)s -i protein.pdb -o protein_clean.pdb
  
  # Keep specific heteroatoms (e.g., cofactors)
  %(prog)s -i protein.pdb -o protein_clean.pdb --keep HEM NAD
  
  # Process CIF file
  %(prog)s -i protein.cif -o protein_clean.cif
  
  # Interactive mode - shows what will be removed
  %(prog)s -i protein.pdb -o protein_clean.pdb --interactive
        """,
    )

    parser.add_argument("-i", "--input", required=True, help="Input PDB or CIF file")
    parser.add_argument(
        "-o", "--output", required=True, help="Output file for cleaned protein"
    )
    parser.add_argument(
        "--keep",
        nargs="+",
        help="Heteroatom residue names to keep (e.g., HEM NAD FAD)",
    )
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Show what will be removed and ask for confirmation",
    )
    parser.add_argument(
        "--quiet", action="store_true", help="Suppress output messages"
    )

    args = parser.parse_args()

    # Check if input file exists
    if not Path(args.input).exists():
        print(f"Error: Input file '{args.input}' not found.", file=sys.stderr)
        sys.exit(1)

    # Initialize preparer
    if not args.quiet:
        print(f"Processing {args.input}...")

    preparer = ProteinPreparer(args.input, args.keep)
    preparer.prepare()

    # Interactive mode - show preview and ask for confirmation
    if args.interactive:
        preparer.print_summary()
        print("\nProceed with writing output? (y/n): ", end="")
        try:
            response = input().strip().lower()
            if response != "y":
                print("Operation cancelled.")
                sys.exit(0)
        except (KeyboardInterrupt, EOFError):
            print("\n\nOperation cancelled.")
            sys.exit(0)

    # Write output
    output_path = preparer.write_output(args.output)

    if not args.quiet:
        preparer.print_summary()
        print(f"\nOutput written to: {output_path}")
        print("\nNext steps:")
        print("1. Add hydrogens (if needed):")
        print(f"   reduce {output_path} > {output_path.stem}_H.pdb")
        print("2. Prepare for docking:")
        print(
            f"   mk_prepare_receptor.py -i {output_path.stem}_H.pdb -o receptor_prepared"
        )


if __name__ == "__main__":
    main()
