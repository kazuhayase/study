// plane scan (sweep) method
// 平面走査

#include<vector>
#include<set>
#include<cstdio>

using namespace std;


const int MAX_N=40000;

//INPUT
int N;
double x[MAX_N], y[MAX_N], r[MAX_N];

// Is the circle-i inside circle-j?
bool inside(int i, int j){
  double dx = x[i] - x[j], dy = y[i] - y[j];
  return dx * dx + dy * dy <= r[j] * r[j];
}

void solve(){
  // enumerate all events
  vector < pair<double, int> > events; // x of left/right of circles
  for (int i=0; i<N; i++){
    events.push_back(make_pair(x[i]-r[i], i)); // left
    events.push_back(make_pair(x[i]+r[i], i+N)); // right
  }
  sort(events.begin(), events.end());

  // scan
  set< pair<double, int> > outers; // all outer circles under scan
  vector<int> res; // list of outer circles
  for (int i=0; i < events.size(); i++){
    int id = events[i].second % N;
    if (events[i].second < N){// case of left 
      set< pair<double, int> >::iterator it = outers.lower_bound(make_pair(y[id], id));
      if (it != outers.end() && inside(id, it->second)) continue;
      if (it != outers.begin() && inside(id, (--it)->second)) continue;
      res.push_back(id);
      outers.insert(make_pair(y[id], id));
    } else {
      outers.erase(make_pair(y[id], id));
    }
  }
  sort(res.begin(), res.end());
  printf("%lu\n", res.size());
  for (int i=0; i<res.size(); i++){
    printf("%d%c", res[i]+1, i+1 == res.size() ? '\n' : ' ');
  }
}

int main(){
  N=5;
  x[0]=0, y[0]=-2, r[0]=1;
  x[1]=0, y[1]=3, r[1]=3;
  x[2]=0, y[2]=0, r[2]=10;
  x[3]=0, y[3]=1.5, r[3]=1;
  x[4]=50, y[4]=50, r[4]=10;

  solve();
}

  
