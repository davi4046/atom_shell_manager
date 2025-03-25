from atom_shell_manager import AtomShellManager
from elements import ELEMENTS


for i in range(0, 118):
    shell_manager = AtomShellManager(i + 1)
    print(f"{ELEMENTS[i]}: {shell_manager.count_valence_electrons()} valence electrons")
