dx = [-1,0,1,0]
dy = [0,-1,0,1]

def solve(field,x,y,W,H):
    Q = list()
    Q.append((x,y,0))
    visited = set()
    visited.add((x,y))
    
    while(Q):
        p = Q.pop(0)
        for i in range(4):
            nx = p[0] + dx[i]
            ny = p[1] + dy[i]
            if 0<=nx<W and 0<=ny<H:
                if not (nx,ny) in visited:
                    if field[(nx,ny)] == 'x':
                        return p[2]+1
                    else:
                        Q.append((nx, ny, p[2]+1))
                        visited.add((nx,ny))
    
    return -1

def main():
    H, W = map (int, input().split())
    sx, sy = map(int, input().split())
    field = dict()
    for y in range(W):
        row = input().split()
        for x in range(H):
            field[(x,y)] = row[x]
    print(solve(field,sx,sy,W,H))

if __name__ == '__main__':
    main()

