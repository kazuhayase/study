#include <cstdio>
#include <cmath>
#include <iostream>
#include <vector>
#include <algorithm>
#include <functional>
#include <string>
#include <map>

using namespace std;

int t;
const int MAX_T = 100;

int k;
const int MAX_K = 100;

double ps, pr, pi, pu, pw, pd, pl;
double ans;

class Key {
  int win_;
  double sun_;
  
public: 

  Key( int win=0, double sun=0 )
    : win_(win), sun_(sun){}

  int win() const { return win_; }
  double sun() const {return sun_;}

  bool operator <(const Key &Obj) const
  {
    if(win_==Obj.win()) {
      return sun_ < Obj.sun();
    } else {
      return win_ < Obj.win();
    }
  }

   bool operator >(const Key &Obj) const
   {
     if(win_==Obj.win()) {
       return sun_ > Obj.sun();
     } else {
       return win_ > Obj.win();
     }
   }


 };

 // key = (#win,sun), value = probability
 typedef pair<Key, double> probPair;
 map <Key, double> probMap[MAX_K * 2];
 //map <Key, double> probMap;


 void read_t();
 void read();
 void solve();

 int main(){
   read_t();
   solve();
   return 0;
 }

 void read_t(){
   cin >> t;
   fprintf(stderr, "t=%d\n", t);
 }

 void read(){

   cin >> k;
   cin >> ps >> pr >> pi >> pu >> pw >> pd >> pl;

   fprintf(stderr, "k=%d, ps=%f, pr=%f, pi=%f, pu=%f, pw=%f, pd=%f, pl=%.3f\n",
	   k,ps,pr,pi,pu,pw,pd,pl);
 }

 void init(){

   ans = 0.0;

   for(int i=0; i < k*2; i++){
     probMap[i].clear();
   }

   Key key_init = Key(0,pi);

   probMap[0].insert(probPair(key_init, 1.0));

 }

 void dp(){
   double pre_lose, pre_win;

   for(int j=1; j < k*2; j++){

     map <Key, double>::iterator it = probMap[j-1].begin();
     while(it != probMap[j-1].end())
      {
	Key key = (*it).first;
	double value  = (*it).second;
	int win=key.win();
	double sun=key.sun();
	double winP = sun * ps + (1-sun) * pr;


	Key keyLoseDown = Key(win, sun-pd < 0.0 ? 0 : sun-pd );
	double valueLoseDown = value * (1-winP) *pl;

	Key keyLoseSame = Key(win, sun);
	double valueLoseSame = value * (1-winP) * (1-pl);

	Key keyWinUp = Key(win+1, sun+pu > 1.0 ? 1.0 : sun+pu);
	double valueWinUp = value * winP *pw;

	Key keyWinSame = Key(win+1, sun);
	double valueWinSame = value * winP *(1-pw);

	map <Key, double>::iterator nit;

	if(j-win < k) {

	  nit = probMap[j].find(keyLoseDown);
	  if(nit == probMap[j].end()){
	    probMap[j].insert(probPair(keyLoseDown, valueLoseDown ));
	  } else {
	    probMap[j].insert(probPair(keyLoseDown, (*nit).second + valueLoseDown ));
	    probMap[j].erase(nit);
	  }
	  
	  nit = probMap[j].find(keyLoseSame);
	  if(nit == probMap[j].end()){
	    probMap[j].insert(probPair(keyLoseSame, valueLoseSame ));
	  } else {
	    probMap[j].insert(probPair(keyLoseSame, (*nit).second + valueLoseSame ));
	    probMap[j].erase(nit);
	  }
	}

	if(win == k-1) {
	  ans += value * winP;
	} else {

	  nit = probMap[j].find(keyWinUp);
	  if(nit == probMap[j].end()){
	    probMap[j].insert(probPair(keyWinUp, valueWinUp ));
	  } else {
	    probMap[j].insert(probPair(keyWinUp, (*nit).second + valueWinUp ));
	    probMap[j].erase(nit);
	  }
	  
	  nit = probMap[j].find(keyWinSame);
	  if(nit == probMap[j].end()){
	    probMap[j].insert(probPair(keyWinSame, valueWinSame ));
	  } else {
	    probMap[j].insert(probPair(keyWinSame, (*nit).second + valueWinSame ));
	    probMap[j].erase(nit);
	  }
	}
	it++;
      }
  }
}

void solve(){

   for (int i = 0; i < t; i++){
    read();
    init();
    dp();
    printf("Case #%d: %.6f\n", i+1, ans);
  }
}
