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
        dict_of_likelihoods[pair] = value
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
print("Standard Deviation =",std)
print("Mean =",mu)
print("First effective strategy chosen as:", l_last_three_quarters)

print("Mu of variance for each material - KA =", KA_var, "KW =", KW_var, "AW =", AW_var)

y_equals_05 = []
for elem in range(len(x)-1):
    y_equals_05 += [0.5]

fig, ax = plt.subplots()
ax.plot(x[:-1],y, "k-.", label="Greatest adversary")
ax.plot(x[:-1],KA, "ro", label="Knight-Archer", markersize=10)
ax.plot(x[:-1],KW, "ys", label="Knight-Wizard", markersize=10)
ax.plot(x[:-1],AW, "bd", label="Archer-Wizard", markersize=10)
ax.plot(x[:-1],y_equals_05, "--",)
plt.xlabel('Iteration:Best pair')
plt.ylabel('Likelihood')
plt.xticks(rotation='vertical')
legend = ax.legend()
# Put a nicer background color on the legend.
plt.show()
