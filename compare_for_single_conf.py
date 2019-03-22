import sys, matplotlib.pyplot as plt, numpy as np

""" Takes a file
    Returns:
        > y = array of max values
        > 3 dictionaries for m in M with:
            > material strength (average likelihood in relevant iterations)
            > win delta (average likelihood above 0.5 in winning & relevant iterations)
            > loss delta (average likelihood below 0.5 in losing & relevant iterations)
        > outplay_potential ( avg (max_f(m) - avg(f(m)), m e M )

"""
def plot_result(file):
    y = []
    KA = []
    KW = []
    AW = []
    iteration = 1
    file = "results/" + sys.argv[1] + "/" + str(file) + ".txt"
    f = open(file, "r")
    line = f.readline()
    dict_of_likelihoods = {}                            # dictionary for all 6 results per iteration
    line = f.readline()                                 # Line details seed pair
    while line != "":           # For line in results file
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
    l_last_three_quarters = max(2,int(l/4))


    KA_dict = {"strength":0, "win_d":0, "loss_d":0, "over_point_5":0}           # declare returned structs
    KW_dict = {"strength":0, "win_d":0, "loss_d":0, "over_point_5":0}
    AW_dict = {"strength":0, "win_d":0, "loss_d":0, "over_point_5":0}
    mat_to_result = {"KA":[KA,KA_dict],"KW":[KW,KW_dict],"AW":[AW,AW_dict]}
    outplay = 0

    for i in range(l_last_three_quarters, l-1):                                 # Fill dictionaries with totals
        for m in mat_to_result.keys():
            mat_to_result[m][1]["strength"] += mat_to_result[m][0][i]
            if mat_to_result[m][0][i] > 0.5:
                mat_to_result[m][1]["over_point_5"] += 1
                mat_to_result[m][1]["win_d"] += (mat_to_result[m][0][i] - 0.5)
            else:
                mat_to_result[m][1]["loss_d"] += (0.5 - mat_to_result[m][0][i])
        outplay += (y[i] - np.mean([KA[i],KW[i],AW[i]]))

    for m in mat_to_result.keys():                                              # Aggregate dictionary values
        mat_to_result[m][1]["strength"] = mat_to_result[m][1]["strength"] / (l - l_last_three_quarters)
        if mat_to_result[m][1]["over_point_5"] > 0:
            mat_to_result[m][1]["win_d"] = mat_to_result[m][1]["win_d"] / mat_to_result[m][1]["over_point_5"]
        else:
            mat_to_result[m][1]["win_d"] = 0
        if mat_to_result[m][1]["over_point_5"] < (l - l_last_three_quarters):
            mat_to_result[m][1]["loss_d"] = mat_to_result[m][1]["loss_d"] / (l - l_last_three_quarters - mat_to_result[m][1]["over_point_5"])
        else:
            mat_to_result[m][1]["loss_d"] = 0

    return y, KA_dict, KW_dict, AW_dict, outplay/(l-l_last_three_quarters)

series_to_plt = {}                          # dictionary of what to plot paired with execution # keys
all_KA_dict = []                            # list of KA dictionaries
all_KW_dict = []
all_AW_dict = []
x = ["seed"]                                # x-axis
max_l = 1
outplay_potential = 0
                                   # max length of series'

for i in range(1,int(sys.argv[2])+1):       # scrape each result file
    series_to_plt[i], new_KA, new_KW, new_AW, new_op  = plot_result(i)
    all_KA_dict += [new_KA]
    all_KW_dict += [new_KW]
    all_AW_dict += [new_AW]
    outplay_potential += new_op / int(sys.argv[2])
    if len(series_to_plt[i]) > max_l: max_l = len(series_to_plt[i])

for i in range(1,max_l):                    # populate x-axis
    x += [i]

# print material results to terminal:
print()
total_strength = 0
mat_to_result = {"KA":all_KA_dict,"KW":all_KW_dict,"AW":all_AW_dict}           # string_descriptors : list of values
for m in mat_to_result.keys():                                            # Calculate values
    strength = 0
    win_d = 0
    loss_d = 0
    for entry in mat_to_result[m]:
        strength += entry["strength"]
        win_d += entry["win_d"]
        loss_d += entry["loss_d"]
    total_strength += strength
    print(m, "\nStrength = " + str(strength/len(mat_to_result[m])), \
    "win_d = " + str(win_d/len(mat_to_result[m])), \
    "loss_d = " + str(loss_d/len(mat_to_result[m])))
    print()

# print global results to terminal:
print("Game\nstrength = " + (str(total_strength/(len(mat_to_result[m])*3))), \
"outplay_potential = " + str(outplay_potential), "\n")

fig, ax = plt.subplots()
for j in range(1,len(series_to_plt)+1):
    x_to_plot = ["seed"]
    for k in range(1,len(series_to_plt[j])):
        x_to_plot += [k]
    ax.plot(x_to_plot,series_to_plt[j], label="execution " + str(j))
plt.xlabel('Iteration')
plt.ylabel('Maximal Likelihood')
# plt.xticks(rotation='vertical')
legend = ax.legend()
# Put a nicer background color on the legend.
plt.show()
