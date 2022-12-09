false :- hypothesis(_,Body,_), bodyList(Body, List), !, member(short(B)(_,_), List).

false :- hypothesis(_,Body,_), bodyList(Body, List), !, member(short(B)(_,_), List).

false :- hypothesis(_,Body,_), bodyList(Body, List), !, member(has_car(A,B),(_,_), List).

false :- hypothesis(_,Body,_), bodyList(Body, List), !, member(closed(B)(_,_), List).

