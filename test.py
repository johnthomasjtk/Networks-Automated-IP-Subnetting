import sys
import json
from math import log

filename = sys.argv[1]
filedesc = open(filename)
jsondata = json.load(filedesc)
filedesc.close()

networkaddress = jsondata["network_addr"]
requiredsubnets = jsondata["subnets"]
netmask = jsondata["netmask"]

listsubnets = []
lengsub = len(requiredsubnets)
i = 1
while i <= lengsub:
	netnum = i
	numhosts = requiredsubnets[str(i)]
	numhosts += 2
	power = 0
	while numhosts > 2**power:
		power += 1
	numhosts = 2**power
	listsubnets.append((netnum, numhosts))
	i += 1


listsubnets = sorted(listsubnets, key=lambda e: e[1], reverse=True)

answerd = {}

cc = str(networkaddress)
cc = cc.split('.')
cc = [bin(int(x)) for x in cc]
cc = [x[2:] for x in cc]
cc = [x.zfill(8) for x in cc]
cc = cc[0] + cc[1] + cc[2] + cc[3]
cc = int(cc,2)

countzero = netmask
countzero = countzero.split('.')
countzero = [bin(int(x)) for x in countzero]
countzero = [x[2:] for x in countzero]
countzero = [x.zfill(8) for x in countzero]
countzero = ''.join(countzero)

cz = 0

for char in countzero:
	if char == '0':
		cz += 1

cz = 2**cz
nd = sum(x[1] for x in listsubnets)

if nd > cz:
	ans = {"success": False}
	print json.dumps(ans)
else:
	ans = {"success": True}
	for i in listsubnets:
		subnetaddr = cc
		subnetstartaddr = cc
		subnetendaddr = cc + i[1]
		subnetendaddr -= 1
		subnethosts = i[1] - 2

		#network address
		subnetaddr = bin(subnetaddr)[2:]
		subnetaddr = subnetaddr.zfill(32)
		templist1 = []
		templist1.append(int(subnetaddr[0:8],2))
		templist1.append(int(subnetaddr[8:16],2))
		templist1.append(int(subnetaddr[16:24],2))
		templist1.append(int(subnetaddr[24:32],2))
		subnetaddr = templist1
		subnetaddr = [str(x) for x in subnetaddr]
		subnetaddr = subnetaddr[0] + '.' + subnetaddr[1] + '.' + subnetaddr[2] + '.' + subnetaddr[3]
		
		#start address
		subnetstartaddr = bin(subnetstartaddr)[2:]
		subnetstartaddr = subnetstartaddr.zfill(32)
		templist2 = []
		templist2.append(int(subnetstartaddr[0:8],2))
		templist2.append(int(subnetstartaddr[8:16],2))
		templist2.append(int(subnetstartaddr[16:24],2))
		templist2.append(int(subnetstartaddr[24:32],2))
		subnetstartaddr = templist2
		subnetstartaddr = [str(x) for x in subnetstartaddr]
		subnetstartaddr = subnetstartaddr[0] + '.' + subnetstartaddr[1] + '.' + subnetstartaddr[2] + '.' + subnetstartaddr[3]
		#end address
		subnetendaddr = bin(subnetendaddr)[2:]
		subnetendaddr = subnetendaddr.zfill(32)
		templist3 = []
		templist3.append(int(subnetendaddr[0:8],2))
		templist3.append(int(subnetendaddr[8:16],2))
		templist3.append(int(subnetendaddr[16:24],2))
		templist3.append(int(subnetendaddr[24:32],2))
		subnetendaddr = templist3
		subnetendaddr = [str(x) for x in subnetendaddr]
		subnetendaddr = subnetendaddr[0] + '.' + subnetendaddr[1] + '.' + subnetendaddr[2] + '.' + subnetendaddr[3]
		
		#subnet mask
		subnetmask = netmask
		subnetmask = subnetmask.split(".")
		subnetmask = [bin(int(x)) for x in subnetmask]
		subnetmask = [x[2:] for x in subnetmask]
		subnetmask = [x.zfill(8) for x in subnetmask]
		subnetmask = subnetmask[0] + subnetmask[1] + subnetmask[2] + subnetmask[3]
		subnetmask = int(subnetmask,2)
		
		maxnum = '255.255.255.255'
		maxnum = maxnum.split('.')
		maxnum = [bin(int(x)) for x in maxnum]
		maxnum = [x[2:] for x in maxnum]
		maxnum = ''.join(maxnum)
		maxnum = int(maxnum,2)

		subnetmask = maxnum - i[1] + 1
		subnetmask = bin(subnetmask)[2:]
		templist4 = []
		templist4.append(int(subnetmask[0:8],2))
		templist4.append(int(subnetmask[8:16],2))
		templist4.append(int(subnetmask[16:24],2))
		templist4.append(int(subnetmask[24:32],2))
		subnetmask = templist4
		subnetmask = [str(x) for x in subnetmask]
		subnetmask = '.'.join(subnetmask)

		dictone = {
				"network_addr": subnetaddr,
				"netmask": subnetmask,
				"start_addr": subnetstartaddr,
				"end_addr": subnetendaddr,
				"total_host_count": subnethosts
			}

		answerd.update({str(i[0]):dictone})
		cc += i[1]
	ans.update({"subnets":answerd})
	print json.dumps(ans)
