import time

from matrices import *
from weapon import *


def simulate_ranik(sims: int, ability: int, proficiency: int, weapons: List[Weapon], curse_percentage=0.0):
    _results = []

    print(f"Raniks curse uptime: {curse_percentage:.0%}")

    for weapon in weapons:
        _attack_total = 0
        _damage_total = 0
        _num_crits = 0
        weapon_results = []

        for _ in range(sims):
            crit = False
            attack = random.randint(1, 20)
            _attack = attack + ability + proficiency + weapon.atk_mod()

            if random.random() < curse_percentage:
                if attack >= 19:
                    crit = True
                    _num_crits += 1
                _damage = weapon.damage_roll(
                    crit) + ability + proficiency  # pact weapon + cursed target add prof to dmg
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


def simulate_solas(sims: int, ability: int, proficiency: int, weapons: List[Weapon]) -> List[
    Tuple[Weapon, pd.DataFrame]]:
    other_dmg = 2
    _results = []

    for weapon in weapons:
        _attack_total = 0
        _damage_total = 0
        _num_crits = 0
        weapon_results = []

        for _ in range(sims):
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


def simulate_daruth(sims: int, ability: int, proficiency: int, weapons: List[Weapon]):
    _results = []

    for weapon in weapons:
        _attack_total = 0
        _damage_total = 0
        _num_crits = 0
        weapon_results = []

        for _ in range(sims):
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


HEADER = "{0:55}{1:>10}{2:>10}{3:>10}".format(f"Name", "Attack", "Damage", "Crit %")
TEMPLATE = "{0:55}{1:>10.1f}{2:>10.1f}{3:>10.1%}"


def print_results(name, attacks, damage, crits):
    print(TEMPLATE.format(name, attacks, damage, crits))


def ranik():
    raniks_weapons = [
        # battleaxe,
        # battleaxe_2h,
        flametongue
    ]
    num_attacks = 2
    results = simulate_ranik(SIMS, ability=3, proficiency=3, weapons=raniks_weapons, curse_percentage=0.5)
    for weapon, result in results:
        print_results(f"Ranik's {weapon}", result['attack'].mean(), result['damage'].mean() * num_attacks,
                      result['crit'].sum() / SIMS)
        # show_matrices(result)


def solas():
    solas_weapons = [
        # longsword,
        flametongue
    ]
    num_attacks = 2
    results = simulate_solas(SIMS, ability=2, proficiency=3, weapons=solas_weapons)
    for weapon, result in results:
        print_results(f"Solas' {weapon}", result['attack'].mean(), result['damage'].mean() * num_attacks,
                      result['crit'].sum() / SIMS)
        # show_matrices(result)


def daruth():
    daruths_weapons = [
        # monk_hand,
        d_flametongue
    ]
    num_attacks = 2
    results = simulate_daruth(SIMS, ability=4, proficiency=3, weapons=daruths_weapons)
    for weapon, result in results:
        print_results(f"Daruth's {weapon}", result['attack'].mean(), result['damage'].mean() * num_attacks,
                      result['crit'].sum() / SIMS)
        # show_matrices(result)


if __name__ == "__main__":
    start = time.perf_counter()
    SIMS = 100_000
    print(f"{SIMS} sims")
    print(HEADER)

    ranik()
    solas()
    daruth()

    print(f"Time: {time.perf_counter() - start:.1f}s")
