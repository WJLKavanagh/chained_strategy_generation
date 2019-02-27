# William Kavanagh, Feb 2019
# Generate stochastic seed strategy for a player in CAG.
# EXAMPLE USAGE: run(["K","A","K","W"], 1, config)

import random

# Main proc:
# Input: chars as list, player as <int> [1,2]
# Output: prints naive seed strategy for player <player>
#         where an action for every state is chosen with an even probability
def run(characters, player):
    print("// Action decision for P" + str(player) + ", naive strategy")
    for Pc1_usable in [True,False]:                         # Can use action of player's first character (i.e. Alive AND not stunned)
        for Pc2_usable in [True,False]:
            for Oc1_targetable in [True,False]:             # Can target opponent's second character (i.e. Alive)
                for Oc2_targetable in [True,False]:
                    available_actions = []                  # List of actions available
                    reset_stuns = "(p" + str(player) + "_stun' = 0)"
                    command = ""
                    for i in range(2):
                        if characters[i] == "A":
                            if [Pc1_usable,Pc2_usable][i] and (Oc1_targetable or Oc2_targetable): available_actions += [2*i+1+(4*(player-1))]
                        else:
                            if [Pc1_usable,Pc2_usable][i] and Oc1_targetable: available_actions += [2*i+1+(4*(player-1))]
                            if [Pc1_usable,Pc2_usable][i] and Oc2_targetable: available_actions += [2*i+2+(4*(player-1))]
                    if len(available_actions) > 1:                              # If more than one action is available
                        guard = "\t[p" + str(player) + "_turn_" + str(4*(player-1)+1) + "]\t"             # NOTE: Labelled as Px_turn_1 when infact these can be _1/2/3/4
                        for index in range(len(available_actions)):
                            command += "1/" + str(len(available_actions)) + ": (attack' = " + str(available_actions[index]) + ") & " + reset_stuns
                            if index < len(available_actions) - 1:
                                command += " +\n\t\t\t"
                            else:
                                command += ";"
                    elif len(available_actions) == 1:
                        guard = "\t[p" + str(player) + "_turn_" + str(available_actions[0]) + "]\t"              # We do this so SMG player declaration still works
                        command = "(attack' = " + str(available_actions[0]) + ") & " + reset_stuns
                        ## TODO
                    else:
                        continue
                    if Pc1_usable: guard += "p" + str(player) + "c1 > 0 & p" + str(player) + "_stun != 1 & "
                    else: guard += "(p" + str(player) + "c1 < 1 | p" + str(player) + "_stun = 1) & "
                    if Pc2_usable: guard += "p" + str(player) + "c2 > 0 & !p" + str(player) + "_stun != 2 & "
                    else: guard += "(p" + str(player) + "c2 < 1 | p" + str(player) + "c_stun = 2) & "
                    if Oc1_targetable: guard += "p" + str(3-player) + "c1 > 0 & "
                    else: guard += "p" + str(3-player) + "c1 < 1 & "
                    if Oc2_targetable: guard += "p" + str(3-player) + "c2 > 0 ->\n\t\t\t"
                    else: guard += "p" + str(3-player) + "c2 < 1 ->\n\t\t\t"
                    print(guard + command)
run(["K","A","K","W"], 2)
