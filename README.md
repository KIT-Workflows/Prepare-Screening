# DFT-Turbomole

## Description

With this Wano, the user can choose one several molecules for a subsequent screening of properties.

## Server setup

The code is based on python and the necessary virtual environment on the server is provided by Simstack. In addition, a configuration file called ```marvin.config``` needs to be provided in ```$NANOMATCH/$NANOVER/configs``` on the server in order to provide access to the Marvin Suite.

## Required input

The required input consists of at least one molecule which can provided in different formats (see below)

## WaNo Settings

- **Molecules input**  
Either a single molecule or a list of molecules can be chosen for (all of) which Gaussian input files are written out. If 'List of Smiles with charge/multiplicity' is chosen in 'multiple molecules' mode, a file containing one line per molecule with space-separated SMILES code, charge and multiplicity must be provided.

- **Calculation of spectra**  
Choose which type of spectra are to be calculated in the workflow.

## Output

The output of this WaNo consists of Gaussian-type input files (```*.inp```) for all molecules.
