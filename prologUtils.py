def add_constraint(constraint_predicate, dataset = 'train'):
    """Currently just removes a predicate from a theory"""
    output_directory = 'trainFiles'
    bk_file = open(output_directory + '/' + dataset + '_aleph.b', 'a')
    bk_file.write(f"false :- hypothesis(_,Body,_), bodyList(Body, List), !, member({constraint_predicate}(_,_), List).\n\n")
    
    bk_file.close()