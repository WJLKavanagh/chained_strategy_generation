# William Kavanagh, Feb 2019
# Generate stochastic seed strategy for a player in CAG.
# EXAMPLE USAGE: run(["K","A","K","W"], 1, config)

import random

# Return <attribute> for <char> in config_<config>.txt as int
def find_attribute(char, config, attribute):
    config_as_line_list = open("configurations/config_" + config + ".txt", "r").readlines()
    for line in config_as_line_list:
        if attribute in line and line[10] == char.upper():
            return int(line.split("= ")[1].split(";")[0])

# Main proc:
# Input: chars as list, player as <int> [1,2]
# Output: prints (stochastic) deterministic seed strategy for player <player>
#         where an action for every state is chosen at random
def run(characters, player, config):
    print("// Action decision for P" + str(player) + ", stochastic strategy")
    max_health = max(
    find_attribute("K", config, "health"),
    find_attribute("A", config, "health"),
    find_attribute("W", config, "health") )
    min_health = 1 - max(
    find_attribute("K", config, "damage"),
    find_attribute("A", config, "damage"),
    find_attribute("W", config, "damage") )
    for pc1 in range(min_health, max_health+1):                 # Player character 1
            for pc2 in range(min_health, max_health+1):
                for oc1 in range(min_health, max_health+1):     # Opponent character and oc1 > 0 and !stuns[0]:
                    for oc2 in range(min_health, max_health+1):
                        for pstun in range(3):
                            possible_actions = []               # List of all actions possible from state
                            action = "9"
                            if pc1 > 0 and oc1 > 0 and pstun != 1: possible_actions += [1]
                            if pc1 > 0 and oc2 > 0 and pstun != 1 and characters[2*(player-1)] != "A": possible_actions += [2]
                            if pc2 > 0 and oc1 > 0 and pstun != 2: possible_actions += [3]
                            if pc2 > 0 and oc2 > 0 and pstun != 2 and characters[2*(player-1) + 1] != "A": possible_actions += [4]
                            if player == 2: possible_actions = [x+4 for x in possible_actions]
                            if len(possible_actions) > 0: action = str(random.choice(possible_actions)) # Pick one action at random if one is available
                            label = "\t[p" + str(player) + "_turn_" + action + "]\t"                    # action label to print
                            guard = "p" + str(player) + "c1 = " + str(pc1) + " & p" + str(player) + "c2 = " + str(pc2)
                            # for i in range(2):
                            #     if pstun == i+1: guard += " & p" + str(player) + "c" + str(i+1) + "_s"
                            #     else: guard += " & !p" + str(player) + "c" + str(i+1) + "_s"
                            guard += " & p" + str(player) + "_stun = " + str(pstun)
                            guard += " & p" + str(3-player) + "c1 = " + str(oc1) + " & p" + str(3-player) + "c2 = " + str(oc2) + " -> "
                            command = "(attack' = " + action + ") & (p" + str(player) + "_stun' = 0);"
                            print(label + guard + command)

#run(["K","A","K","A"], 2, "a")
