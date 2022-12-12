def add_constraint(constraint_predicate, dataset = 'train'):
    """
    Currently just removes a predicate from a hypothesis
    Path included so requires editing 
    """
    bk_file = open('./data/mutag188/mutag188.b', 'a')
    bk_file.write(f"\nfalse :- hypothesis(_,Body,_), bodyList(Body, List), !, member({constraint_predicate}(_,_), List).\n\n")
    
    bk_file.close()