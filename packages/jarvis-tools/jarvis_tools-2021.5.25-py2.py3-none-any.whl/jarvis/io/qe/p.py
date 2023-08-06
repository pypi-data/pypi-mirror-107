f=open('p','r')
lines=f.read().splitlines()
f.close()
hartree_to_ev = 27.2113839
info={}
from collections import defaultdict
mem=defaultdict()
for i in lines:
    tmp=i.split()
    info={}
    info['jid']='na'
    info['energy']=hartree_to_ev*float(tmp[2])
    mem[tmp[1]]=info

from jarvis.db.jsonutils import dumpjson
dumpjson(data=mem,filename='unary_qe_tb.json')

