class etc:
	def __init__(self):
		return None
	dice=[1,2,3,4,5,6]
	coin=[0,1]
class percentage:
	def __init__(self):
		return None
	def Factorial(self,n):
		j=1
		for i in range(1,n+1):
			j=j*i
		return j
	def nPr(self,n,r):
		return self.Factorial(n)/self.Factorial(n-r)
	def nCr(self,n,r):
		return self.nPr(n,r)/self.Factorial(r)
	def AnB(self,A,B):
		C=[]
		for i in range(len(A)):
			for j in range(len(B)):
				if A[i]==B[j]:
					C=C+[B[j]]
		return C 
	def Ac(self,A,S):
		S2=list(S)
		for i in A[:]:
			S2.remove(i)
		return S2
	def AUB(self,A,B):
		C=A+B
		D=self.AnB(A,B)
		for i in D[:]:
			C.remove(i)
		C.sort()
		return C
	def AEB(self,A,B):
		n=0
		for i in A[:]:
			for j in B[:]:
				if i == j:
					n=n+1
		if n == len(A) and len(A)>1:
			return True
		return False
		
	def AcB(self,A,B):
		n=0
		for i in A[:]:
			for j in B[:]:
				if i == j:
					n=n+1
		if n == len(A):
			return True
		return False
	def P(self,A,S):
		if self.AcB(A,S):
			return float(len(A))/float(len(S))
		else:
			return 0
	def P_BlA(self,A,B,S):
		return self.P(self.AnB(A,B),S)/self.P(A,S)
	def nPIr(self,n,r):
		j=1
		for i in range(0,r):
			j=j*i
		return j
	def nHr(self,n,r):
		return self.nCr(n+r-1,r)
	def AmB(self,A,B,S):
		C=self.Ac(B,S)
		return self.AnB(A,C)
class statistics:
    def __init__(self):
        return None
    def autoconfigure(self,n,P):
        li=[]
        for i in range(0,n+1):
            p=percentage()
            li.append([i,percentage.nCr(p,n,i)*(P**i)*((1-P)**(n-i))])
        return li
    def into_graph(self,li):
        s="X     |"
        s2="P(X=x)|"
        for i in li:
            s=s+str(i[0])+"     "
            s2=s2+str(format(i[1],".3f"))+" "
        print(s +"|sum\n"+"---------------------------------------------------------------------\n"+s2+"|1")
    def P_cond(self,li,cond):
        c2=0;
        c3=0;
        if ">=" in cond:
            c=cond.split("=")
            c2=int(c[1])
            for i in li:
                if i[0]>=c2:
                    c3+=i[1]
        if ">" in cond:
            c=cond.split(">")
            c2=int(c[1])
            for i in li:
                if i[0]>c2:
                    c3+=i[1]
        if "<=" in cond:
            c=cond.split("=")
            c2=int(c[1])
            for i in li:
                if i[0]<=c2:
                    c3+=i[1]
        if "<" in cond:
            c=cond.split("<")
            c2=int(c[1])
            for i in li:
                if i[0]<c2:
                    c3+=i[1]
        if "=" in cond:
            c=cond.split("=")
            c2=int(c[1])
            for i in li:
                if i[0]==c2:
                    c3+=i[1]
        return c3