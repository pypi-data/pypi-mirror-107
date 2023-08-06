""""""""
percstat
""""""""

percstat is used when you calculate percentage and statistics

==============
Installation:`
==============

- Use the package manager [pip]
- (https://pip.pypa.io/en/stable/) to install percstat.

```
pip install percstat
```

===========
Changelogs:
===========

changelogs:
::

    v0.0.0b1~25:beta,not added statistics
    v0.0.1a1~4:alpha,first release,added statistics
    edited readme.md

=======
Usage:
=======

```
import percstat.percstat as p
```

- other not means “other”! other means a,b,c,…(For example)
- class etc

how to use:
::

    a=p.etc.dicevalue=[1,2,3,4,5,6],change a to other 
    b=p.etc.coinvalue=[0,1],change b to other
    #class percentage
    c=p.percentage.Factorial(n)  #n is integer, change c to other, returns n*(n-1)*…*2*1
    d=p.percentage.nPr(n,r) #n and r is integer, change d to other,  returns Factorial(n)/Factorial(n-r)
    e=p.percentage.nCr(n,r) #n and r is integer, change e to other,  returns nPr(n,r)/Factorial(r)
    f=p.percentage.AnB(A,B) # A and B is list, change f to other, returns intersection of A and B
    g=p.percentage.Ac(A,S) # A and S is list, change g to other, returns compliment of A in S
    h=p.percentage.AUB(A,B) # A and B is list, change h to other, returns union of A and B
    i=p.percentage.AEB(A,B) # A is Element , B is list, change i to other, returns true if A is in B
    j=p.percentage.AcB(a,b) # A is Element that type is list, B is list, change j to other, returns true if A is in B
    k=p.percentage.P(A,S) # A is Element, S is list change k to other, returns percentage pf A in S
    l=p.percentage.P_BlA(A,B,S) # A and B is Element but, B must in A, S is list, change l to other, returns conditional Probability of B in A
    m_=p.percentage.nPIr(n,r) #n and r is integer, change m_ to other, returns n**r
    n_=p.percentage.nHr(n,r) # n and r is integer, change n_ to other, returns nCr(n+r-1,r)
    o=p.percentage.AmB(A,B,S) #A and B is list, change o to other, returns difference of A and B in S(A-B)
    #class statistics
    p_=p.statistics.autoconfigure(n,P) #n is integer, P is float (nmore than 0 and less than 1) , change p_ to other,returns list that configured(rule:nCr(n,r)*(P**r)*((1-P)**(n-r))) 0 to n, r is another variable that don’t need to declare.
    p.statistics.into_graph(li) #li is list(use autoconfigure(n,P)),print   graphs with rules.
    q=p.P_cond(li,cond) # li is list(use autoconfigure(n,P)),cond is string, returns percentage based on cond(condition,ex: “a>8” means select more than 8 in graph and returns sum of these. and you can multiply these conditional sentence with “&” (ex:”a<7&a>9” means select less than 7 and more than 9 in graph and get sum.)),don’t allow like a<x<b or etc.
    r_=p.statistics.E_X(li) #returns averages of autoconfigured list.
    s=p.statistics.V_X(li) #returns variations of autoconfigured list.
    t=p≥statistics.sigma_X(li) #returns square root of V_X(li)
    u=p.statistics.convert_NXtoNZ(x,m,sigma)#
    v=p.statistics.configure_N(x,m,sigma) #
    w=p.statistics.autoconfigure_N(a,b,m,sigma)#returns calculated percentage based on sigma and m(same as E_X(li)) in range a and b (a<=x<=b)

========
License:
========
 - BSD license
 - see (https://choosealicense.com/licenses/bsd)  
 - free to use even commercial!!