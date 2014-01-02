typedef long long ll;

const int MAX_N = 100000;

// INPUT
int n, a[MAX_N]

//BIT Binary Indexed Tree
//  1-indexed array 
// sum(i) := a1 + a2 + ... + ai
// add(i,x) : ai += x

// last 1bit of i == i & -i
// i - last 1bit == i - (i&-i) = i & (i-1)

//[1,n]

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

void solve(){
  ll ans = 0;
  for (int j=0; j < n; j++){
    ans += j - sum(a[j]);
    add(a[j], 1);
  }
  printf("%lld\n", ans);
}
