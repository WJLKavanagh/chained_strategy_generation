# William Kavanagh, Feb 2019
# Identifies dominant strategies in RPGLite for a given configuration
# USAGE: ???

import prefix, free_strat, adversarial_strat, suffix, stochastic_strat, naive_strat     # PRISM generating files
import sys, os

# USAGE OF IMPORTED FILES:
# prefix.run([characters], smg?, multiple_init?, config_prefix)
# free_strat.run([characters], player#)
# adversarial_strat.run([characters], player#, adv_file_prefix)
# suffix.run([characters], multiple_init?)
# stochastic_strat.run([characters], player#, config_prefix)
# naive_strat.run([characters], player#)

config = sys.argv[1]
output_destination = sys.argv[2]


pairs = ["KA","KW","AW"]                # All material choices for a player
for pair in pairs:                      # For each pair
    print("Pair: " + pair + " generating optimal strategy..")
    characters = pair+pair              # Generate the optimal strategy for a symmetric setup from the full initial set
    sys.stdout = open(output_destination + "/" + characters + "_smg_mul.prism", "w")
    prefix.run(characters, 1, 1, config)
    free_strat.run(characters, 1)
    free_strat.run(characters, 2)
    suffix.run(characters, 1)
    sys.stdout = sys.__stdout__
    os.system("prism " + output_destination + "/" + characters + "_smg_mul.prism properties/smg.props -prop 1 -exportstates tmp.sta -exportadvmdp tmp.tra > " + output_destination + "/log.txt")
    print("Strategy generated, calculating adversaries..")
    





"""
prefix.run(characters, 0, 0, config)
naive_strat.run(characters, 1)
free_strat.run(characters, 2)
suffix.run(characters, 0)
"""
