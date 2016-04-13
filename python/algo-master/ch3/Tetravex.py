from collections import namedtuple

Piece = namedtuple('Piece', 'u d l r')

def dfs(field, used, pieces, H, W, pos):
    if pos == H * W:
        return True
    y = int(pos / W)
    x = pos % W

    for i in range(H*W):
        if used[i]:
            continue
        if x>0 and pieces[i].l != field[y][x-1].r:
            continue
        if y>0 and pieces[i].u != field[y-1][x].d:
            continue
        used[i] = True
        field[y][x] = pieces[i]
        if dfs(field, used, pieces, H, W, pos + 1):
            return True
        used[i] = False
        
    return False

def solve(pieces, H, W):
    field = [[Piece(0,0,0,0) for i in range(W)] for j in range(H)]
    used = [False for i in range(W*H)]
    
    return dfs(field, used, pieces, H, W, 0)

def main():
    while True:
        H, W = map(int, input().split())  
        if H == 0 and W == 0:
            break
        pieces = [Piece(0,0,0,0) for i in range(W*H)]
        for i in range(H):
            for j in range(W):
                u,d,l,r = map(int, input().split())

                pieces[i*W + j] = Piece(u,d,l,r)

        if solve(pieces, H, W):
            print ("Yes")
        else :
            print ("No")
            
if __name__ == '__main__':
    main()
    
