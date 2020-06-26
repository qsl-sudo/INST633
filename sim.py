from random import random
def simulation():
    graph={'A':0,'B':0,'C':0,'D':1,'E':0,'F':0,'G':0,'H':0,'I':0,'J':0}
    adj=[{'A','B'},{'A','C'},{'B','C'},{'B','D'},{'C','D'},{'C','E'},{'D','E'},{'E','F'},{'E','G'},{'G','H'},{'C','H'},{'G','I'},{'G','J'},{'I','J'}]
    newInfected=set()
    #init
    round=0
    newInfected.add('D')
    if random()<=0.8:
        graph['H']=1
        newInfected.add('H')
    #3 round
    round=1
    while round<=3:
        recentInfected=newInfected
        newInfected=set()
        for node in recentInfected:
            for edge in adj:
                if node in edge and random()<=0.7:
                    newInfected=newInfected.union(edge)-recentInfected
        if len(newInfected)>0:
            for node in newInfected:
                graph[node]=1
        round=round+1
    return graph

def play(ttl):
    cnt=1
    result={'A':0,'B':0,'C':0,'D':0,'E':0,'F':0,'G':0,'H':0,'I':0,'J':0}
    while cnt<=ttl:
        curr=simulation()
        for n in curr:
            result[n]=curr[n]+result[n]
        cnt=cnt+1
    for n in result:
        result[n]=result[n]/ttl
    print(str(ttl)+' times of simulations\nAVG: ')
    print(result)


play(10000)
