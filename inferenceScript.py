from pyswip import Prolog

prolog = Prolog()
prolog.consult('acuityFiles/Version6/aleph6.pl')
list(prolog.query(f"read_all('data/mutag188/mutag188')."))
list(prolog.query(f"induce."))
list(prolog.query(f"write_rules('train_theory.txt')."))

