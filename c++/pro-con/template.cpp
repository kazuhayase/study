#include <cstdio>
#include <climits>
#include <cmath>
#include <iostream>
#include <algorithm>
#include <map>
#include <set>
#include <vector>
#include <string>

typedef vector<int> vec;
typedef vector<vec> mat;
typedef long long ll;
typedef unsigned long long ull;

using namespace std;

const int MAX_N = 50;
const int INF = std::numeric_limits<int>::max(); //2,147,483,647 == 2^31 -1

template <typename T>
void FILL_(void* ptr, size_t size, T value) {
  std::fill((T*)ptr, (T*)ptr + size, value);
}

//INPUT

int n;
int A[MAX_N];

void solve(){

  int ans=0;
  printf("%d\n", ans);

}

int main(){
  solve();
  return 0;
}

