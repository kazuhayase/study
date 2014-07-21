#include<cstdio>
#include<algorithm>
#include<set>
using namespace std;

#define numof(array)  (sizeof (array) / sizeof *(array))

const int MAX_WH = 200;

// memo array to be -1 for all beforehand
int mem[MAX_WH + 1][MAX_WH + 1];

int grundy(int w, int h){
  if (mem[w][h] != -1) return mem[w][h];

  set<int> s;
  for (int i=2; w-i >=2; i++) s.insert(grundy(i,h) ^ grundy(w-i,h));
  for (int i=2; h-i >=2; i++) s.insert(grundy(w,i) ^ grundy(w,h-i));

  int res = 0;
  while (s.count(res)) res++;
  return mem[w][h] = res;
}

void solve(int w, int h){
  if (grundy(w,h) != 0) puts("WIN");
  else puts("LOSE");
}

int main (){
  int w=2, h=2;
  for(int i=0; i<MAX_WH+1; i++){
    fill(mem[i], mem[i]+(MAX_WH+1), -1);
  }
  solve(w,h);

  w=4, h=2;
  for(int i=0; i<MAX_WH+1; i++){
    fill(mem[i], mem[i]+(MAX_WH+1), -1);
  }
  solve(w,h);
}

