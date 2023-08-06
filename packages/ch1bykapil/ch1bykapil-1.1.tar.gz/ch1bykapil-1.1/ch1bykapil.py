"""#print("kapil")
dhingra = ["kd", "pd", "sd"]
print(dhingra[1])
print(dhingra.append("hg"))
dhingra.pop()
dhingra.insert(1,"nd")
dhingra.insert(0,"hgd")
dhingra.extend(["azan", "rahat"])
print("new values: "+ str(dhingra))
print(dhingra.remove("kd"))
print(dhingra)
count=1
for member in dhingra:
    print(str(count) + " " + str(member))
    count+=1
dhingra=["kd","pd",["azan","rahat"]]
for member in dhingra:
    if (isinstance(member, list)):
        for small_member in member:
            print(small_member)
    else:
         print (member)
for num in range(4):
    print(num)
dhingraupdate=enumerate(dhingra,1)
print(list(dhingraupdate))


dhingra=["kd","pd",["azan",["rahat",["pd"],"afreen"]]]
def nestedlist (getlist,iden=False,level=0):
    for itemsingetlist in getlist:
        if iden==False:
            if (isinstance(itemsingetlist, list)):
                nestedlist(itemsingetlist)
            else:
                print(itemsingetlist)
        else:
            if (isinstance(itemsingetlist, list)):
                nestedlist(itemsingetlist,True,level+1)
            else:
                for item in range(level):
                    print("\t", end="")
                print(itemsingetlist)

nestedlist(dhingra,False)
"""
dhingra=["kd","pd",["azan",["rahat",["pd"],"afreen"]]]
def nestedlist (getlist,iden=False,level=0):
    for itemsingetlist in getlist:
        if (isinstance(itemsingetlist, list)):
            nestedlist(itemsingetlist,iden,level+1)
        else:
            if iden:
                for item in range(level):
                    print("\t", end="")
            print(itemsingetlist)

nestedlist(dhingra,False,4)