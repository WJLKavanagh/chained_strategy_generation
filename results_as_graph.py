# When saving images please modify the subplots to the following:
# 0.10, 0.15, 0.98,.0.94, 0.20, 0.20

import sys, matplotlib.pyplot as plt, numpy as np

file = sys.argv[1]
f = open(file, "r")
x = ["seed"]
y = []
KA = []
KW = []
AW = []
iteration = 1

line = f.readline()
dict_of_likelihoods = {}                            # dictionary for all 6 results per iteration
line = f.readline()                                 # Line details seed pair
x[0] += ":" + line.split("for: ")[1].split(", ")[0]
while line != "":           # For line in results file
    if "probability of:" in line:                                       # If the line is an adversary
        value = float(line.strip().split("of: ")[1])                    # get the likelihood
        pair = line.strip().split("strategy, ")[1].split(" has")[0]     # get the ordering
        dict_of_likelihoods[pair] = value                               # Used to take lower ordering per pair, per iteration
    if "Best opponent" in line:
        best_pair = line.split("to be: ")[1].split(", generating")[0]
        #print("Best pair is", best_pair + ": " + str(dict_of_likelihoods[best_pair]))
        x += [str(iteration) + ":" + best_pair]
        iteration += 1
        y += [dict_of_likelihoods[best_pair]]
        KA += [min(dict_of_likelihoods["KA"], dict_of_likelihoods["AK"])]
        KW += [min(dict_of_likelihoods["KW"], dict_of_likelihoods["WK"])]
        AW += [min(dict_of_likelihoods["AW"], dict_of_likelihoods["WA"])]
        dict_of_likelihoods = {}
    line = f.readline()

l = len(x)
l_last_three_quarters = max(int(l/4),2)
mat_to_result = {"KA":KA,"KW":KW,"AW":AW,"max":y}           # string_descriptors : list of values
material_total = {"KA":0,"KW":0,"AW":0,"max":0}
material_over_point_5 = {"KA":[0,0],"KW":[0,0],"AW":[0,0],"max":0}
material_under_point_5 = {"KA":[0,0],"KW":[0,0],"AW":[0,0],"max":0}

for m in ["KA","KW","AW"]:                                                      # Print out material robustness and deltas
    print(m, "robustness =", np.mean(mat_to_result[m][l_last_three_quarters:]))
    over_point_5 = []
    under_point_5 = []
    for res in mat_to_result[m][l_last_three_quarters:]:
        if res > 0.501: over_point_5 += [res - 0.5]                             # ignore rounding errors
        elif res < 0.499: under_point_5 += [0.5 - res]
    if len(over_point_5) > 0:  print(m, "win delta =", np.mean(over_point_5))
    else: print(m, "win delta = 0.0")
    if len(under_point_5) > 0: print(m, "loss delta =", np.mean(under_point_5))
    else: print(m, "loss delta = 0.0")
print()

outplays = []                                                                   # calculate outplay potential
for it in range(l_last_three_quarters-1, l-1):
    outplays += [y[it] - np.mean([KA[it],KW[it],AW[it]])]
print("Outplay potential =", np.mean(outplays))
print("Game robustness =", np.mean(KA[l_last_three_quarters:] + KW[l_last_three_quarters:] + AW[l_last_three_quarters:]))

y_equals_05 = [0.5]*(len(x)-1)                                                  # to plot y=0.5
fig, ax = plt.subplots()
ax.plot(x[:-1],y, "k-.", label="Greatest adversary")
ax.plot(x[:-1],KA, "ro", label="Knight-Archer", markersize=10)
ax.plot(x[:-1],KW, "ys", label="Knight-Wizard", markersize=10)
ax.plot(x[:-1],AW, "bd", label="Archer-Wizard", markersize=10)
ax.plot(x[:-1],y_equals_05, "--",)
plt.tick_params(labelsize=18)
plt.xlabel('Iteration', fontsize=18)
plt.ylabel('Likelihood', fontsize=18)
legend = ax.legend(fontsize=24)
plt.xticks(rotation='vertical')
plt.show()
