# William Kavanagh, Feb 2019
# Generate prefix of PRISM files for CAG.
# EXAMPLE USAGE: run(["K","A","K","W"], 1, 0, "a")

import datetime

# Given character as <char>, find health in config_<config>.txt
def find_health(char, config):
    config_as_line_list = open("configurations/config_" + config + ".txt", "r").readlines()
    for line in config_as_line_list:
        if "health" in line and line[10] == char.upper():
            return line.split("= ")[1].split(";")[0]

# Main proc:
# Input: chars as list, model_is_smg as bool, multiple_init_states as bool, config as str
# Output: prints prefix of .prism file to stdout
def run(characters, model_is_smg, multiple_init_states, config):
# Print comments and model
    print("// Author:\tWilliam Kavanagh, University of Glasgow")
    print("// Created:\t" + str(datetime.datetime.now())[:-7])
    print("// File:\tCAG auto-generated model")
    print("// Characters:\t" + characters[0] + characters[1] + " vs " + characters[2] + characters[3] + "\n")
    if model_is_smg:
        print("smg\n")
    else:
        print("mdp\n")
# Print configuration and players if appropriate
    print("// Configuration " + config.upper() + ":")
    for line in (open("configurations/config_" + config + ".txt", "r").readlines()):
        print(line[:-1])
    if model_is_smg:
        p1_action_list = "\nplayer p1\n\t[p1_turn_1], "             # Build string for P1's actions
        if characters[0] != "A":
            p1_action_list += "[p1_turn_2], "
        p1_action_list += "[p1_turn_3], "
        if characters[1] != "A":
            p1_action_list += "[p1_turn_4], "
        print (p1_action_list + "[p1_turn_skip]\nendplayer")
        p2_action_list = "player p2\n\t[p2_turn_5], "
        if characters[2] != "A":
            p2_action_list += "[p2_turn_6], "
        p2_action_list += "[p2_turn_7], "
        if characters[3] != "A":
            p2_action_list += "[p2_turn_8], "
        print (p2_action_list + "[p2_turn_skip]\nendplayer")
# Define variables with inits if appropriate
    print("\nmodule game")
    print("\tattack\t: [0..9]; // Action decision: 0 - NONE, 1 - p1c1>p2c1, 2 - p1c1>p2c2, 3 - p1c2>p2c1, 4 - p1c2>p2c2, 5 - p2c1>p1c1, 6 - p2c1>p1c2, 7 - p2c2>p1c1, 8 - p2c2>p1c2, 9 - NEXT")
    print("\tturn\t: [0..2]; // Player to act")
    for player_num in range(2):
        for char_num in range(2):
            if player_num == 0 and char_num == 0:
                print("// Health and is_stunned variables")
            if multiple_init_states:
                print("\tp"+str(player_num+1)+"c"+str(char_num+1)+"\t: [health_floor..health_ceiling];\t\t// player " + str(player_num+1) + " character " + str(char_num+1) + " health value")
            else:
                PxCx_health = find_health(characters[2*player_num+char_num], config)
                print("\tp"+str(player_num+1)+"c"+str(char_num+1)+"\t: [health_floor..health_ceiling] init " + PxCx_health + ";\t// player " + str(player_num+1) + " character " + str(char_num+1) + " health value")
        print("\tp"+str(player_num+1)+"_stun\t: [0..2]; \t\t\t\t\t// 0 - Neither character stunned, 1 - character 1 stunned, 2 - character 2 stunned")
    print("\n\t[flip_coin]\tturn = 0 -> 0.5 : (turn' = 1) + 0.5 : (turn' = 2);")
    print("\t[next_turn]\tattack = 9 & turn > 0 & (p1c1 > 0 | p1c2 > 0) & (p2c1 > 0 | p2c2 > 0) -> (attack' = 0) & (turn' = 3 - turn);\n")
