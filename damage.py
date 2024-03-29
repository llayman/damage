import random


def calc_damage(attack: int, dice: int, ability: int = 0, other_dmg=0, crit=20, num_dice: int = 1):
    damage = 0
    for _ in range(num_dice):
        damage += random.randint(1, dice)
        if attack >= crit:
            damage += random.randint(1, dice)
    return damage + other_dmg + ability


def solas_longsword(sims: int, ability: int, num_attacks = 1):
    attacks = 0
    damage = 0
    crits = 0
    for _ in range(sims):
        for __ in range(num_attacks):
            attack = random.randint(1, 20)
            attacks += attack + ability + 2

            if attack >= 20:
                crits += 1
            damage += calc_damage(attack, dice=8, ability=ability, other_dmg=2)  # dueling

    return attacks / (sims * num_attacks), damage / sims, crits * 100 / (sims * num_attacks)


def ranik_axe(sims: int, ability: int, curse_percentage=.5):
    attacks = 0
    damage = 0
    crits = 0
    for _ in range(sims):
        attack = random.randint(1, 20)  # assumes pact weapon
        attacks += attack + ability + 2

        if random.random() < curse_percentage:
            if attack >= 19:
                crits += 1
            damage += calc_damage(attack, dice=8, ability=ability, other_dmg=1+2, crit=19)  # assumes pact weapon and + 1 axe
        else:
            if attack >= 20:
                crits += 1
            damage += calc_damage(attack, dice=8, ability=ability, other_dmg=1)  # assumes pact weapon and + 1 axe
    return attacks / sims, damage / sims, crits * 100 / sims

def ranik_axe_two_handed(sims: int, ability: int, curse_percentage=.5, num_attacks: int = 1):
    attacks = 0
    damage = 0
    crits = 0
    for _ in range(sims):
        for __ in range(num_attacks):
            attack = random.randint(1, 20)  # assumes pact weapon
            attacks += attack + ability + 2

            if random.random() < curse_percentage:
                if attack >= 19:
                    crits += 1
                damage += calc_damage(attack, dice=10, ability=ability, other_dmg=1 + 2,
                                      crit=19)  # assumes pact weapon and + 1 axe
            else:
                if attack >= 20:
                    crits += 1
                damage += calc_damage(attack, dice=10, ability=ability, other_dmg=1)  # assumes pact weapon and + 1 axe


    return attacks / (sims * num_attacks), damage / sims, crits * 100 / (sims * num_attacks)


def solas_flametongue(sims: int, ability: int, num_attacks: int = 1):
    attacks = 0
    damage = 0
    crits = 0
    for _ in range(sims):
        for __ in range(num_attacks):
            attack = random.randint(1, 20)
            attacks += attack + ability + 2

            if attack >= 20:
                crits += 1
            damage += calc_damage(attack, dice=6, ability=ability, other_dmg=2)  # dueling
            damage += calc_damage(attack, dice=6)
            damage += calc_damage(attack, dice=6)

    return attacks / (sims * num_attacks), damage / sims, crits * 100 / (sims * num_attacks)

def ranik_flametongue(sims: int, ability: int, curse_percentage=.5, num_attacks: int = 1):
    attacks = 0
    damage = 0
    crits = 0
    for _ in range(sims):
        for __ in range(num_attacks):
            attack = random.randint(1, 20)
            attacks += attack + ability + 2
            if random.random() < curse_percentage:
                if attack >= 19:
                    crits += 1
                damage += calc_damage(attack, dice=6, ability=ability, other_dmg=2, crit=19)  # assumes pact weapon
                damage += calc_damage(attack, dice=6, crit=19)
                damage += calc_damage(attack, dice=6, crit=19)
            else:
                if attack >= 20:
                    crits += 1
                damage += calc_damage(attack, dice=6, ability=ability)  # assumes pact weapon
                damage += calc_damage(attack, dice=6)
                damage += calc_damage(attack, dice=6)

    return attacks / (sims * num_attacks), damage / sims, crits * 100 / (sims * num_attacks)




def print_results(title, attacks, damage, crits):
    print(f"{title} attack: {attacks:.1f}, damage: {damage:.1f}, crits: {crits:.1f}%")

class Weapon:

    def __init__(self, name, damage, extra_dmg):
        self.name = name
        self.damage = damage
        self.xtra_dmg = extra_dmg
        self.flat = None
        self.num_rolls, self.dice, self.modififer = self._split(damage)
        self.xtra_num_rolls, self.xtra_dice, self.xtra_modifier = self._split(extra_dmg)

    def _split(self, dmg):
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

    def __repr__(self):
        return f"Weapon({self.name}, {self.damage}, {self.xtra_dmg})"

    def __str__(self):
        result = self.name + ": "
        if(self.flat):
            result += str(self.flat)
            return result
        result += f"{self.num_rolls}d{self.dice}"
        if(self.modififer != 0):
            result += str(self.modififer)


        return result






if __name__ == "__main__":
    SIMS = 100000
    result = solas_longsword(SIMS, 2)
    print_results("Solas' longsword attack", *result)
    result2 = solas_flametongue(SIMS, 2)
    print_results("Solas' flametongue attack", *result2)
    print(f"Damage diff: {result2[1] - result[1]:.1f}")

    result = solas_longsword(SIMS, 2, num_attacks=2)
    print_results("Solas' longsword attack (multiattack)", *result)
    result2 = solas_flametongue(SIMS, 2, num_attacks=2)
    print_results("Solas' flametongue attack (multiattack)", *result2)
    print(f"Damage diff: {result2[1] - result[1]:.1f}")

    print('='*10)

    curse = .4
    ranik_axe_result = ranik_axe(SIMS, 3, curse_percentage=.4)
    print_results("Ranik's battleaxe attack", *ranik_axe_result)

    ranik_axe_result_dual = ranik_axe_two_handed(SIMS, 3, curse_percentage=.4)
    print_results("Ranik's battleaxe (two-hand)", *ranik_axe_result_dual)

    ranik_flametongue_result = ranik_flametongue(SIMS, 3, curse_percentage=.4)
    print_results("Ranik's flametongue attack", *ranik_flametongue_result)

    ranik_axe_result_dual = ranik_axe_two_handed(SIMS, 3, curse_percentage=.4, num_attacks=2)
    print_results("Ranik's battleaxe (two-hand, multiattack)", *ranik_axe_result_dual)

    ranik_flametongue_result = ranik_flametongue(SIMS, 3, curse_percentage=.4, num_attacks=2)
    print_results("Ranik's flametongue attack (multiattack)", *ranik_flametongue_result)

    flametongue = Weapon("Flametongue", "1d6", "2d6")
    print(flametongue)


