# Midterm 1 Repository

This repository contains programs and matrix element data for calculating the ground-state energy of atoms using Full Configuration Interaction (FCI) theory and Hartree-Fock (HF) theory.

## Contents

- **FCI.py**  
  This program implements the FCI algorithm to calculate the ground-state energy. The Hamiltonian matrix for the FCI method is pre-calculated analytically, allowing the program to simply diagonalize the matrices for helium and beryllium atoms and output their ground-state energies.
  
- **HF.py**  
  This program implements an object-oriented HF algorithm for ground-state energy calculation. It reads data from the file `Matrix_elements_table/Matrix_elements.txt`, which contains the necessary matrix elements for the calculations.

## Author

Yevhenii Volkov
