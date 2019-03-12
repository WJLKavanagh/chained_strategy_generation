# chained_adversary_generation
Work on using probabilistic model checking to analyse game balance

This work can be run locally on any machine with [Prism-Games](https://www.prismmodelchecker.org/games/) accessible via '$ prism' on command-line. Alternatively, it can be run on Sand, which will use an extended version of Prism that identifies multiple equivalent adversarial strategies.

## Notes:

* Everything should run locally on atleast a fairly powerful laptop. 
* You will need to make the folder used as the output destination before running ($ mkdir output/results)
* Feel free to make more configurations following the format used for **a** and **b**.
* If you run any programs fully then please add them to the results folder. Tool 1 is deterministic so only file is needed for each configuration, but tool 2 isn't and more data is always nice. If you copied the full terminal output including the line that called the program into a new file in *results/**config**/**date_and_time**.txt* that would be appreciated.

## Todo:

* Sand functionality not yet added. Working on having the Sand version (final arg = True) be able to detect multiple equivalent adversaries with identical likelihoods.

## Tool 1: Finding dominant strategies:

```$ python find_dominant_strategy.py configuration output_destination on_sand?```

example:  

```python find_dominant_strategy.py "a" output/test 0```

args:
* configuration: string which is added to "config_" and ".txt" to give a file name in configurations/
* output_destination: file location used to store all output files, includes all models, optimal strategies and a log file
* on_sand: boolean of whether to run using extended Prism on Sand and use extra memory, otherwise it will use _$ prism_ to call Prism with default memory allocation.

find_dominant_strategy will generate 3 optimal strategies, one for each pair, when played against an opponent using the same material. It will then calculate the adversary of each strategy with all 4 orderings of different material. If all adversaries have a likelihood of winning of less than 0.5 against any optimal strategy, then that optimal strategy is **dominant**.

## Tool 2: Finding dominanted material

```$ python find_dominanted_material.py configuration output_destination on_sand?```

example:

```python find_dominated_material.py "a" "output/10_3" False```

args same as for tool 1

find_dominanted_material will generate a stochastic seed strategy for one of the pairs chosen stochastically at run-time. The adversary of that strategy for each ordering of each pair is then calculated and the pair that has the highest maximal likelihood is used to generate a padded version of the strategy. This strategy is then used as the adversaries for each ordering against it is calculated and the best is generated. This process continues whilst the strategies generated are new to that execution. Should a strategy be generated that has been generated before, then the program will terminate detailing which strategies are identical. The output will need to be analysed manually in order to analyse whether any material is dominated. If the adversarial orderings are consistently from the same material then it is fair to assume that that material is dominating the other.

