<p align="center"><a href="https://pypi.org/project/readme-md/">readme-md</a> install: [sudo] pip install percstat</p>
<p>NOTICE:the percentage library only use abpout percentage. </p>
<p>if you want to use percentage and statistics, you re welcome!</p>
<p>it is open source(even commercial use!)!</p>
<p>function list:</p>
<p>class       function(type,argument(if function)) returns    value</p>
<p>etc coin(variable(list))        -           [0,1]</p>
<p>etc dice(variable(list))        -           [1,2,3,4,5,6]</p>
<p>percentage Factorial(function,integer n) n<em>(n-1)</em>...<em>2</em>1    - </p>
<p>percentage nPr(function,integer n,integer r) Factorial(n)/Factorial(n-r) - </p>
<p>percentage nCr(function,integer n,integer r) nPr(n,r)/Factorial(r) -</p>
<p>percentage AnB(function,list A,list B) intersection of A and B -</p>
<p>percentage Ac(function,list A,list S) complementary set of A in S -</p>
<p>percentage AUB(function,list A,list B) union A and B</p>
<p>percentage AEB(function,list A,list B) true if A is in B    -</p>
<p>percentage AcB(function,list A,list B) same as AEB, but len(A) is 1 -</p>
<p>percentage P(function,list A,list S) percentage of A if A is in S -</p>
<p>percentage P_BlA(function,list A,list B,list S) P(AnB,S)/P(A,S) -</p>
<p>percentage nPIr(function,integer n,integer r) n power r -</p>
<p>percentage nHr(function,integer n,integer r) nCr(n+r-1,r)    -</p>
<p>percentage AmB(fuunction,list A,list B,list S) AnB(A,Ac(B,S))</p>
<p>statistics autoconfigure(function,integer n,float P) list(n,percentage) -</p>
<p>statistics into_graph(function,list li) autoconfigured list intoi graph -</p>


