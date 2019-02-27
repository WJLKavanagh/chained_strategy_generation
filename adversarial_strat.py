# William Kavanagh, Feb 2019
# Generate a pure adversarial strategy for a player in CAG.
# USAGE: run(["K","A","K","W"], 2, "tmp")

# Main proc:
# Input: chars as list, player as <int> [1,2], file_prefix as str
# Output: prints adversarial strategy for player <player> based on files <file_prefix>.tra/.sta
def run(characters, player, file_prefix):
    print("//Action decision for P" + str(player) + ", adversarial strategy")
    reset_stuns_string = "(p" + str(player) + "_stun' = 0);"
    transitions = {}                                                # Dictionary stores all relevant transitions
    for line in open(file_prefix+".tra","r").readlines():           # For every line in the .tra file
        if line[-10:-2] == "p" + str(player) + "_turn_":            # If the line is relevant
            transitions[line.split(" ")[0]] = line.split("_")[2][:-1]    # Store state_id with attack label
    state_description = ["attack", "turn", "p1c1", "p1c2", "p1_stun", "p2c1", "p2c2", "p2_stun"]
    for line in open(file_prefix+".sta","r").readlines()[1:]:       # For every state in the model (skip first line)
        if line.split(":(")[1][0] != "0":                           # If the state is a decision state
            break                                                   # States no longer relevant, end.
        if line.split(":(")[1][2] == str(player):                   # State is decision state for correct player
            state_info = line.split(":(")[1][:-2].split(",")        # Collect state info as list (attack and turn, we know those)
            state_id = line.split(":(")[0]                          # Collect state id
            if state_id in transitions.keys():                      # If state is valid (states where the game is over are ignored)
                guard_comm = "\t[p" + str(player) + "_turn_" + transitions[state_id] + "]\t"    # build guard_comm string
                for i in range(len(state_description)):             # Iterate over each VAR in the state
                    guard_comm += state_description[i] + " = " + state_info[i]
                    if i < len(state_description) - 1:
                        guard_comm += " & "
                guard_comm += " ->\n\t\t\t\t (attack' = " + transitions[state_id] + ") & (p"
                guard_comm += str(player) + "c1_s' = false) & (p" + str(player) + "c2_s' = false);"
                print(guard_comm)
    skip_action = "\t[p" + str(player) + "_turn_skip]\tattack = 0 & turn = "
    skip_action += str(player) + " & ( (p" + str(player) + "_stun = 1 & p" + str(player) + "c2 < 1) | "
    skip_action += "(p" + str(player) + "_stun = 2 & p" + str(player) + "c1 < 1) ) ->\n\t\t\t\t(attack' = 9) & "
    print(skip_action + reset_stuns_string + " // skip if forced")
