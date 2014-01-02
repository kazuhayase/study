//BIT Binary Indexed Tree
//  1-indexed array 
// sum(i) := a1 + a2 + ... + ai
// add(i,x) : ai += x

// last 1bit of i == i & -i
// i - last 1bit == i - (i&-i) = i & (i-1)

//[1,n]

const int MAX_N = 100000;
int bit[MAX_N + 1],n;

int sum(int i){
  int s = 0;
  while(i > 0){ 
    s += bit[i];
    i -= i & -i;
  }
  return s;
}

void add(int i, int x){
  while(i <= n){
    bit[i] += x;
    i += i & -i;
  }
}
