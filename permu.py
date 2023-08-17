arr=list(input())
n=len(arr)
ans=[]
def rec(ar,path,ans):
    if len(path)==n :
        ans.append(path)
        return
    for i in range(len(ar)) :
        a=ar[:i]+ar[i+1:]
        rec(a,path+[i],ans)


rec(arr,[],ans)
print(ans)
