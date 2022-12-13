def add_constraint(constraint_predicate, dataset = 'mutag188'):
    """
    Currently just removes a predicate from a hypothesis
    Path included so requires editing 
    """
    bk_file = open('./data/mutag188/mutag188.b', 'a')
    bk_file.write(f"\nfalse :- hypothesis(_,Body,_), bodyList(Body, List), !, member({constraint_predicate}(_,_), List).\n\n")
    
    bk_file.close()

def add_positive(example_num, dataset='mutag188'):
    """
    Currently just adds an example to the positives file.
    We need to implement something that checks whether the example already exists there
    and something that removes the example from the negative file. 
    """
    print("Hello")
    file = open('./data/mutag188/mutag188.f', 'a')
    file.write(f"\ntrue_mutagenic(d{example_num}).\n")
    
    file.close()