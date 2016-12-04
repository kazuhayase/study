field=dict()
n=0
m=0

def pf():
    print("-----")
    for j in range(n):
        ln = ''
        for i in range(m):
            ln += field[(i,j)]
        print(ln)
    print("-----")

def dfs(x, y):
    field[(x,y)]='.'
    for dx in range(-1,2):
        for dy in range(-1,2):
            nx = x+dx
            ny = y+dy
            if 0 <=nx and nx < m and 0<=ny and ny < n and field[(nx,ny)] == 'W':
                dfs(nx,ny)

if __name__ == '__main__':
    n=int(input())
    m=int(input())
    for j in range(n):
        st = input()
        for i in range(m):
            field[(i,j)]=st[i]
    res=0
    for j in range(n):
        for i in range(m):
            if field[(i,j)] == 'W':
                dfs(i,j)
                res += 1
                pf()
    print("{}".format(res))
    