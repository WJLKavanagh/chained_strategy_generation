# William Kavanagh, Feb 2019
# Generate a 'free' (nondeterministic) strategy for a player in CAG.
# USAGE: run(["K","A","K","W"], 2)

# Main proc:
# Input: chars as list, player as <int> [1,2]
# Output: prints free strategy for player <player>
def run(characters, player):
    print("// Action decision for P" + str(player) + ", free strategy")
    action_num = 5
    if player == 1: action_num = 1
    reset_stuns_string = "(p" + str(player) + "c1_s' = false) & (p" + str(player) + "c2_s' = false);"
    for char_num in range(2):
        prefix_string_to_print = "\tattack = 0 & turn = "
        prefix_string_to_print += str(player) + " & p" + str(player) + "c" + str(char_num+1)
        prefix_string_to_print += " > 0 & p" + str(player) + "c" + str(char_num+1) + "_s = false & "
        if characters[2*(player-1)+char_num] == "A":
            label = "\t[p" + str(player) + "_turn_" + str(action_num) + "]"
            prefix_string_to_print += "(p" + str(3-player) + "c1 > 0 | p" + str(3-player) + "c2 > 0) -> "
            prefix_string_to_print += "(attack' = " + str(action_num) + ") & "
            print(label + prefix_string_to_print + reset_stuns_string)
            action_num += 2
        else:
            for opponent_c in range(1,3):
                label = "\t[p" + str(player) + "_turn_" + str(action_num) + "]"
                string_to_print = label + prefix_string_to_print
                string_to_print += "p" + str(3-player) + "c" + str(opponent_c) + " > 0 -> "
                string_to_print += "(attack' = " + str(action_num) + ") & "
                print(string_to_print + reset_stuns_string)
                action_num += 1
    skip_action = "\t[p" + str(player) + "_turn_skip]\tattack = 0 & turn = "
    skip_action += str(player) + " & ( (p" + str(player) + "c1_s & p" + str(player) + "c2 < 1) | "
    skip_action += "(p" + str(player) + "c1 < 1 & p" + str(player) + "c2_s) ) -> (attack' = 9) & "
    print(skip_action + reset_stuns_string + " // skip if forced")


# run(["K","A","K","W"], 2)
