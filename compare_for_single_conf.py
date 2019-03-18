import sys, matplotlib.pyplot as plt, numpy as np




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
    KA_total_var = 0
    KW_total_var = 0
    AW_total_var = 0
    for i in range(l_last_three_quarters, l-1):
        KA_total_var += y[i] - KA[i]
        KW_total_var += y[i] - KW[i]
        AW_total_var += y[i] - AW[i]
    KA_var = KA_total_var / l_last_three_quarters
    KW_var = KW_total_var / l_last_three_quarters
    AW_var = AW_total_var / l_last_three_quarters

    std = np.std([KA_var, KW_var, AW_var], dtype=np.float64)
    mu = np.mean([KA_var, KW_var, AW_var])
    return y, std, mu

series_to_plt = {}
x = ["seed"]
max_l = 0
list_of_mu = []
list_of_std = []
for i in range(1,int(sys.argv[2])+1):
    series_to_plt[i], new_mu, new_std  = plot_result(i)
    list_of_mu += [new_mu]
    list_of_std += [new_std]
    if len(series_to_plt[i]) > max_l: max_l = len(series_to_plt[i])


for i in range(1,max_l):
    x += [i]


for i in range(len(list_of_mu)):
    print("Series", i+1, "\t- mean =", str(list_of_mu[i])[:6], "std =", str(list_of_std[i])[:6])
print("~~~"*15)
print("Mean of \t- mean =", str(np.mean(list_of_mu))[:6], "std =", str(np.mean(list_of_std))[:6])

fig, ax = plt.subplots()
for j in range(1,len(series_to_plt)+1):
    x_to_plot = ["seed"]
    for k in range(1,len(series_to_plt[j])):
        x_to_plot += [k]
    ax.plot(x_to_plot,series_to_plt[j], label="series " + str(j))
plt.xlabel('Iteration')
plt.ylabel('Maximal Likelihood')
# plt.xticks(rotation='vertical')
legend = ax.legend()
# Put a nicer background color on the legend.
plt.show()
