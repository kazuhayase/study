#include <cstdio>
#include <iostream>
#include <vector>
#include <algorithm>
#include <functional>
#include <string>

using namespace std;

// Player
class Player {
  string m_strName;
  int m_iShot;
  int m_iHeight;

public: 

  Player( string name="", int shot=0, int height=0 )
    : m_strName(name), m_iShot(shot), m_iHeight(height){}

  string name() const { return m_strName; }
  int shot() const { return m_iShot; }
  int height() const { return m_iHeight; }
  
  static bool LexName(const Player& rLeft, const Player& rRight) { return rLeft.m_strName < rRight.m_strName; }
  static bool Rate(const Player& rLeft, const Player& rRight) { 
    if (rLeft.m_iShot == rRight.m_iShot){ return rLeft.m_iHeight > rRight.m_iHeight; }
    else { return rLeft.m_iShot > rRight.m_iShot; }
  }
};


int t;
const int MAX_T = 50;

int n[MAX_T], m[MAX_T], p[MAX_T];
const int MAX_N = 30;
const int MAX_M = 120;
const int MAX_P = 5;
const int MAX_Len = 25;

//Player all[MAX_T][MAX_N];
vector <Player> all;
vector <Player> odd;
vector <Player> even;
vector <Player> last;


void print_all(){
  vector<Player>::iterator it = all.begin();
  while( it != all.end() )

    {
      cerr << it->name() << "," << it->shot() << "," << it->height() << endl;
      ++it;
    }
}

void print_odd(){
  vector<Player>::iterator it = odd.begin();
  while( it != odd.end() )

    {
      cerr << it->name() << "," << it->shot() << "," << it->height() << endl;
      ++it;
    }
}

void print_even(){
  vector<Player>::iterator it = even.begin();
  while( it != even.end() )

    {
      cerr << it->name() << "," << it->shot() << "," << it->height() << endl;
      ++it;
    }
}

void print_last(){
  vector<Player>::iterator it = last.begin();
  while( it != last.end() )

    {
      cerr << it->name() << "," << it->shot() << "," << it->height() << endl;
      ++it;
    }
}

void print_ans(){

  vector<Player>::iterator it = last.begin();
  while( it != last.end() )

    {
      cout << " " << it->name();
      ++it;
    }
  cout << endl;
}

/*
string name[MAX_T][MAX_N];
int shot[MAX_T][MAX_N];
int height[MAX_T][MAX_N];
*/

void read_t();
void read(int i);
void solve(int i);

int main(){
  read_t();
  for(int i=0; i < t; i++){
    read(i);
    solve(i);
  }
  return 0;
}

void read_t(){
  cin >> t;
  fprintf(stderr, "t=%d\n", t);
}

void read(int i){

  string name;
  int shot; int height;
  //int i;

  //init
  all=vector<Player>();
  odd=vector<Player>();
  even=vector<Player>();
  last=vector<Player>();
  
  cin >> n[i] >> m[i] >> p[i];
  fprintf(stderr, "n[%d]=%d, m[%d]=%d, p[%d]=%d\n", i, n[i], i, m[i], i, p[i]);
  
  for(int j=0; j < n[i]; j++){
    cin >> name >> shot >> height;
    all.push_back(Player(name, shot, height));
  }

  print_all();
}


void solve(int i){

  //int i;
  int ans;

  sort(all.begin(), all.end(), Player::Rate);
  
  cerr << "[all sorted by Rate]\n";
  print_all();

  //k1 = odd team size, k2= even team size;
  int k1, k2;
  k2 = n[i]/2; k1=n[i]-k2;
  
  int rest1, rest2;
  
  rest1 = m[i] % k1;
  rest2 = m[i] % k2;
  
  fprintf(stderr, "k1=%d,k2=%d,rest1=%d,rest2=%d\n", k1, k2, rest1, rest2);
  
  vector<Player>::iterator it = all.begin();
  
  it += p[i]*2-1;
  for (int j=0; j<p[i]; j++){
    even.push_back(*it);
    it--;
    odd.push_back(*it);
    it--;
  }
  
  it = all.begin();
  it += p[i]*2-1;
  for (;;){
    it++;
    if(it == all.end()) break;
    odd.push_back(*it);
    it++;
    if(it == all.end()) break;
    even.push_back(*it);
  }
  
  cerr << "[odd]\n";
  print_odd();
  cerr << "[even]\n";
  print_even();
  
  vector<Player>::iterator it1 = odd.begin();
  vector<Player>::iterator it2 = even.begin();
  it1 += rest1; it2+=rest2;
  for(int j=0; j<p[i]; j++){
    last.push_back(*it1);
    last.push_back(*it2);
    it1++; it2++;
    if(it1 == odd.end()) {it1 = odd.begin();}
    if(it2 == even.end()) {it2 = even.begin();}
  }
  
  cerr << "[last before lex sort]\n";
  print_last();
  
  sort(last.begin(), last.end(), Player::LexName);
  
  cerr << "[last after lex sort]\n";
  print_last();    
  
  printf("Case #%d:", i+1);
  
  print_ans();
  
}

    /*
    if(rest1>p[i]){
      for(int l=0; l<rest1; l++){
	it1++;
      }
      for(int l=0; l<p[i]; l++){
	last.push_back(*it1);
	it1++;
      }
    } else {
      for(int l=0; l<p[i] - rest1 +1; l++){
	last.push_back(*it1);
	it1++;
      }
      for(int l=p[i] - rest1; l<p[i]; l++){
	it1++;
      }
      for(int l=p[i]; l<p[i] + rest1 +1; l++){
	last.push_back(*it1);
	it1++;
      }
    }

    vector<Player>::iterator it2 = even.begin();
    if(rest2>p[i]){
      for(int l=0; l<rest2; l++){
	it2++;
      }
      for(int l=0; l<p[i]; l++){
	last.push_back(*it2);
	it2++;
      }
    } else {
      for(int l=0; l<p[i] - rest2 +1; l++){
	last.push_back(*it2);
	it2++;
      }
      for(int l=p[i] - rest2; l<p[i]; l++){
	it2++;
      }
      for(int l=p[i]; l<p[i] + rest2 +1; l++){
	last.push_back(*it2);
	it2++;
      }
    }
    */
