import time
from typing import List, Tuple

from matrices import *
from weapon import *


def simulate_ranik(sims: int, weapons: List[Weapon], curse_percentage=0.0, num_attacks=1):
    ability = 3
    proficiency = 2
    _results = []

    print(f"Raniks curse uptime: {curse_percentage:.0%}")

    for weapon in weapons:
        _attack_total = 0
        _damage_total = 0
        _num_crits = 0
        weapon_results = []

        for _ in range(sims):
            for __ in range(num_attacks):
                crit = False
                attack = random.randint(1, 20)
                _attack = attack + ability + proficiency + weapon.atk_mod()

                if random.random() < curse_percentage:
                    if attack >= 19:
                        crit = True
                        _num_crits += 1
                    _damage = weapon.damage_roll(crit) + ability + proficiency  # pact weapon + cursed target add prof to dmg
                else:
                    if attack >= 20:
                        crit = True
                        _num_crits += 1
                    _damage = weapon.damage_roll(crit) + ability  # pact weapon

                weapon_results.append((_attack, _damage, crit))
                _attack_total += _attack
                _damage_total += _damage

        _results.append((weapon, pd.DataFrame.from_records(weapon_results, columns=['attack', 'damage', 'crit'])))

    return _results


def simulate_solas(sims: int, weapons: List[Weapon], num_attacks: int = 1) -> List[Tuple[Weapon, pd.DataFrame]]:
    ability = 2
    proficiency = 2
    other_dmg = 2
    _results = []

    for weapon in weapons:
        _attack_total = 0
        _damage_total = 0
        _num_crits = 0
        weapon_results = []

        for _ in range(sims):
            for __ in range(num_attacks):
                crit = False

                attack_roll = random.randint(1, 20)
                _attack = attack_roll + ability + proficiency + weapon.atk_mod()
                if attack_roll >= 20:
                    crit = True
                    _num_crits += 1
                _damage = weapon.damage_roll(crit) + ability + other_dmg

                weapon_results.append((_attack, _damage, crit))
                _attack_total += _attack
                _damage_total += _damage

        _results.append((weapon, pd.DataFrame.from_records(weapon_results, columns=['attack', 'damage', 'crit'])))

    return _results


def simulate_daruth(sims: int, weapons: List[Weapon], num_attacks=1):
    ability = 4
    proficiency = 2
    _results = []

    for weapon in weapons:
        _attack_total = 0
        _damage_total = 0
        _num_crits = 0
        weapon_results = []

        for _ in range(sims):
            for __ in range(num_attacks):
                crit = False
                attack_roll = random.randint(1, 20)
                _attack = attack_roll + ability + proficiency + weapon.atk_mod()

                if attack_roll >= 20:
                    crit = True
                    _num_crits += 1
                _damage = weapon.damage_roll(crit) + ability

                weapon_results.append((_attack, _damage, crit))
                _attack_total += _attack
                _damage_total += _damage

        _results.append((weapon, pd.DataFrame.from_records(weapon_results, columns=['attack', 'damage', 'crit'])))

    return _results

HEADER = "{0:45}{1:>10}{2:>10}{3:>10}".format(f"Name", "Attack", "Damage", "Crit %")
TEMPLATE = "{0:45}{1:>10.1f}{2:>10.1f}{3:>10.1%}"


def print_results(name, attacks, damage, crits):
    print(TEMPLATE.format(name, attacks, damage, crits))


if __name__ == "__main__":
    start = time.perf_counter()
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
    num_attacks = 1
    results = simulate_ranik(SIMS, raniks_weapons, curse_percentage=0.4)
    for weapon, result in results:
        print_results(f"Ranik's {weapon}", result['attack'].mean(), result['damage'].mean(),
                      result['crit'].sum() / (SIMS * num_attacks))
        # show_matrices(result)

    solas_weapons = [
        longsword,
        flametongue
    ]
    num_attacks = 1
    results = simulate_solas(SIMS, solas_weapons, num_attacks)
    for weapon, result in results:
        print_results(f"Solas' {weapon}", result['attack'].mean(), result['damage'].mean(), result['crit'].sum() / (SIMS * num_attacks))
        # show_matrices(result)

    daruths_weapons = [
        monk_hand
    ]
    num_attacks = 1
    results = simulate_daruth(SIMS, daruths_weapons)
    for weapon, result in results:
        print_results(f"Daruth's {weapon}", result['attack'].mean(), result['damage'].mean(), result['crit'].sum() / (SIMS * num_attacks))
        # show_matrices(result)

    print(f"Time: {time.perf_counter()-start:.1f}s")
