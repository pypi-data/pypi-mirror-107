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
"""
dhingra=["kd","pd",["azan",["rahat",["pd"],"afreen"]]]
def nestedlist (getlist):
    for itemsingetlist in getlist:
        if (isinstance(itemsingetlist, list)):
            nestedlist(itemsingetlist)
        else:
             print(itemsingetlist)
nestedlist(dhingra)
