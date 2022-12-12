:-consult("aleph_input/train_aleph.bk").

true_class(A,Ex) :-
     molecule_logp(A,3.26),
    Ex = [molecule_logp(A,3.26)].

true_class(A,Ex) :-
     molecule_ind1(A,1),
    Ex = [molecule_ind1(A,1)].

