# William Kavanagh, Feb 2019
# Generate a suffix of PRISM files for CAG.
# USAGE: run(["K","A","K","W"], 0)

# Main proc:
# Input: chars as list, multiple_init_states as bool
# Output: prints suffix of PRISM file representing RPGLite
def run(characters, multiple_init_states):
    for player in range(2):             # Current Player
        print("// Action resolution player " + str(player+1))
        for char in range(2):           # Current Actor
            for opp in range(2):        # Current Target
                actor = "p" + str(player+1) + "c" + str(char+1)         # String representing actor
                target = "p" + str(2-player) + "c" + str(opp+1)         # String representing target
                action_label = "\t[" + actor + "_" + target + "]\t"
                attack_state = (4*player + 2*char + opp + 1)
                action_string = action_label + "attack = " + str(attack_state)

                if characters[2*player+char] == "K":                # if actor is a Knight
                    action_string += " & " + target + " > 0 -> "
                    action_string += "Knight_accuracy: (" + target + "' = " + target + " - Knight_damage) & (attack' = 9) + "
                    action_string += "1 - Knight_accuracy: (attack' = 9);"
                    print(action_string)
                elif characters[2*player+char] == "W":              # if actor is a Wizard
                    action_string += " & " + target + " > 0 -> "
                    action_string += "Wizard_accuracy: (" + target + "' = " + target + " - Wizard_damage) & (attack' = 9) & (" + target[:2] + "_stun' = " + str(opp+1) + ") + "
                    action_string += "1 - Wizard_accuracy: (attack' = 9);"
                    print(action_string)
                else:                                               # Else actor is an Archer
                    goto = 9
                    if attack_state % 2 == 1: goto = attack_state + 1   # Attempt next attack or finish second attack
                    action_string1 = action_string + " & " + target + " > 0 -> Archer_accuracy: (" + target + "' = " + target
                    action_string1 += " - Archer_damage) & (attack' = " + str(goto) + ") + 1 - Archer_accuracy: (attack' = " + str(goto) + ");"
                    action_string2 = action_string + " & " + target + " < 1 -> (attack' = " + str(goto) + ");"
                    print(action_string1)
                    print(action_string2)
    print("endmodule\n")

    if multiple_init_states:
        print("//Multiple initial states\ninit\n\tattack = 0 & turn > 0\nendinit\n")
# Labels and Formulae
    print('label \"p1_wins\" = (p1c1 > 0 | p1c2 > 0) & p2c1 < 1 & p2c2 < 1;')
    print('label \"p2_wins\" = (p2c1 > 0 | p2c2 > 0) & p1c1 < 1 & p1c2 < 1;')
    print("formula health_ceiling \t= max(Knight_health, Archer_health, Wizard_health);")
    print("formula health_floor \t= 1 - max(Knight_damage, Archer_damage, Wizard_damage);")
