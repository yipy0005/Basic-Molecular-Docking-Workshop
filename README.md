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
6. [Step 4: Create the Conda Environment](#step-4-create-the-conda-environment)
7. [Step 5: Activate the Environment](#step-5-activate-the-environment)
8. [Step 6: Verify Your Setup](#step-6-verify-your-setup)
9. [Using the `pdbqt2pdb.sh` Script](#using-the-pdbqt2pdbsh-script)
10. [Troubleshooting](#troubleshooting)
11. [Acknowledgments](#acknowledgments)

---

## What You’ll Learn

* How to install Anaconda, a tool that manages Python and packages for you.
* What a terminal (or command prompt) is and how to open it.
* How to create and manage a reproducible Python environment using Conda.
* How to activate that environment and run scripts for molecular docking preparation.

## Prerequisites

* A computer running **Windows**, **macOS**, or **Linux**.
* Internet connection to download Anaconda and the workshop materials.

---

## Step 1: Install Anaconda

Anaconda is a free package manager that installs Python and many useful scientific packages.

1. Open your web browser and go to the [Anaconda Downloads page](https://www.anaconda.com/products/distribution).
2. Choose the installer for your operating system (Windows, macOS, or Linux).
3. Download the installer and follow the on-screen instructions:

   * **Windows**: Double-click the `.exe` file and click through the install wizard.
   * **macOS**: Open the `.pkg` file and follow the prompts.
   * **Linux**: Open a terminal and run `bash ~/Downloads/Anaconda3-*.sh`, then follow the prompts.

Once installation is complete, you’ll have access to the `conda` command-line tool.

---

## Step 2: Open a Terminal

A **terminal** (also called a command prompt or shell) is a program where you type text commands to control your computer.

* **Windows**:

  1. Click the Start menu.
  2. Search for **Anaconda Prompt** or **Command Prompt**.
  3. Click to open it.
* **macOS**:

  1. Open **Finder** > **Applications** > **Utilities**.
  2. Double-click **Terminal**.
* **Linux**:

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
   git clone https://github.com/YourUser/Basic-Molecular-Docking-Workshop.git
   ```

3. Change into the workshop directory:

   ```bash
   cd Basic-Molecular-Docking-Workshop
   ```

---

## Step 4: Create the Conda Environment

The `environment.yml` file lists all the software and packages we need.

1. In the terminal (make sure you’re inside the `Basic-Molecular-Docking-Workshop` folder), run:

   ```bash
   conda env create -f environment.yml
   ```

2. Wait while Conda downloads and installs everything. This may take several minutes.

You now have a new environment named `molecular_docking_workshop`.

---

## Step 5: Activate the Environment

Before using any workshop tools, you must "activate" the environment:

* **All operating systems**:

  ```bash
  conda activate molecular_docking_workshop
  ```

After activation, your prompt will change to show the environment name, for example:

```bash
(molecular_docking_workshop) your-computer:Basic-Molecular-Docking-Workshop yourname$
```

---

## Step 5: Activate the Environment

Before using any workshop tools, you must "activate" the environment:

* **All operating systems**:

  ```bash
  conda activate molecular_docking_workshop
  ```

After activation, your prompt will change to show the environment name, for example:

```bash
(molecular_docking_workshop) your-computer:Basic-Molecular-Docking-Workshop yourname$
```

### Additional Setup: Install Meeko and ProDy

Once the environment is active, install the **Meeko** package and **ProDy**:

```bash
# Clone the Meeko repository and navigate to the Meeko folder
git clone https://github.com/forlilab/Meeko.git
cd Meeko
```

```bash
# Switch to the development branch
git checkout develop
```

```bash
# Install Meeko in editable mode
pip install .
```

```bash
# Install ProDy
pip install prody
```

```bash
# Return to the workshop root folder
cd ..
```

---

## Step 6: Verify Your Setup

With the environment active, check that key programs are available:

```bash
which vina      # Should print a path to the "vina" executable
which reduce    # Should print a path to the "reduce" executable
python --version  # Should print Python 3.10.x
```

If these commands return paths and versions without errors, you’re all set!

---

## Using the `pdbqt2pdb.sh` Script

We provide a script to convert `.pdbqt` files into individual `.pdb` files.

1. Make the script executable (only needed once):

   ```bash
   chmod +x pdbqt2pdb.sh
   ```

2. Run the script on a `.pdbqt` file:

   ```bash
   ./pdbqt2pdb.sh my_structure.pdbqt
   ```

   * The script splits each `MODEL` into its own file and converts them to `.pdb` format.
   * You’ll see output like:

     ```
     → Converted to my_structure_model1.pdb and removed my_structure_model1.pdbqt
     ```

---

## Troubleshooting

* **"Command not found" errors**: Make sure you have activated the environment with `conda activate molecular_docking_workshop`.
* **Permission denied** when running the script: Ensure you ran `chmod +x pdbqt2pdb.sh`.
* If you get stuck at any step, feel free to ask for help or check online resources for Conda and Git.

---

## Acknowledgments

This workshop uses open-source tools including:

* [RDKit](https://www.rdkit.org/)
* [AutoDock Vina](http://vina.scripps.edu/)
* [Biopython, Gemmi, SciPy](https://www.scipy.org/)

Enjoy learning molecular docking!
