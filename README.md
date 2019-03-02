# chained_adversary_generation
Work on using probabilistic model checking to analyse game balance

This work can be run locally on any machine with Prism-Games (4.4.dev) accessible via '$ prism' on command-line. Alternatively, it can be run on Sand, which will use an extended version of Prism that identifies multiple equivalent adversarial strategies.

## Tool 1: Finding dominant strategies:

```$ python find_dominant_strategy.py configuration output_destination on_sand?```

example:  

```python find_dominant_strategy.py "a" output/test 0```

args:
* configuration: string which is added to "config_" and ".txt" to give a file name in configurations/
* output_destination: file location used to store all output files, includes all models, optimal strategies and a log file
* on_sand: boolean of whether to run using extended Prism on Sand and use extra memory, otherwise it will use _$ prism_ to call Prism with default memory allocation.

Find_dominant_strategy will generate 3 optimal strategies, one for each pair, when played against an opponent using the same material. It will then calculate the adversary of each strategy with all 4 orderings of different material. If all adversaries have a likelihood of winning of less than 0.5 against any optimal strategy, then that optimal strategy is **dominant**.
