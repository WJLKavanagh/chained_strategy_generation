# William Kavanagh, March 2019
# Identifies dominant strategies in RPGLite for a given configuration
# USAGE: For a given configuration of RPGLite, find adversarial strategies of known effective strategies to identify dominanted material

import prefix, free_strat, adversarial_strat, suffix, stochastic_strat, naive_strat     # PRISM generating files
import sys, os, random, filecmp

# USAGE OF IMPORTED FILES:
# prefix.run([characters], smg?, multiple_init?, config_prefix)
# free_strat.run([characters], player#)
# adversarial_strat.run([characters], player#, adv_file_prefix, always_p1?)
# suffix.run([characters], multiple_init?)
# stochastic_strat.run([characters], player#, config_prefix)
# naive_strat.run([characters], player#)

# HIGH-LEVEL:
# Generate some seed Strategy
# For each pair:
#   calculate the adversarial likelihood against the strategy
# generate the adversary with maximal likelihood from multiple initial states
# *For each pair:
#   calculate the adversarial likelihood against the newly generated strategy
# Generate the adverasry with maximal likelihood from multiple initial states
# If the strategy has not been generated before:
#   goto *


def find_result(file):
    f = open(file, "r").readlines()
    for i in range(len(f)-1,0,-1):
        if "Result:" in f[i]:
            return f[i].split("ult: ")[1].split(" (value")[0]

# Takes some int i, returns true if adversary<i>.txt is uniqe
# i.e. there is not some k < i where adversary<k>.txt == adversary_strat_<i>.txt
def adversary_is_unique(i):
    if i > 1:
        for k in range(i-1, 0, -1):
            if filecmp.cmp(
            output_destination + "/adversary" + str(i) + ".txt",
            output_destination + "/adversary" + str(k) + ".txt",
            shallow=False):
                print("Adversary " + str(i) + " found to be identical to adversary " + str(k))
                return False
    return True

config = sys.argv[1]
output_destination = sys.argv[2]
on_sand = sys.argv[3]

pairs = ["KA","KW","AW"]                                                    # All material choices for a player
chosen_seed_pair = random.choice(pairs)                                     # Choose one pair for the seed
sys.stdout = open(output_destination + "/seed_strat.txt", "w")              # Generate some seed strategy
stochastic_strat.run("KA"+chosen_seed_pair, 2, config)                      # Current using stochastic seed, naive could be used here (opposing pair is irrelevant)
sys.stdout = sys.__stdout__
print("Seed strategy generated for: " + chosen_seed_pair + ", finding adversarial \
probability for all opposing pairs (this takes about a minute)")
max_likelihood = 0.0                                                        # Value for highest adversarial likelihood
best_opponent = chosen_seed_pair                                            # Identity for pair with highest adversarial likelihood
for pair in pairs:                                                          # For each ordering of each pair
    for ordering in [pair, pair[1]+pair[0]]:                                # Calculate the adversary against the seed strategy
        characters = ordering + chosen_seed_pair
        sys.stdout = open(output_destination + "/seed_v_" + ordering + ".prism", "w")
        prefix.run(characters, 0, 0, config)
        free_strat.run(characters, 1)
        print(open(output_destination + "/seed_strat.txt", "r").read())     # Copy in the adversary
        suffix.run(characters,0)
        sys.stdout = sys.__stdout__
        os.system("prism " + output_destination + "/seed_v_" + ordering + ".prism \
        properties/mdp.props -prop 1 > " + output_destination + "/log.txt")
        result_vs_seed = float(find_result(output_destination+ "/log.txt"))
        print("Against the seed strategy, " + ordering + " has an adversarial probability of: " + str(result_vs_seed))
        if result_vs_seed > max_likelihood:                                     # FIND_MAX
            max_likelihood = result_vs_seed
            best_opponent = ordering
print("Best opponent found to be: " + best_opponent + ", generating strategy")

characters = best_opponent + chosen_seed_pair
sys.stdout = open(output_destination + "/seed_v_BEST.prism", "w")
prefix.run(characters, 0, 1, config)
free_strat.run(characters, 1)
print(open(output_destination + "/seed_strat.txt", "r").read())                 # Copy in the adversary
suffix.run(characters,1)
sys.stdout = sys.__stdout__
os.system("prism " + output_destination + "/seed_v_BEST.prism properties/mdp.props -prop 1 \
        -exportadvmdp " + output_destination + "/tmp.tra -exportstates " + output_destination + "/tmp.sta \
        > " + output_destination + "/log.txt")                                  # Find the adversary from multiple initial states and export the states/transitions
sys.stdout = open(output_destination + "/adversary1.txt", "w")
adversarial_strat.run(characters, 1, output_destination+"/tmp", False)          # generate the adversary and write to file as prism code
sys.stdout = sys.__stdout__

adversarial_pair = best_opponent
adversary_count = 1                                                             # number of adversaries found
while adversary_is_unique(adversary_count):
    print("Strategy number " + str(adversary_count) + " generated, finding adversaries for all opposing pairs ...")
    max_likelihood = 0.0                                                        # Value for highest adversarial likelihood
    best_opponent = ""                                                          # Identity of pair with highest adversarial likelihood
    for pair in pairs:                                                          # For each ordering of each pair
        results = {}
        for ordering in [pair, pair[1]+pair[0]]:                                # Calculate the adversary against the last adv_strategy
            characters = adversarial_pair + ordering
            sys.stdout = open(output_destination + "/adv" + str(adversary_count) + "_v_" + ordering + ".prism", "w")
            prefix.run(characters, 0, 0, config)
            print(open(output_destination + "/adversary" + str(adversary_count) + ".txt", "r").read())     # Copy in the adversary
            free_strat.run(characters, 2)
            suffix.run(characters,0)
            sys.stdout = sys.__stdout__
            os.system("prism " + output_destination + "/adv" + str(adversary_count) + "_v_" + ordering + ".prism \
            properties/mdp.props -prop 2 -cuddmaxmem 2g > " + output_destination + "/log.txt")
            result_vs_adv = float(find_result(output_destination+ "/log.txt"))
            print("Against the last adversarial strategy, " + ordering + " has an adversarial probability of: " + str(result_vs_adv))
            results[ordering] = result_vs_adv
        if min(results.values()) > max_likelihood:                              # FIND_MAX with min P of each pair
            max_likelihood = min(results.values())
            best_opponent = min(results, key = results.get)
    print("Best opponent found to be: " + best_opponent + ", generating adversarial strategy ...")

    # Generate adversary for player 1 based on adversary for p2 of adv v best
    characters = adversarial_pair + best_opponent
    sys.stdout = open(output_destination + "/adv" + str(adversary_count) + "_v_BEST.prism", "w")
    prefix.run(characters, 0, 1, config)
    print(open(output_destination + "/adversary" + str(adversary_count) + ".txt", "r").read())
    free_strat.run(characters, 2)
    suffix.run(characters, 1)
    sys.stdout = sys.__stdout__
    os.system("prism " + output_destination + "/adv" + str(adversary_count) + "_v_BEST.prism properties/mdp.props -prop 2 \
            -exportadvmdp " + output_destination + "/tmp.tra -exportstates " + output_destination + "/tmp.sta \
            -cuddmaxmem 2g > " + output_destination + "/log.txt")
    # update adversary
    adversary_count += 1
    sys.stdout = open(output_destination + "/adversary" + str(adversary_count) + ".txt", "w")
    adversarial_strat.run(characters, 2, output_destination+"/tmp", True)       # generate the adversary and write to file as prism code
    sys.stdout = sys.__stdout__
    adversarial_pair = best_opponent
