
global result
result = [] 

def permutation(li):
if li == [] or li == None:
    return

if len(li) == 1:
    result.append(li[0])
    print result
    result.pop()
    return

for i in range(0,len(li)):
    result.append(li[i])
    permutation(li[:i] + li[i+1:])
    result.pop()    
