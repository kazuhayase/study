#include<string>
#include<iostream>
using namespace std;

typedef unsigned long long ull;

const ull B = 100000007;

//INPUT
string Astr,Bstr;

// Is A in B?
bool contain(string a, string b){
  int al = a.length(), bl = b.length();
  if (al > bl) return false;

  // B to the al-th
  ull t=1;
  for(int i=0; i<al; i++) t *= B;
  
  // hash compuation of the heads of length al for A, B
  ull ah=0, bh=0;
  for (int i=0; i<al; i++) ah = ah * B + a[i];
  for (int i=0; i<al; i++) bh = bh * B + b[i];

  // rolling hash for B
  for (int i=0; i+al <= bl; i++){
    if (ah == bh) return true;
    if (i + al < bl) bh = bh * B + b[i+al] - b[i] * t;
  }
  return false;
}

// how long do tail of A and head of B overlap?

int overlap(string a, string b){
  int al = a.length(), bl = b.length();
  int ans = 0;
  ull ah=0, bh=0, t=1;
  for (int i=1; i <= min(al, bl); i++){
    ah = ah + a[al - i] * t; // hash of tail of A of length i
    bh = bh * B + b[i-1]; // hash of head of B of length i
    if (ah == bh) ans =i;
    t *= B;
  }
  return ans;
}

void solve(){
  string CAT = "A=" + Astr + ", B=" + Bstr;
  cout << CAT << endl;

  if(contain(Astr, Bstr)){
    puts("Contain; Yes");
  } else {
    puts("Contain; No");
  }

  if(overlap(Astr, Bstr)){
    puts("Overlap; Yes");
  } else {
    puts("Overlap; No");
  }
  return;
}

int main(){
  Astr = "abc", Bstr = "xyz";
  solve();

  Astr = "abc", Bstr = "asebcabcopijad";
  solve();

  Astr = "abc", Bstr = "bcaa";
  solve();

  Astr = "abc", Bstr = "abcaa";
  solve();

}
