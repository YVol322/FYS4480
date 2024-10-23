import numpy as np 



class System:

    """
        Initialize the System object with the Fermi level and maximum level index.
        
        Parameters:
        Fermi_level_index (int): The index representing the Fermi level.
        Max_index (int): The maximum index for the system's states.
    """
    def __init__(self, Fermi_level_index, Max_index):
        self.set_Fermi_level(Fermi_level_index, Max_index)


    """
        Set the Fermi level and the maximum level index for the system.

        Parameters:
        fermi_index (int): The index representing the Fermi level.
        max_index (int): The maximum index for the system's states.
        """
    def set_Fermi_level(self, fermi_index, max_index):
        self.fermi_index = fermi_index
        self.max_index = max_index


    """
        Yield states that are below the Fermi level.
        
        Yields:
        tuple: (state_index, spin), where spin is either 0.5 (up) or -0.5 (down).
    """
    def below_Fermi(self):
        for i in range(self.fermi_index + 1):
            yield i, 0.5 # Spin-up state
            yield i, -0.5 # Spin-down state


    """
        Yield states that are above the Fermi level.
        
        Yields:
        tuple: (state_index, spin), where spin is either 0.5 (up) or -0.5 (down).
        """
    def above_Fermi(self):
        for i in range(self.fermi_index + 1, self.max_index):
            yield i, 0.5
            yield i, -0.5


class Coulumb_integrals:


    """
        Initialize the Coulomb_integrals object.

        Parameters:
        Z (int): The atomic number.
        Nstates (int): The number of quantum states in the system.
        system (System): An instance of the System class.
    """
    def __init__(self, Z, Nstates, system):
        self.Z = Z
        self.states = Nstates
        self.mat = np.zeros((Nstates, Nstates, Nstates, Nstates))  # 4D interaction matrix
        self.values = {}
        self._read_values_and_fill_matrix()
    

    """
        Read matrix elements from a file and fill the interaction matrix.
        The values are based on the atomic number.
    """
    def _read_values_and_fill_matrix(self):
        with open('../Matirx_elements_table/Matrix_elements.txt', 'r') as f:
            for line in f:
                key, value = line.strip().split('=')
                key = key.strip()

                # Evaluate the value string, replacing symbols with Python/numpy syntax
                value = eval(value.replace('Z', str(self.Z))
                             .replace('Sqrt', 'np.sqrt')
                             .replace('[', '(').replace(']', ')').strip())

                bra, ket = key.split('V') # Split the matrix element key into bra and ket
                i, j = int(bra[1])-1, int(bra[2])-1
                k, l = int(ket[1])-1, int(ket[2])-1

                # Store the evaluated value into the 4D matrix and the dictionary
                self.mat[i, j, k, l] = value
                self.values[key] = value  # Store values
    

    """
        Calculate the one-body energy of a quantum state.
        
        Parameters:
        state (tuple): A tuple representing the quantum state (n, spin).
        
        Returns:
        float: The one-body energy of the state.
    """
    def one_body(self, state):
        n = state[0] + 1  # Quantum number n (starts at 1)
        return -(self.Z * self.Z) / (2 * n*n) # Hydrogen-like one-body energy
    

    """
        Calculate the two-body Coulomb integral based on quantum state indices and spins.

        Parameters:
        i (tuple): Quantum state (index, spin) for the first particle.
        j (tuple): Quantum state (index, spin) for the second particle.
        k (tuple): Quantum state (index, spin) for the third particle.
        l (tuple): Quantum state (index, spin) for the fourth particle.

        Returns:
        float: The value of the two-body Coulomb integral, considering spin conservation.
        """
    def two_body(self, i, j, k, l):
        # Check for spin conservation
        spin1 = (i[1] == k[1]) and (j[1] == l[1])  # Spin conservation for the first configuration
        spin2 = (i[1] == l[1]) and (j[1] == k[1])  # Spin conservation for the second configuration

        # Return the AS matrix elements
        return spin1 * self.mat[i[0], j[0], k[0], l[0]] - spin2 * self.mat[i[0], j[0], l[0], k[0]]