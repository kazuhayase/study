#include <cstdio>
#include <vector>
using namespace std;

typedef long long ll;

//INPUT
vector<int> A;

ll merge_count(vector<int> &a){
  int n = a.size();
  if (n <= 1) return 0;

  ll cnt = 0;
  vector<int> b(a.begin(), a.begin() + n/2);
  vector<int> c(a.begin() + n/2, a.end());

  cnt += merge_count(b);
  cnt += merge_count(c);

  int ai = 0, bi = 0, ci = 0;
  while (ai < n) {
    if (bi < b.size() && (ci == c.size() || b[bi] <= c[ci])) {
      a[ai++] = b[bi++];
    } else {
      cnt += n/2 - bi;
      a[ai++] = c[ci++];
    }
  }
  return cnt;
}

void solve(){
  printf("%lld\n", merge_count(A));
}

int main(){
  A.clear();
  int a0_org[] = {1,2,3,4};
  vector<int> a0(a0_org, end(a0_org));
  A.insert(A.end(), a0.begin(), a0.end());
  solve();

  A.clear();
  int a1_org[] = {1,3,2,4};
  vector<int> a1(a1_org, end(a1_org));
  A.insert(A.end(), a1.begin(), a1.end());
  solve();

  A.clear();
  int a2_org[] = {3,1,2,4};
  vector<int> a2(a2_org, end(a2_org));
  A.insert(A.end(), a2.begin(), a2.end());
  solve();

  A.clear();
  int a3_org[] = {4,3,2,1};
  vector<int> a3(a3_org, end(a3_org));
  A.insert(A.end(), a3.begin(), a3.end());
  solve();



}
