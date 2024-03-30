import random
import re

from typing import List

DIE_PATTERN = re.compile(r"(\d)+d(\d+)([+-]\d+)?", re.IGNORECASE)


def parse_dice(dmg: str) -> (int, int, int):
    dmg = "".join(dmg.split())
    parts = re.fullmatch(DIE_PATTERN, dmg)
    if not parts:
        raise ValueError

    num_roll = int(parts[1])
    die = int(parts[2])
    modifier = 0 if parts.lastindex == 2 else int(parts[3])

    return num_roll, die, modifier


class Weapon:

    @staticmethod
    def roll(num: int, die: int, crit: bool) -> int:
        damage = 0
        for _ in range(num):
            damage += random.randint(1, die)
            if crit:
                damage += random.randint(1, die)
        return damage

    def damage_roll(self, crit: bool = False) -> int:
        raise NotImplementedError

    def atk_mod(self) -> int:
        raise NotImplementedError

    def __str__(self) -> str:
        raise NotImplementedError


class FlatDamageWeapon(Weapon):

    def __init__(self, name: str, dmg: int):
        self.name = name
        self.dmg = dmg

    def damage_roll(self, crit=False):
        return self.dmg if not crit else self.dmg * 2

    def atk_mod(self) -> int:
        return 0

    def __repr__(self):
        return f"FlatDamageWeapon({self.name}, {self.dmg}"

    def __str__(self):
        return f"{self.name} ({self.dmg} flat)"


class SimpleWeapon(Weapon):
    @staticmethod
    def from_dice(name, damage: str, extra_dmg: str = None) -> Weapon:
        rolls, die, mod = parse_dice(damage)
        extra = parse_dice(extra_dmg) if extra_dmg else (0, 0, 0)
        return SimpleWeapon(name, rolls, die, mod, mod, *extra)

    @staticmethod
    def roll(num, die, crit):
        damage = 0
        for _ in range(num):
            damage += random.randint(1, die)
            if crit:
                damage += random.randint(1, die)
        return damage

    def __init__(self, name, num_rolls, die, atk_modifier=0, dmg_modifier=0,
                 xtra_num_rolls=0, xtra_die=0, xtra_dmg_modifier=0):
        self.name = name
        self.num_rolls = num_rolls
        self.die = die
        self.atk_modifier = atk_modifier
        self.dmg_modifier = dmg_modifier
        self.xtra_num_rolls = xtra_num_rolls
        self.xtra_die = xtra_die
        self.xtra_dmg_modifier = xtra_dmg_modifier

    def damage_roll(self, crit=False):
        damage = Weapon.roll(self.num_rolls, self.die, crit) + self.dmg_modifier

        if self.xtra_die:
            damage += Weapon.roll(self.xtra_num_rolls, self.xtra_die, crit) + self.xtra_dmg_modifier

        return damage

    def atk_mod(self) -> int:
        return self.atk_modifier

    def __str__(self):
        mod = ""

        if self.atk_modifier == self.dmg_modifier and self.atk_modifier != 0:
            mod = f'+{self.atk_modifier}'
        elif self.atk_modifier != self.dmg_modifier:
            mod = f', atk: {self.atk_modifier}, dmg: {self.dmg_modifier}'

        xtra = ""
        if self.xtra_die:
            xtra_mod = ""
            if self.xtra_dmg_modifier != 0:
                xtra_mod = f'+{self.xtra_dmg_modifier}'
            xtra = f" + ({self.xtra_num_rolls}d{self.xtra_die}{xtra_mod})"

        return f"{self.name} ({self.num_rolls}d{self.die}{mod}){xtra}"


def simulate_ranik(sims: int, weapons: List[Weapon], curse_percentage=0.0, num_attacks=1):
    ability = 3
    proficiency = 2
    print(f"Raniks curse uptime: {curse_percentage:.0%}")

    for weapon in weapons:
        _attack_total = 0
        _damage_total = 0
        _num_crits = 0
        for _ in range(sims):
            for __ in range(num_attacks):
                crit = False
                attack = random.randint(1, 20)
                _attack_total += attack + ability + proficiency + weapon.atk_mod()

                if random.random() < curse_percentage:
                    if attack >= 19:
                        crit = True
                        _num_crits += 1
                    _damage_total += weapon.damage_roll(
                        crit) + ability + proficiency  # pact weapon + cursed target add prof to dmg
                else:
                    if attack >= 20:
                        crit = True
                        _num_crits += 1
                    _damage_total += weapon.damage_roll(crit) + ability  # pact weapon

        print_results(f"Ranik's {weapon}", _attack_total / (sims * num_attacks), _damage_total / sims,
                      _num_crits / (sims * num_attacks))


def simulate_solas(sims: int, weapons: List[Weapon], num_attacks: int = 1):
    ability = 2
    proficiency = 2
    other_dmg = 2

    for weapon in weapons:
        _attack_total = 0
        _damage_total = 0
        _num_crits = 0

        for _ in range(sims):
            for __ in range(num_attacks):
                crit = False
                attack = random.randint(1, 20)
                _attack_total += attack + ability + proficiency + weapon.atk_mod()

                if attack >= 20:
                    crit = True
                    _num_crits += 1
                _damage_total += weapon.damage_roll(crit) + ability + other_dmg

        print_results(f"Solas' {weapon}", _attack_total / (sims * num_attacks), _damage_total / sims,
                      _num_crits / (sims * num_attacks))


def simulate_daruth(sims: int, weapons: List[Weapon], num_attacks=1):
    ability = 4
    proficiency = 2

    for weapon in weapons:
        _attack_total = 0
        _damage_total = 0
        _num_crits = 0
        for _ in range(sims):
            for __ in range(num_attacks):
                crit = False
                attack = random.randint(1, 20)
                _attack_total += attack + ability + proficiency + weapon.atk_mod()

                if attack >= 20:
                    crit = True
                    _num_crits += 1
                _damage_total += weapon.damage_roll(crit) + ability

        print_results(f"Daruth's {weapon}", _attack_total / (sims * num_attacks), _damage_total / sims,
                      _num_crits / (sims * num_attacks))


HEADER = "{0:45}{1:>10}{2:>10}{3:>10}".format(f"Name", "Attack", "Damage", "Crit %")
TEMPLATE = "{0:45}{1:>10.1f}{2:>10.1f}{3:>10.1%}"


def print_results(name, attacks, damage, crits):
    print(TEMPLATE.format(name, attacks, damage, crits))


if __name__ == "__main__":
    SIMS = 100_000
    print(f"{SIMS} sims")
    print(HEADER)

    battleaxe = SimpleWeapon("battleaxe", num_rolls=1, die=8, dmg_modifier=1)
    battleaxe_2h = SimpleWeapon("battleaxe (2h)", num_rolls=1, die=10, dmg_modifier=1)
    flametongue = SimpleWeapon.from_dice("flametongue(?) scimitar", "1d6", "2d6")
    longsword = SimpleWeapon.from_dice("longsword", "1d8")
    monk_hand = SimpleWeapon.from_dice("monk hands", "1d6")

    raniks_weapons = [
        battleaxe,
        battleaxe_2h,
        flametongue
    ]
    simulate_ranik(SIMS, raniks_weapons, curse_percentage=0.4)

    solas_weapons = [
        longsword,
        flametongue
    ]
    simulate_solas(SIMS, solas_weapons)

    daruths_weapons = [
        monk_hand
    ]
    simulate_daruth(SIMS, daruths_weapons)
