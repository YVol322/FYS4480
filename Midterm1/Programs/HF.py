import numpy as np 
import matplotlib.pyplot as plt
from classes import System, Coulumb_integrals

class HarteeFock:


    """
        Initialize the Hartree-Fock solver.

        Parameters:
        system (System): The quantum system generated by the System class.
        matrix (Coulumb_integrals): Coulomb integrals matrix containing interaction elements.
        Z (int): The atomic number.
        n_parts (int): The number of particles in the system.
        n_states (int): The number of single-particle states in the system.
        max_iterations (int): Maximum number of Hartree-Fock iterations.
        tolerance (float): Convergence criterion for the iterative solver.
    """
    def __init__(self, system, matrix, Z, n_parts, n_states, max_iterations, tolerance):

        # Initializing Hartree-Fock class variables
        self.system = system  # Quantum system from the System class
        self.matrix = matrix  # Coulomb integrals matrix
        self.Z = Z  # Atomic number
        self.n_parts = n_parts  # Number of particles
        self.n_states = n_states  # Number of single-particle states
        self.max_iterations = max_iterations  # Maximum number of iterations allowed
        self.tolerance = tolerance  # Convergence tolerance
        # Generate all possible single-particle states with spin
        self.SPS = [(i, spin) for i in range(system.max_index) for spin in (0.5, -0.5)]  
        self.energies = []  # To track energy convergence over iterations

    

    """
        Compute the density matrix from the coefficient matrix C.

        Parameters:
        C (numpy.ndarray): Coefficient matrix of size (n_parts, n_states).
        
        Returns:
        numpy.ndarray: Density matrix of shape (n_states, n_states).
    """
    def density_matrix(self, C):
        rho = np.zeros(C.shape)  # Adjust shape accordingly.

        for n in range(self.n_states):
            for m in range(self.n_states):
                temp = 0
                for l in range(self.n_parts):
                    temp += np.conjugate(C[l, n]) * C[l, m]  # Sum over particles using conjugate coefficients
                rho[n, m] = temp

        return rho


    """
        Compute the ground state energy using the density matrix.

        Parameters:
        rho (numpy.ndarray): The density matrix.
        
        Updates:
        self.E (float): Stores the computed ground state energy.
    """
    def ground_state_energy(self, rho):
        # Calculate one-body energy contribution
        temp = sum(rho[ii, ii] * self.matrix.one_body(i) for ii, i in enumerate(self.SPS))
    
        # Calculate two-body energy contribution
        temp += sum(
            0.5 * rho[ii, kk] * rho[jj, ll] * self.matrix.two_body(i, j, k, l)
            for ii, i in enumerate(self.SPS)
            for jj, j in enumerate(self.SPS)
            for kk, k in enumerate(self.SPS)
            for ll, l in enumerate(self.SPS)
        )
    
        self.E = temp  # Store the calculated energy

    

    """
        Construct the Hartree-Fock matrix using the density matrix.

        Parameters:
        rho (numpy.ndarray): The density matrix.
        
        Returns:
        numpy.ndarray: The Hartree-Fock matrix.
    """
    def HF_matrix(self, rho):
        HF_mat = np.zeros(rho.shape)
    
        # Add one-body matrix elements
        for ii, i in enumerate(self.SPS):
            HF_mat[ii, ii] = self.matrix.one_body(i)
    
        # Add two-body matrix elements (interaction terms)
        for ii, i in enumerate(self.SPS):
            for jj, j in enumerate(self.SPS):
                HF_mat[ii, jj] += sum(
                    rho[kk, ll] * self.matrix.two_body(i, k, j, l)
                    for kk, k in enumerate(self.SPS)
                    for ll, l in enumerate(self.SPS)
                )
    
        return HF_mat



    """
        Perform the iterative Hartree-Fock calculation to determine the ground-state energy.
    """
    def HF_iteration(self):
        C = np.eye(self.n_states)  # Initialize coefficient matrix as identity
        rho = self.density_matrix(C)  # Initial density matrix
        previous_eigenvalues = None  # To track eigenvalue convergence

        for i in range(self.max_iterations):
            HF = self.HF_matrix(rho)  # Construct the Hartree-Fock matrix

            # Solve for eigenvalues and eigenvectors (coefficients)
            E, C = np.linalg.eigh(HF)

            # Check for convergence based on the difference in eigenvalues
            if previous_eigenvalues is not None:
                eigenvalue_diff = np.max(np.abs(E - previous_eigenvalues))
                if eigenvalue_diff < self.tolerance:
                    print(f"Converged after {i+1} iterations.")
                    break

            previous_eigenvalues = E  # Update the previous eigenvalues for the next iteration

            # Update the density matrix and compute the ground-state energy
            rho = self.density_matrix(C.T)  
            self.ground_state_energy(rho)
            self.energies.append(self.E)  # Store energy at every iteration



if __name__ == '__main__':
    

    """
        Execute the Hartree-Fock algorithm for a given atomic number and particle count.

        Parameters:
        Z (int): Atomic number.
        parts (int): Number of electrons/particles.
        fermi_index (int): The Fermi level index. Defaults to 0.
        max_index (int): Maximum index of quantum states. Defaults to 3.
        n_states (int): Number of single-particle states. Defaults to 3.
        
        Returns:
        float: Minimum ground-state energy found during iterations.
        list: History of energy values at each iteration.
    """
    def HF_algo(Z, parts, fermi_index=0, max_index=3, n_states=3):
        system = System(fermi_index, max_index) # Initialize the system
        integrs_matrix = Coulumb_integrals(Z, n_states, system) # Compute 4d interaction matrix

        solver = HarteeFock(system, integrs_matrix, Z, parts, 6, 
                             max_iterations=100, tolerance=1e-14)  # Create the Hartree-Fock solver

        # Perform the Hartree-Fock calculation
        solver.HF_iteration()

        # Return the minimum energy and the energy history
        return np.min(solver.energies), solver.energies


    """
        Solve the Hartree-Fock equations for multiple atoms.

        Parameters:
        atoms (list): A list of dictionaries, each representing an atom with 
                      'name', 'Z' (atomic number), 'n_electrons', and 'Fermi_index'.
    """
    def solve_multiple_atoms(atoms):
        for atom in atoms:
            eigenvalue, list = HF_algo(atom['Z'], atom['n_electrons'], atom['Fermi_index'])

            print(f"1st iteration {atom['name']} ground state energy: {list[0]:.4f}")
            print("\n")
            print(f"converged {atom['name']} ground state energy =  {eigenvalue:.4f}")
            print("\n")

    # Helium and Beryllium atom tuples
    atoms = [
        {"name": "He", "Z": 2, "n_electrons": 2, "Fermi_index": 0},
        {"name": "Be", "Z": 4, "n_electrons": 4, "Fermi_index": 1}
    ]

    # Solve for He and Be
    solve_multiple_atoms(atoms)