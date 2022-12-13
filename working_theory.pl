:-consult("aleph_input/train_aleph.bk").

true_class(A,Ex) :-
     molecule_logp(A,2.29),
    Ex = [molecule_logp(A,2.29)].

true_class(A,Ex) :-
     molecule_logp(A,3.26),
    Ex = [molecule_logp(A,3.26)].

true_class(A,Ex) :-
     molecule_logp(A,4.18),
    Ex = [molecule_logp(A,4.18)].

true_class(A,Ex) :-
     molecule_logp(A,4.44),
    Ex = [molecule_logp(A,4.44)].

true_class(A,Ex) :-
     molecule_inda(A,1),
    Ex = [molecule_inda(A,1)].

true_class(A,Ex) :-
     molecule_logp(A,3),
    Ex = [molecule_logp(A,3)].

true_class(A,Ex) :-
     molecule_logp(A,2.52),
    Ex = [molecule_logp(A,2.52)].

true_class(A,Ex) :-
     molecule_logp(A,5.87),
    Ex = [molecule_logp(A,5.87)].

true_class(A,Ex) :-
     molecule_logp(A,4.69),
    Ex = [molecule_logp(A,4.69)].

true_class(A,Ex) :-
     molecule_logp(A,4.23),
    Ex = [molecule_logp(A,4.23)].

