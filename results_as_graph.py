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
        print("Best pair is", best_pair + ": " + str(dict_of_likelihoods[best_pair]))
        x += [str(iteration) + ":" + best_pair]
        iteration += 1
        y += [dict_of_likelihoods[best_pair]]
        KA += [min(dict_of_likelihoods["KA"], dict_of_likelihoods["AK"])]
        KW += [min(dict_of_likelihoods["KW"], dict_of_likelihoods["WK"])]
        AW += [min(dict_of_likelihoods["AW"], dict_of_likelihoods["WA"])]
        dict_of_likelihoods = {}

    line = f.readline()

print(x)
print(y)

fig, ax = plt.subplots()
ax.plot(x[:-1],y, "k-.", label="Greatest adversary")
ax.plot(x[:-1],KA, "ro", label="Knight-Archer")
ax.plot(x[:-1],KW, "ys", label="Knight-Wizard")
ax.plot(x[:-1],AW, "bd", label="Archer-Wizard")
plt.xlabel('Iteration:Best pair')
plt.ylabel('Likelihood')
plt.xticks(rotation='vertical')
legend = ax.legend()
# Put a nicer background color on the legend.
plt.show()
