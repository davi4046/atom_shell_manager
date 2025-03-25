SUBSHELLS_BY_ENERGY = [
    (1, "s"),
    (2, "s"),
    (2, "p"),
    (3, "s"),
    (3, "p"),
    (4, "s"),
    (3, "d"),
    (4, "p"),
    (5, "s"),
    (4, "d"),
    (5, "p"),
    (6, "s"),
    (4, "f"),
    (5, "d"),
    (6, "p"),
    (7, "s"),
    (5, "f"),
    (6, "d"),
    (7, "p"),
]

SUBSHELL_TYPE_MAX_ELECTRONS = {"s": 2, "p": 6, "d": 10, "f": 14}


class AtomShellManager:
    def __init__(self, initial_electrons: int):
        self.subshells = {}
        for _ in range(initial_electrons):
            self.add_electron()

    def add_electron(self):
        for subshell in SUBSHELLS_BY_ENERGY:
            electrons = self.subshells.get(subshell, 0)
            if electrons < SUBSHELL_TYPE_MAX_ELECTRONS[subshell[1]]:
                self.subshells[subshell] = electrons + 1
                self.__apply_d_orbital_stability()
                break

    def remove_electron(self):
        for subshell in reversed(SUBSHELLS_BY_ENERGY):
            electrons = self.subshells.get(subshell, 0)
            if electrons > 0:
                self.subshells[subshell] = electrons - 1
                self.__apply_d_orbital_stability()
                break

    def get_valence_electrons_by_subshell(self) -> dict:
        last_populated_subshell = None

        for subshell in reversed(SUBSHELLS_BY_ENERGY):
            electrons = self.subshells.get(subshell, 0)
            if electrons > 0:
                last_populated_subshell = subshell
                break

        start_energy_index = 0

        for shell_index in range(7, 0, -1):
            if (shell_index, "p") == last_populated_subshell:
                continue

            s_electrons = self.subshells.get((shell_index, "s"), 0)
            p_electrons = self.subshells.get((shell_index, "p"), 0)

            s_is_full = s_electrons == SUBSHELL_TYPE_MAX_ELECTRONS["s"]
            p_is_full = p_electrons == SUBSHELL_TYPE_MAX_ELECTRONS["p"]

            if s_is_full and p_is_full:
                start_energy_index = SUBSHELLS_BY_ENERGY.index((shell_index, "p")) + 1
                break

        if start_energy_index == 0 and (1, "s") != last_populated_subshell:
            start_energy_index = 1

        result = {}

        for subshell in SUBSHELLS_BY_ENERGY[start_energy_index:]:
            if subshell[1] in ["d", "f"] and subshell != last_populated_subshell:
                continue
            if subshell in self.subshells:
                result[subshell] = self.subshells[subshell]

        return result

    def count_valence_electrons(self) -> int:
        return sum(self.get_valence_electrons_by_subshell().values())

    def __apply_d_orbital_stability(self):
        outer_shell_index = max(subshell[0] for subshell in self.subshells)

        if outer_shell_index < 2:
            return

        s_subshell = (outer_shell_index, "s")
        d_subshell = (outer_shell_index - 1, "d")

        if not s_subshell in self.subshells or not d_subshell in self.subshells:
            return

        s_electrons = self.subshells[s_subshell]
        d_electrons = self.subshells[d_subshell]

        if s_electrons > 0 and (d_electrons == 4 or d_electrons == 9):
            self.subshells[s_subshell] -= 1
            self.subshells[d_subshell] += 1
