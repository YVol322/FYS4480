import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# Create the figures PNG and PDF directories if it does not exist
Path("Figures").mkdir(exist_ok=True)
Path("Figures/PNG").mkdir(parents=True, exist_ok=True)
Path("Figures/PDF").mkdir(parents=True, exist_ok=True)

# Define the range of g values
g_values = np.linspace(-1, 1, 1000)

# Lists to store the eigenvalues
eigenvalues_listFCI = []
eigenvalues_listCI = []
eigenvalues_listHF = []
eigenvalues_listRSPT3 = []
eigenvalues_listRSPT2 = []
eigenvalues_listRSPT4 = []

# Loop over the values of g
for g in g_values:
    # Create FCI Hamiltonian matrix
    FCI = np.array([
        [2 - g, -g/2, -g/2, -g/2, -g/2, 0],
        [-g/2, 4 - g, -g/2, -g/2, 0, -g/2],
        [-g/2, -g/2, 6 - g, 0, -g/2, -g/2],
        [-g/2, -g/2, 0, 6 - g, -g/2, -g/2],
        [-g/2, 0, -g/2, -g/2, 8 - g, -g/2],
        [0, -g/2, -g/2, -g/2, -g/2, 10 - g]
    ])

    # Create CI Hamiltonian matrix
    CI = np.array([
        [2 - g, -g/2, -g/2, -g/2, -g/2],
        [-g/2, 4 - g, -g/2, -g/2, 0],
        [-g/2, -g/2, 6 - g, 0, -g/2],
        [-g/2, -g/2, 0, 6 - g, -g/2],
        [-g/2, 0, -g/2, -g/2, 10 - g],
    ])
    
    # Calculate the eigenvalues
    eigenvaluesFCI, _ = np.linalg.eig(FCI)
    eigenvaluesCI, _ = np.linalg.eig(CI)
    
    # Collect the eigenvalues for plotting
    eigenvalues_listFCI.append(eigenvaluesFCI)
    eigenvalues_listCI.append(eigenvaluesCI)
    eigenvalues_listHF.append(2-g)
    eigenvalues_listRSPT3.append(2-g - 7/24 * g*g - 1/12*g*g*g)
    eigenvalues_listRSPT2.append(2-g - 7/24 * g*g)
    eigenvalues_listRSPT4.append(2-g - 7/24 * g*g - 1/12*g*g*g - 0.179*g*g*g*g)


# Convert the list one of eigenvalues into a numpy array for easier indexing and sort FCI and CI ones
eigenvalues_arrayFCI = np.array(eigenvalues_listFCI)
eigenvalues_arrayFCI = np.sort(eigenvalues_arrayFCI)

eigenvalues_arrayCI = np.array(eigenvalues_listCI)
eigenvalues_arrayCI = np.sort(eigenvalues_arrayCI)


eigenvalues_arrayHF = np.array(eigenvalues_listHF)
eigenvalues_arrayRSPT3 = np.array(eigenvalues_listRSPT3)
eigenvalues_arrayRSPT2 = np.array(eigenvalues_listRSPT2)
eigenvalues_arrayRSPT4 = np.array(eigenvalues_listRSPT4)

GS_FCI = eigenvalues_arrayFCI[:, 0]  # FCI ground state
GS_CI = eigenvalues_arrayCI[:, 0]  # FCI ground state



# Plot for all FCI eigenvalues
plt.figure(figsize=(10, 6))
plt.style.use('ggplot')
for i in range(eigenvalues_arrayFCI.shape[1]):
    plt.plot(g_values, eigenvalues_arrayFCI[:, i], label=f'Eigenvalue {i}')
plt.style.use('ggplot')
plt.xlabel('g')
plt.ylabel(r'Energy $\epsilon$')
plt.legend()
plt.grid(True)
plt.savefig('figures/PDF/FCI.pdf')


# Plot for all CI eigenvalues
plt.figure(figsize=(10, 6))
for i in range(eigenvalues_arrayCI.shape[1]):
    plt.plot(g_values, eigenvalues_arrayCI[:, i], label=f'Eigenvalue {i}', linewidth=2)
plt.style.use('ggplot')
plt.xlabel('g')
plt.ylabel(r'Energy $\epsilon$')
plt.legend()
plt.grid(True)
plt.savefig('figures/PDF/CI.pdf')
plt.savefig('figures/PNG/CI.png')


