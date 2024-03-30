import random


class Weapon:

    def __init__(self, name, damage, extra_dmg='0'):
        self.name = name
        self.damage = damage
        self.xtra_dmg = extra_dmg
        self.flat = None
        self.num_rolls, self.dice, self.modifier = self._split(damage)
        self.xtra_num_rolls, self.xtra_dice, self.xtra_modifier = self._split(extra_dmg)

    def _split(self, dmg):
        if str(dmg) == '0':
            return 0, 0, 0
        dmg = "".join(dmg.split()).lower()
        mod_str = dmg.split(r'+')
        modifier = 0
        num_roll = 0
        die = 0

        if len(mod_str) == 2:
            modifier = int(mod_str[1])
        elif len(mod_str) > 2:
            raise ValueError("Too many +'s")

        # Could be flat or <x>d<y>
        dmg = mod_str[0]
        die_str = dmg.split('d')
        if len(die_str) == 1:
            # flat damage
            # XXX: Won't work if extra also has flat damage
            self.flat = int(die_str[0])
        elif len(die_str) != 2:
            raise ValueError("Too many d's")
        else:
            num_roll = int(die_str[0])
            die = int(die_str[1])

        return num_roll, die, modifier

    def damage_roll(self, crit=False):
        if self.flat:
            return self.flat

        damage = self._roll(self.num_rolls, self.dice, crit) + self.modifier

        if self.xtra_dmg:
            damage += self._roll(self.xtra_num_rolls, self.xtra_dice, crit) + self.xtra_modifier

        return damage

    def _roll(self, num, die, crit):
        damage = 0
        for _ in range(num):
            damage += random.randint(1, die)
            if crit:
                damage += random.randint(1, die)
        return damage

    def __repr__(self):
        return f"Weapon({self.name}, {self.damage}, {self.xtra_dmg})"

    def __str__(self):
        _result = self.name + " ("
        if self.flat:
            _result += str(self.flat)
            return _result
        _result += f"{self.num_rolls}d{self.dice}"
        if self.modifier != 0:
            _result += f'+{self.modifier}'
        return _result + ')'


def calc_damage(attack: int, dice: int, ability: int = 0, other_dmg=0, crit=20, num_dice: int = 1):
    damage = 0
    for _ in range(num_dice):
        damage += random.randint(1, dice)
        if attack >= crit:
            damage += random.randint(1, dice)
    return damage + other_dmg + ability


def solas_weapon(sims: int, weapon: Weapon, num_attacks=1):
    ability = 2
    proficiency = 2
    other_dmg = 2

    _attack_total = 0
    _damage_total = 0
    _num_crits = 0

    for _ in range(sims):
        for __ in range(num_attacks):
            crit = False
            attack = random.randint(1, 20)
            _attack_total += attack + ability + proficiency

            if attack >= 20:
                crit = True
                _num_crits += 1
            _damage_total += weapon.damage_roll(crit) + ability + other_dmg

    return _attack_total / (sims * num_attacks), _damage_total / sims, _num_crits * 100 / (sims * num_attacks)


def ranik_weapon(sims: int, weapon: Weapon, curse_percentage, num_attacks=1):
    ability = 3
    proficiency = 2
    other_dmg = 0

    _attack_total = 0
    _damage_total = 0
    _num_crits = 0
    for _ in range(sims):
        for __ in range(num_attacks):
            crit = False
            attack = random.randint(1, 20)
            _attack_total += attack + ability + proficiency

            if random.random() < curse_percentage:
                if attack >= 19:
                    crit = True
                    _num_crits += 1
                _damage_total += weapon.damage_roll(crit) + ability + proficiency  # cursed target add prof to dmg
            else:
                if attack >= 20:
                    crit = True
                    _num_crits += 1
                _damage_total += weapon.damage_roll(crit) + ability  # assumes pact weapon

    return _attack_total / (sims * num_attacks), _damage_total / sims, _num_crits * 100 / (sims * num_attacks)


def print_results(name, attacks, damage, crits):
    print(f"{name} attack: {attacks:.1f}, damage: {damage:.1f}, crits: {crits:.1f}%")


if __name__ == "__main__":
    SIMS = 100_000

    curse = .4

    w = battleaxe = Weapon("battleaxe", "1d8+1")
    print_results(f"Ranik's {w}", *ranik_weapon(SIMS, battleaxe, curse))

    w = battleaxe_2h = Weapon("battleaxe (2H)", "1d10+1")
    print_results(f"Ranik's {w}", *ranik_weapon(SIMS, battleaxe_2h, curse))

    w = flametongue = Weapon("flametongue scimitar?", "1d6", "2d6")
    print_results(f"Ranik's {w}", *ranik_weapon(SIMS, flametongue, curse))

    #
    # ranik_flametongue_result = ranik_flametongue(SIMS, 3, curse_percentage=.4, num_attacks=2)
    # print_results("Ranik's flametongue attack (multiattack)", *ranik_flametongue_result)
    #
    # flametongue = Weapon("Flametongue", "1d6", "2d6")
    # print(flametongue)


    longsword = Weapon("Longsword", "1d8")
    result = solas_weapon(SIMS, longsword, 2)
    print_results("Solas' longsword attack (weapon)", *result)


