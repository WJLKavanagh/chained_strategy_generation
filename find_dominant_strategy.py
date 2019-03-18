# William Kavanagh, Feb 2019
# Identifies dominant strategies in RPGLite for a given configuration
# USAGE: For a given configuration of RPGLite, identify dominant strategies if show they do not exist

import prefix, free_strat, adversarial_strat, suffix, stochastic_strat, naive_strat     # PRISM generating files
import sys, os

# USAGE OF IMPORTED FILES:
# prefix.run([characters], smg?, multiple_init?, config_prefix)
# free_strat.run([characters], player#)
# adversarial_strat.run([characters], player#, adv_file_prefix, always_p1?)
# suffix.run([characters], multiple_init?)
# stochastic_strat.run([characters], player#, config_prefix)
# naive_strat.run([characters], player#)

# HIGH-LEVEL:
# For each material in Material: (m in [KA, KW, AW]):
#   Generate the optimal strategy when played against itself
#   For each opposing material in Material (m' in [KA, KW, AW] != m)
#       For both orderings of the pair (m = c1c2 | c2c1)
#           Calculate the adversarial probability against the optimal strategy
#           If either of the probabilities is under 0.5:
#               The strategy is dominant

def find_result(file):
    f = open(file, "r").readlines()
    for i in range(len(f)-1,0,-1):
        if "Result:" in f[i]:
            return f[i].split("ult: ")[1].split(" (value")[0]

config = sys.argv[1]
output_destination = sys.argv[2]
on_sand = sys.argv[3]


pairs = ["KA","KW","AW"]                # All material choices for a player
for pair in pairs:                      # For each pair
    print("Pair: " + pair + " generating optimal strategy, this can take up to 5 minutes ...")
    characters = pair+pair              # Generate the optimal strategy for a symmetric setup from the full initial set
    sys.stdout = open(output_destination + "/" + characters + "_smg_mul.prism", "w+")
    prefix.run(characters, 1, 1, config)
    free_strat.run(characters, 1)
    free_strat.run(characters, 2)
    suffix.run(characters, 1)
    sys.stdout = sys.__stdout__
    if on_sand == "1":
    # Usually takes 2-3 seconds to build the model and 2.5 minutes to calculate the adversary
        # "on sand"
        os.system("/scratch/gethin/prism-william/prism/bin/prism " + output_destination + "/" + characters + "_smg_mul.prism \
        properties/smg.props -prop 1 -exportstates " + output_destination + "/tmp.sta -exportadvmdp " + output_destination + "/tmp.tra -javamaxmem 400g \
        > " + output_destination + "/log.txt")
    else:
        # "not on sand"
        os.system("prism " + output_destination + "/" + characters + "_smg_mul.prism properties/smg.props -prop 1 -javamaxmem 4g -exportstates " + output_destination + "/tmp.sta -exportadvmdp " + output_destination + "/tmp.tra > " + output_destination + "/log.txt")
    print("Strategy generated, calculating adversaries..")
    # Strategy is encoded in tmp.sta and tmp.tra files.
    sys.stdout = open(output_destination + "/" + pair + "_optimal_strategy.txt", "w+")
    adversarial_strat.run(characters, 1, output_destination + "/tmp", False)
    # Strategy is encoded as Prism code in a .txt file
    sys.stdout = sys.__stdout__
    for opposing_pair in pairs:
        if opposing_pair != pair:
            for opposing_order in [opposing_pair, opposing_pair[1]+opposing_pair[0]]:   # For both orderings, i.e. KA = [KA, AK]
                characters = pair+opposing_order
                sys.stdout = open(output_destination + "/" + characters + "_OptvAdv.prism", "w+")
                prefix.run(characters, 0, 0, config)
                print(open(output_destination + "/" + pair + "_optimal_strategy.txt", "r").read())
                free_strat.run(characters, 2)
                suffix.run(characters, 0)
                sys.stdout = sys.__stdout__
                if on_sand == "1":
                    # "on sand"
                    os.system("/scratch/gethin/prism-william/prism/bin/prism " + output_destination + "/" + characters + "_OptvAdv.prism \
                    properties/mdp.props -prop 2 -exportstates " + output_destination + "/tmp.sta -exportadvmdp " + output_destination + "/tmp.tra -javamaxmem 400g \
                    > " + output_destination + "/log.txt")
                else:
                    # "not on sand"
                    os.system("prism " + output_destination + "/" + characters + "_OptvAdv.prism properties/mdp.props -prop 2 -javamaxmem 4g -exportstates " + output_destination + "/tmp.sta -exportadvmdp " + output_destination + "/tmp.tra > " + output_destination + "/log.txt")
                print("Comparing adversary for " + opposing_order + " against optimal symmetric strategy for " + pair + ", result: " + find_result(output_destination+"/log.txt"))
