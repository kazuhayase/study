dx=(1,1,0,-1,-1,0)
dy=(0,1,1,0,-1,-1)

def solve(startX, startY, obstacles, turn):
    Q = list()
    Q.append((startX, startY,0))
    visited = set()
    visited.add((startX, startY))
    
    while(Q):
        p = Q.pop(0)
        for i in range(6):
            x = p[0] + dx[i]
            y = p[1] + dy[i]
            t = p[2] + 1
            
            if t > turn:
                continue
            
            if (x,y) in obstacles:
                continue
            
            if (x,y) in visited:
                continue
            
            visited.add((x,y))
            Q.append((x,y,t))
            
    return len(visited)

def main():
    while True:
        t, n = map(int, input().split())  
        if t == 0 and n == 0:
            break
        obstacles = set()
        for i in range(n):
            x, y = map(int, input().split())
            obstacles.add((x,y))
        startX, startY = map(int, input().split())
        print(solve(startX, startY, obstacles, t))    


if __name__ == '__main__':
    main()
    