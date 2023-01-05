:-consult("aleph_input/train_aleph.bk").

true_class(A,Ex) :-
     molecule_has_atoms(A,B), atoms_atype(B,27),
    Ex = [molecule_has_atoms(A,B), atoms_atype(B,27)].