# Plot for FCI ground state energy
plt.figure(figsize=(10, 6))
plt.plot(g_values, GS_FCI, label="FCI Ground State", color = 'k', linewidth=2)
plt.xlabel(r"$g$", fontsize=12)
plt.ylabel(r"Ground State Energy $\epsilon_0$", fontsize=12)
plt.legend(fontsize=12)
plt.grid(True, linestyle="--", alpha=0.7)
plt.tight_layout()
plt.savefig('figures/PDF/FCI0.pdf')
plt.savefig('figures/PNG/FCI0.png')


# Plot for FCI and CI ground state energies
plt.figure(figsize=(10, 6))
plt.plot(g_values, GS_FCI, label="FCI Ground State", linestyle = 'dashed', color = 'k', linewidth=2)
plt.plot(g_values, GS_CI, label="CI Ground State", linewidth=2)
plt.xlabel(r"$g$", fontsize=12)
plt.ylabel(r"Ground State Energy $\epsilon_0$", fontsize=12)
plt.legend(fontsize=12)
plt.grid(True, linestyle="--", alpha=0.7)
plt.tight_layout()
plt.savefig('figures/PDF/CIFCI.pdf')
plt.savefig('figures/PNG/CIFCI.png')


# Plot for FCI, CI and HF ground state energies
plt.figure(figsize=(10, 6))
plt.plot(g_values, GS_FCI, label="FCI Ground State", linestyle = 'dashed', color = 'k', linewidth=2)
plt.plot(g_values, GS_CI, label="CI Ground State", linewidth=2)
plt.plot(g_values, eigenvalues_arrayHF, label="HF Ground State", linewidth=2)
plt.xlabel(r"$g$", fontsize=12)
plt.ylabel(r"Ground State Energy $\epsilon_0$", fontsize=12)
plt.legend(fontsize=12)
plt.grid(True, linestyle="--", alpha=0.7)
plt.tight_layout()
plt.savefig('figures/PDF/HF.pdf')
plt.savefig('figures/PNG/HF.png')


# Plot for FCI and RSPT3 ground state energies
plt.figure(figsize=(10, 6))
plt.plot(g_values, GS_FCI, label="FCI Ground State", linestyle = 'dashed', color = 'k', linewidth=2)
plt.plot(g_values, eigenvalues_arrayRSPT3, label="RSPT3 Ground State", linewidth=2)
plt.xlabel(r"$g$", fontsize=12)
plt.ylabel(r"Ground State Energy $\epsilon_0$", fontsize=12)
plt.legend(fontsize=12)
plt.grid(True, linestyle="--", alpha=0.7)
plt.tight_layout()
plt.savefig('figures/PDF/RSPT3.pdf')
plt.savefig('figures/PDF/RSPT3.pdf')


# Plot for FCI and RSPT2 ground state energies
plt.figure(figsize=(10, 6))
plt.plot(g_values, GS_FCI, label="FCI Ground State", linestyle = 'dashed', color = 'k', linewidth=2)
plt.plot(g_values, eigenvalues_arrayRSPT2, label="RSPT2 Ground State", linewidth=2)
plt.xlabel(r"$g$", fontsize=12)
plt.ylabel(r"Ground State Energy $\epsilon_0$", fontsize=12)
plt.legend(fontsize=12)
plt.grid(True, linestyle="--", alpha=0.7)
plt.tight_layout()
plt.savefig('figures/PDF/RSPT2.pdf')
plt.savefig('figures/PNG/RSPT2.png')



# Plot for FCI and RSPT4 ground state energies
plt.figure(figsize=(10, 6))
plt.plot(g_values, GS_FCI, label="FCI Ground State", linestyle = 'dashed', color = 'k', linewidth=2)
plt.plot(g_values, eigenvalues_arrayRSPT4, label="RSPT4 Ground State", linewidth=2)
plt.xlabel(r"$g$", fontsize=12)
plt.ylabel(r"Ground State Energy $\epsilon_0$", fontsize=12)
plt.legend(fontsize=12)
plt.grid(True, linestyle="--", alpha=0.7)
plt.tight_layout()
plt.savefig('figures/PDF/RSPT4.pdf')
plt.savefig('figures/PNG/RSPT4.png')
#plt.show()