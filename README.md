# Basic Molecular Docking Workshop

Welcome to the **Basic Molecular Docking Workshop**! This guide will walk you through every step, from installing Anaconda to setting up and activating your workshop environment. Even if you're completely new to using a terminal (the program where you type commands), don’t worry—we’ve got you covered.

> **Note:** First complete the setup steps below to configure your environment, then follow the step-by-step instructions in [TUTORIAL.md](https://github.com/yipy0005/Basic-Molecular-Docking-Workshop/blob/main/TUTORIAL.md) to learn how to perform molecular docking.

> **New:** Check out [EXAMPLE_WORKFLOW.md](EXAMPLE_WORKFLOW.md) for a complete end-to-end example with the 1IEP structure.

> **📚 Documentation:** See [DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md) for a complete guide to all available documentation.

---

## Table of Contents

1. [What You’ll Learn](#what-youll-learn)  
2. [Prerequisites](#prerequisites)  
3. [Step 1: Install Anaconda](#step-1-install-anaconda)  
4. [Step 2: Open a Terminal](#step-2-open-a-terminal)  
5. [Step 3: Clone the Workshop Repository](#step-3-clone-the-workshop-repository)  
6. [Step 4: Run the Setup Script](#step-4-run-the-setup-script)  
7. [Using the `pdbqt2pdb.sh` Script](#using-the-pdbqt2pdbsh-script)  
8. [Extracting Ligand Center Coordinates](#extracting-ligand-center-coordinates)  
9. [Running the Chemical Editor](#running-the-chemical-editor)  
10. [Uninstallation](#uninstallation)  
11. [Troubleshooting](#troubleshooting)  
12. [Future Features](#future-features)  
13. [Acknowledgments](#acknowledgments)  

---

## What You’ll Learn

* How to install Anaconda, a tool that manages Python and packages for you.  
* What a terminal (or command prompt) is and how to open it.  
* How to clone the workshop repository.  
* How to run the provided `setup.sh` to configure your Conda environment, install dependencies, and verify your setup.  
* How to launch the included chemical editor (`chemdraw`).  
* How to uninstall the workshop and remove all related files and environments.

## Prerequisites

* A computer running **Windows**, **macOS**, or **Linux**.  
* Internet connection to download Anaconda and the workshop materials.  

---

## Step 1: Install Anaconda

Anaconda is a free package manager that installs Python and many useful scientific packages.

1. Open your web browser and go to the [Anaconda Downloads page](https://www.anaconda.com/products/distribution).  
2. Choose the installer for your operating system (Windows, macOS, or Linux).  
3. Download the installer and follow the on-screen instructions:
   - **Windows**: Double-click the `.exe` file and click through the install wizard.  
   - **macOS**: Open the `.pkg` file and follow the prompts.  
   - **Linux**: Open a terminal and run `bash ~/Downloads/Anaconda3-*.sh`, then follow the prompts.

Once installation is complete, you’ll have access to the `conda` command-line tool.

---

## Step 2: Open a Terminal

A **terminal** (also called a command prompt or shell) is a program where you type text commands to control your computer.

- **Windows**:  
  1. Click the Start menu.  
  2. Search for **Anaconda Prompt** or **Command Prompt**.  
  3. Click to open it.  
- **macOS**:  
  1. Open **Finder** > **Applications** > **Utilities**.  
  2. Double-click **Terminal**.  
- **Linux**:  
  1. Press `Ctrl + Alt + T` or search for **Terminal** in your applications menu.

You should see a window with a prompt, such as `C:\Users\YourName>` on Windows or `your-macbook:~ yourname$` on macOS/Linux.

---

## Step 3: Clone the Workshop Repository

1. In your terminal, navigate to the folder where you want to keep the workshop files. For example:  
   ```bash
   cd ~/Documents
   ```
2. Clone this repository from GitHub (you need to have [Git installed](https://git-scm.com/)—Anaconda includes Git by default):  
   ```bash
   git clone https://github.com/yipy0005/Basic-Molecular-Docking-Workshop.git
   ```
3. Change into the workshop directory:  
   ```bash
   cd Basic-Molecular-Docking-Workshop
   ```

---

## Step 4: Run the Setup Script

We’ve provided a `setup.sh` that automates environment creation, dependency installation, and verification:

1. Make the script executable (only needed once):  
   ```bash
   chmod +x setup.sh
   ```
2. Run it:  
   ```bash
   ./setup.sh
   ```
3. Follow the on-screen output. When it finishes, you’ll have:
   - A Conda environment named `molecular_docking_workshop`  
   - All required packages (including Meeko, ProDy, AutoDock Vina, etc.)  
   - The chemical editor `chemdraw` installed and ready to launch  
   - Executables verified (`vina`, `reduce`, `python --version`)  
   - The helper script `pdbqt2pdb.sh` made executable  

Once `setup.sh` completes successfully, you’re ready to proceed to the tutorial.

---

## Using the `pdbqt2pdb.sh` Script

We provide a script to convert `.pdbqt` files into individual `.pdb` files.

1. (Already made executable by `setup.sh`—no action needed.)  
2. Run the script on a `.pdbqt` file:  
   ```bash
   ./pdbqt2pdb.sh my_structure.pdbqt
   ```
   - The script splits each `MODEL` into its own file and converts them to `.pdb` format.  
   - You’ll see output like:
     ```
     → Converted to my_structure_model1.pdb and removed my_structure_model1.pdbqt
     ```

---

## Extracting Ligand Center Coordinates

When preparing for molecular docking, you need to know where to center your docking box. The `extract_ligand_center.py` tool helps you identify ligands in PDB/CIF files and calculate appropriate box parameters.

### Quick Start

1. Run in interactive mode to see all ligands and select one:
   ```bash
   python extract_ligand_center.py -i input_files/protein.pdb
   ```
   The tool will:
   - List all ligands and prompt you to select one
   - Ask for a custom box size (or use default 20 Å)

2. Or directly select a ligand with custom box size:
   ```bash
   python extract_ligand_center.py -i input_files/protein.pdb -s 1 --box-size "25"
   ```

3. The tool will provide ready-to-use coordinates for `mk_prepare_receptor.py`:
   ```bash
   mk_prepare_receptor.py \
     -i your_receptor.pdb \
     -o receptor_prepared \
     -p -v \
     --box_size 24.7 32.7 29.5 \
     --box_center 15.614 53.380 15.455
   ```

For detailed usage and examples, see [LIGAND_EXTRACTOR_README.md](LIGAND_EXTRACTOR_README.md) or check out the [QUICK_START_GUIDE.md](QUICK_START_GUIDE.md).

---

## Running the Chemical Editor

After setup, launch the chemical editor by simply typing:

```bash
chemdraw
```

and pressing Enter. This will start the `chemdraw` application installed in your environment.

---

## Uninstallation

If you ever want to remove the workshop and its environment entirely, use the provided `uninstall.sh`:

1. Make the script executable (if you haven’t already):  
   ```bash
   chmod +x uninstall.sh
   ```
2. Run it:  
   ```bash
   ./uninstall.sh
   ```
3. This will:
   - Deactivate and remove the `molecular_docking_workshop` Conda environment  
   - Delete the entire `Basic-Molecular-Docking-Workshop` directory  

---

## Troubleshooting

* **"Command not found" errors**: Ensure you used `./setup.sh` and that it finished without errors.  
* **Permission denied** when running scripts: Verify `chmod +x setup.sh uninstall.sh pdbqt2pdb.sh` has been applied.  
* If you get stuck, feel free to ask for help or check online resources for Conda, Git, and the workshop repo.

---

## Future Features

We're continuously working to improve this workshop! Planned enhancements include:

### Automated Structure Preparation
- **Protein Preparation**: Automated hydrogen addition, charge assignment, and structure cleaning
- **Ligand Preparation**: Convert SMILES to 3D structures, handle protonation states, generate conformers
- **One-Click Workflow**: From raw structures to docking-ready files in a single command

### Enhanced Analysis Tools
- **Binding Site Detection**: Automatic identification of potential binding pockets
- **Flexible Residue Selection**: Suggest residues for flexible docking
- **Batch Processing**: Process multiple ligands or structures at once

See [FUTURE_FEATURES.md](FUTURE_FEATURES.md) for a comprehensive roadmap and detailed information about upcoming features.

**Your feedback matters!** If you have suggestions or feature requests, please open an issue on the repository.

---

## Acknowledgments

This workshop uses open-source tools including:

* [RDKit](https://www.rdkit.org/)  
* [AutoDock Vina](http://vina.scripps.edu/)  
* [Biopython, Gemmi, SciPy](https://www.scipy.org/)

Enjoy learning molecular docking!
