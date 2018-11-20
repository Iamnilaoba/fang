lst=[{"name":"zhangsan","age":12},
     {"name":"lisi","age":18},
     {"name":"wangwu","age":11}]

def sort(lst,key,reverse):
    for i in range(len(lst)-1):
        for j in range(len(lst)-1-i):
            a=key[lst[j]]
            b=key[lst[j+1]]
            if a>b if not reverse else a<b:
                lst[j],lst[j+1]=lst[j+1],lst[j]

sort(lst,lambda item:item['age'])
print(lst)
