# Basic Molecular Docking Workshop

Welcome to the **Basic Molecular Docking Workshop**! This guide will walk you through every step, from installing Anaconda to setting up and activating your workshop environment. Even if you're completely new to using a terminal (the program where you type commands), don’t worry—we’ve got you covered.

> **Note:** First complete the setup steps below to configure your environment, then follow the step-by-step instructions in [TUTORIAL.md](https://github.com/yipy0005/Basic-Molecular-Docking-Workshop/blob/main/TUTORIAL.md) to learn how to perform molecular docking.

---

## Table of Contents

1. [What You’ll Learn](#what-youll-learn)  
2. [Prerequisites](#prerequisites)  
3. [Step 1: Install Anaconda](#step-1-install-anaconda)  
4. [Step 2: Open a Terminal](#step-2-open-a-terminal)  
5. [Step 3: Clone the Workshop Repository](#step-3-clone-the-workshop-repository)  
6. [Step 4: Run the Setup Script](#step-4-run-the-setup-script)  
7. [Using the `pdbqt2pdb.sh` Script](#using-the-pdbqt2pdbsh-script)  
8. [Running the Chemical Editor](#running-the-chemical-editor)  
9. [Uninstallation](#uninstallation)  
10. [Troubleshooting](#troubleshooting)  
11. [Acknowledgments](#acknowledgments)  

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

## Acknowledgments

This workshop uses open-source tools including:

* [RDKit](https://www.rdkit.org/)  
* [AutoDock Vina](http://vina.scripps.edu/)  
* [Biopython, Gemmi, SciPy](https://www.scipy.org/)

Enjoy learning molecular docking!
