:-consult("aleph_input/train_aleph.bk").

true_class(A,Ex) :-
     has_car(A,B), short(B), closed(B),
    Ex = [has_car(A,B), short(B), closed(B)].

