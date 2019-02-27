import prefix, free_strat, adversarial_strat, suffix

characters = ["K", "A", "K", "A"]
prefix.run(characters, 0, 0, "a")
adversarial_strat.run(characters, 1, "tmp")
free_strat.run(characters, 2)
suffix.run(characters, 0)
