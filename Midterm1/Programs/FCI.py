import numpy as np


# analytically computed 1p1h hamiltonian matrix for helium atom (Z = 2)
H2 = np.array([[-2.75, 0.1787, 0.1787, 0.0879, 0.0879],
             [0.1787, -1.6259, 0.0439, -0.0787, 0.0224],
             [0.1787, 0.0439, -1.6259, 0.0224, -0.0787],
             [0.0879, -0.0787, 0.0224, -1.1597, 0.0115],
             [0.0879, 0.0224, -0.0787, 0.0115, -1.1597]])


# analytically computed 1p1h hamiltonian matrix for beryllium atom (Z = 4)
H4 = np.array([[-13.716, 0.189, 0.189, 0.445, 0.445],
             [0.189, -6.980, 0.023, -0.002, 0.008],
             [0.189, 0.023, -6.980, 0.008, -0.002],
             [0.445, -0.002, 0.008, -12.575, 0.030],
             [0.445, 0.008, -0.002, 0.030, -12.575]])


# using numpy to solve eigenvalue problem for th given matrices. Minimal eigenvalue is the FCI ground state energy
He_eigenvalues, He_eigenvectors = np.linalg.eig(H2)
Be_eigenvalues, Be_eigenvectors = np.linalg.eig(H4)


print(f"FCI ground state energy for He atom = {np.min(He_eigenvalues)}")
print(f"FCI ground state energy for Be atom = {np.min(Be_eigenvalues)}")