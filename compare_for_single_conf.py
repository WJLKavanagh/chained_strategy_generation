import sys, matplotlib.pyplot as plt, numpy as np




def plot_result(file):
    y = []
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
            dict_of_likelihoods = {}
        line = f.readline()
    return y

series_to_plt = {}
x = ["seed"]
max_l = 0
for i in range(1,int(sys.argv[2])+1):                                                        # Change the second arg of range to one greater than the number of results for the configuration
    series_to_plt[i] = plot_result(i)
    if len(series_to_plt[i]) > max_l: max_l = len(series_to_plt[i])


for i in range(1,max_l):
    x += [i]

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
