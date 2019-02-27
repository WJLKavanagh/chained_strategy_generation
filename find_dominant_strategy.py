# William Kavanagh, Feb 2019
# Identifies dominant strategies in RPGLite for a given configuration
# USAGE: ???

import prefix, free_strat, adversarial_strat, suffix, stochastic_strat

# USAGE OF IMPORTED FILES:
# prefix.run([characters], smg?, multiple_init?, config_suffix)
# free_strat.run([characters], player#)
# adversarial_strat.run([characters], player#, adv_file_prefix)
# suffix.run([characters], multiple_init?)


characters = ["K", "A", "K", "W"]
prefix.run(characters, 0, 0, "a")
stochastic_strat.run(characters, 1, "a")
free_strat.run(characters, 2)
suffix.run(characters, 0)
