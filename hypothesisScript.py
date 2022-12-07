
def clean_theory(theory):
    clean_theory = []
    for i in range(0,len(theory)-1):
        if ':-' not in theory[i+1]:
                rule = theory[i].strip().replace('\n', '') + ' ' + theory[i+1].strip().replace('\n', '')
                clean_theory.append(rule)
    
    return clean_theory

def merge_lines(clean_theory):
    # Tidy up to ensure all rules begin with head :- body
    full_theory = []
    if len(clean_theory) > 1:
        for i in range(0,len(clean_theory)-1):
            if ':-' not in clean_theory[i+1]:
                    rule = clean_theory[i] + ' ' + clean_theory[i+1]
                    full_theory.append(rule)
            elif ':-' in clean_theory[i]:
                full_theory.append(clean_theory[i])

    else:
        full_theory = clean_theory

    return list(set(full_theory))

def remove_duplicates(seq): 
   # order preserving
   noDupes = []
   [noDupes.append(i) for i in seq if not noDupes.count(i)]
   return ' '.join(noDupes)
   
def translate_theory(dataset, filename = 'working_theory.pl'):

    with open(f'{dataset}_theory.txt') as f:
        theory = f.readlines()
    
    theory = clean_theory(theory)
    theory = merge_lines(theory)
    theory = [remove_duplicates(rule.split(' ')) for rule in theory] # remove duplicates

    save_ruleset_to_prolog(dataset, filename, theory)
    return theory

def add_constraint(dataset, constraint_predicate):
    """Currently just removes a predicate from a theory"""
    output_directory = 'aleph_input'
    bk_file = open(output_directory + '/' + dataset + '_aleph.bk', 'a')
    bk_file.write(f"false :- hypothesis(_,Body,_), bodyList(Body, List), !, member({constraint_predicate}(_,_), List).\n\n")
    
    bk_file.close()

def ilp_induce(dataset, prolog):
    # generate initial ILP thoery and save to a file
    prolog.consult('aleph6.pl')
    list(prolog.query(f"read_all('aleph_input/{dataset}_aleph')."))
    list(prolog.query("induce."))
    list(prolog.query(f"write_rules('{dataset}_theory.txt')."))

def ilp_induce_incremental(dataset, prolog):
    # generate initial ILP thoery and save to a file
    prolog.consult('aleph6.pl')
    list(prolog.query(f"read_all('aleph_input/{dataset}_aleph')."))
    list(prolog.query("induce_incremental."))
    list(prolog.query(f"write_rules('{dataset}_theory.txt')."))

def save_ruleset_to_prolog(dataset, filename, full_theory):
    file = open(filename, 'w')
    file.write(f':-consult("aleph_input/{dataset}_aleph.bk").\n')
    file.write("\n")

    for rule in full_theory:
        head = 'true_class(A,Ex) :-'
        body = rule.rpartition(':-')[2][:-1]

        file.write(head + "\n")
        file.write("    " + body + ",\n")
        file.write("    Ex = " + f"[{body.strip()}].\n")
        file.write("\n")

    file.close()        


if __name__ == "__main__":
    theory = translate_theory(dataset = 'train')
    print(theory)