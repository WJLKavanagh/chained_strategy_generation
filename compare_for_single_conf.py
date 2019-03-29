import sys, matplotlib.pyplot as plt, numpy as np

""" Takes a file
    Returns:
        > y = array of max values
        > 3 dictionaries for m in M with:
            > material strength (average likelihood in relevant iterations)
            > win delta (average likelihood above 0.5 in winning & relevant iterations)
            > loss delta (average likelihood below 0.5 in losing & relevant iterations)
        > iterations (number of relevant iterations)
        > outplay_potential ( avg (max_f(m) - avg(f(m)), m e M )
        > seed (material pair used for seed strategy)

"""
def plot_result(file):
    y = []
    KA = []
    KW = []
    AW = []
    iteration = 1
    file = "results/" + sys.argv[1] + "/" + str(file) + ".txt"
    f = open(file, "r")
    line = f.readline()                                 # first line not used
    dict_of_likelihoods = {}                            # dictionary for all 6 results per iteration
    line = f.readline()                                 # Line details seed pair
    seed = "not found"
    while line != "":           # For line in results file
        if seed == "not found" and "Seed strategy" in line:
            seed = line.split(": ")[1].split(",")[0]
        if "probability of:" in line:                                       # If the line is an adversary
            value = float(line.strip().split("of: ")[1])                    # get the likelihood
            pair = line.strip().split("strategy, ")[1].split(" has")[0]     # get the ordering
            dict_of_likelihoods[pair] = value
        if "Best opponent" in line:
            best_pair = line.split("to be: ")[1].split(", generating")[0]
            iteration += 1
            y += [dict_of_likelihoods[best_pair]]
            KA += [min(dict_of_likelihoods["KA"], dict_of_likelihoods["AK"])]
            KW += [min(dict_of_likelihoods["KW"], dict_of_likelihoods["WK"])]
            AW += [min(dict_of_likelihoods["AW"], dict_of_likelihoods["WA"])]
            dict_of_likelihoods = {}
        line = f.readline()

    l = len(y)
    first_rel = max(2,int(l/4))                                                 # first relevant iteration
    KA_dict = {"robustness":0, "win_d":0, "loss_d":0}                           # declare returned structs
    KW_dict = {"robustness":0, "win_d":0, "loss_d":0}
    AW_dict = {"robustness":0, "win_d":0, "loss_d":0}
    mat_to_result = {"KA":[KA,KA_dict],"KW":[KW,KW_dict],"AW":[AW,AW_dict]}
    outplay = 0

    for m in ["KA","KW","AW"]:                                                  # fill material dictionaries
        mat_to_result[m][1]["robustness"] = np.mean(mat_to_result[m][0][first_rel:])
        over_point_5 = []
        under_point_5 = []
        for res in mat_to_result[m][0][first_rel:]:
            if res > 0.501: over_point_5 += [res - 0.5]                         # ignore rounding errors
            elif res < 0.499: under_point_5 += [0.5 - res]
        if len(over_point_5) > 0:  mat_to_result[m][1]["win_d"] = np.mean(over_point_5)
        else: mat_to_result[m][1]["win_d"] = 0.0
        if len(under_point_5) > 0: mat_to_result[m][1]["loss_d"] = np.mean(under_point_5)
        else: mat_to_result[m][1]["loss_d"] = 0.0

    outplays = []                                                                   # calculate outplay potential
    for it in range(first_rel, l-1):
        outplays += [y[it] - np.mean([KA[it],KW[it],AW[it]])]
    outplay_potential = np.mean(outplays)

    return y, KA_dict, KW_dict, AW_dict, (l - first_rel), outplay_potential, seed

max_l = 1
series_to_plt = {}
KA_dict = {"robustness":0, "win_d":0, "loss_d":0}                               # declare printed structs
KW_dict = {"robustness":0, "win_d":0, "loss_d":0}
AW_dict = {"robustness":0, "win_d":0, "loss_d":0}
outplay_potential = 0
seed_list = []
it_list = []

for i in range(1,int(sys.argv[2])+1):       # scrape each result file
    series_to_plt[i], new_KA, new_KW, new_AW, new_it, new_op, new_seed  = plot_result(i)
    seed_list += [new_seed]
    it_list += [new_it]
    outplay_potential += new_it*new_op
    for m in ["robustness", "win_d", "loss_d"]:
        KA_dict[m] += new_KA[m]*new_it
        KW_dict[m] += new_KW[m]*new_it
        AW_dict[m] += new_AW[m]*new_it
    if len(series_to_plt[i]) > max_l: max_l = len(series_to_plt[i])
x = ["seed"] + [range(1,max_l)]

for d in [KA_dict, KW_dict, AW_dict]:
    for m in ["robustness", "win_d", "loss_d"]:
        d[m] = d[m] / np.sum(it_list)

for elem in KA_dict.values(): print(elem)
for elem in KW_dict.values(): print(elem)
for elem in AW_dict.values(): print(elem)
print(outplay_potential / np.sum(it_list))
print(np.mean([KA_dict["robustness"], KW_dict["robustness"], AW_dict["robustness"]]))

fig, ax = plt.subplots()
for j in range(1,len(series_to_plt)+1):
    x_to_plot = ["seed"] + list(range(1,len(series_to_plt[j])))
    ax.plot(x_to_plot,series_to_plt[j], label="execution " + str(j) + " (" + seed_list[j-1] + ")")
max_x = 0
for s in series_to_plt.keys():
    max_x = max(max_x, len(series_to_plt[s]))
y_equals_05 = [0.5]*(max_x)
ax.plot(["seed"] + list(range(1,max_x)),y_equals_05, "--",)
plt.xlabel('Iteration')
plt.ylabel('Maximal Likelihood')
plt.tick_params(labelsize=18)
plt.xlabel('Iteration', fontsize=18)
plt.ylabel('Likelihood', fontsize=18)
legend = ax.legend(fontsize=28)
plt.show()
