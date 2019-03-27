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
mat_to_result = {"KA":KA,"KW":KW,"AW":AW,"max":y}           # string_descriptors : list of values
material_total = {"KA":0,"KW":0,"AW":0,"max":0}
material_over_point_5 = {"KA":[0,0],"KW":[0,0],"AW":[0,0],"max":0}
material_under_point_5 = {"KA":[0,0],"KW":[0,0],"AW":[0,0],"max":0}

incorrect_material_punish = 0

for i in range(l_last_three_quarters, l-1):             # for all representative iterations (give strategies time to 'settle')
    for m in ["KA","KW","AW","max"]:                    # for all material
        material_total[m] += mat_to_result[m][i]        # sum values
    best_pair = x[i+1].split(":")[1]                    # identify pair with greatest result
    if best_pair in ["AK", "WK", "WA"]:
        best_pair = best_pair[1] + best_pair[0]
    second_best = 0
    for m_ in ["KA","KW","AW"]:
        if m_ != best_pair:
            if mat_to_result[m_][i] > second_best:
                second_best = mat_to_result[m_][i]      # Find_max for second best value in each iteration
    incorrect_material_punish += (mat_to_result[best_pair][i] - second_best)
    for m__ in  ["KA","KW","AW"]:
        if mat_to_result[m__][i] > 0.5:
            material_over_point_5[m__][0] += (mat_to_result[m__][i] - 0.5)
            material_over_point_5[m__][1] += 1
        if mat_to_result[m__][i] < 0.5:
            material_under_point_5[m__][0] += (0.5 - mat_to_result[m__][i])
            material_under_point_5[m__][1] += 1




second_plot_x = ["KA","KW","AW","best"]
second_plot_y = []
for m in ["KA","KW","AW","max"]:                  # for all material
    if m != "max":
        if material_under_point_5[m][0] < 0.001: material_under_point_5[m][0] = 999
    value = material_total[m]/(l-l_last_three_quarters)
    second_plot_y += [value]
    print(m, "material strength \t\t=", str(value)[:6])
    if m != "max":
        if material_over_point_5[m][1] > 0:
            print(m, "material over .5 \t\t=", str(material_over_point_5[m][0]/material_over_point_5[m][1])[:6])
        else:
            print(m, "material over .5 \t\t= 0.0")
        if material_under_point_5[m][1] > 0:
            print(m, "material under .5 \t\t=", str(material_under_point_5[m][0]/material_under_point_5[m][1])[:6])
        else:
            print(m, "material under .5 \t\t= 0.0")
        print()


print("Outplay potential \t\t=", str(second_plot_y[3] - np.mean(second_plot_y[:2]))[:6])
# NOT USED: print("Incorrect material punish \t=", str(incorrect_material_punish/(l-l_last_three_quarters))[:6])

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

"""
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
"""

"""
y_equals_05 = []
for elem in range(len(x)-1):
    y_equals_05 += [0.5]

fig, (ax, ax_) = plt.subplots(1, 2, sharey=True)
ax.plot(x[:-1],y, "k-.", label="Greatest adversary")
ax.plot(x[:-1],KA, "ro", label="Knight-Archer", markersize=10)
ax.plot(x[:-1],KW, "ys", label="Knight-Wizard", markersize=10)
ax.plot(x[:-1],AW, "bd", label="Archer-Wizard", markersize=10)
ax.plot(x[:-1],y_equals_05, "--",)
ax_.bar(second_plot_x, second_plot_y)
ax_.plot(second_plot_x,[0.5,0.5,0.5,0.5], "r--",)
plt.xlabel('Iteration:Best pair')
plt.ylabel('Likelihood')
plt.xticks(rotation='vertical')
legend = ax.legend()
"""


plt.show()
