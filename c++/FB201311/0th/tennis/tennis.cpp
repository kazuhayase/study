#include <cstdio>
#include <cmath>
#include <iostream>
#include <vector>
#include <algorithm>
#include <functional>
#include <string>

using namespace std;

int t;
const int MAX_T = 100;

int k;
const int MAX_K = 100;

double ps, pr, pi, pu, pw, pd, pl;

class Sun {
  
  double sun;
  double exist;
  
public: 

  Sun( double _sun=0.0, double _exist=0.0)
    : sun(_sun), exist(_exist){}

  double sun() const { return sun; }
  double exist() const { return exist; }

};

class Prob {
  int win;
  int lose;
  vector<Sun> sunlist;
  
public: 

  Prob( int _win=0, int _lose=0, vector _sunlist=)
    : win(_win), lose(_lose), sunlist(_sun){}

  int win() const { return win; }
  int lose() const { return lose; }
  vector <Sun> sunlist() const { return sunlist; }
};

// [#WIN] [#Sets]
double prob[MAX_K * 2][MAX_K * 2];
double sun[MAX_K * 2][MAX_K * 2];
double win[MAX_K * 2][MAX_K * 2];

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
  for(int i=0; i<MAX_K * 2; i++){
    for(int j=0; j<MAX_K * 2; j++){
      prob[i][j]=0.0, sun[i][j]=0.0, win[i][j]=0.0;
  }
  prob[0][0]=1.0;
  sun[0][0]=pi;
  win[0][0]=pi*ps+(1-pi)*pr;
  if(win[0][0] > 1.0) win[0][0]=1.0;

  }
}

void dp(){
  double pre_lose, pre_win;

  for(int j=1; j < k; j++){

    pre_win=0.0;
    pre_lose = (1-win[0][j-1])*prob[0][j-1];

    prob[0][j] = pre_win+pre_lose;
    if (prob[0][j] > 1.0) prob[0][j]=1.0;

    sun[0][j] = (sun[0][j-1]-pre_lose*pd*pl)*pre_lose;
    if (isfinite(sun[0][j])!=0) sun[0][j]=0.0;
    if (sun[0][j] < 0.0) sun[0][j]=0.0;


    win[0][j] = sun[0][j]*ps + (1-sun[0][j])*pr;
    if(win[0][j] > 1.0) win[0][j]=1.0;

    for(int i=1; i < k *2; i++){

      pre_win = win[i-1][j-1]*prob[i-1][j-1];
      pre_lose = (1-win[i][j-1])*prob[i][j-1];
      
      prob[i][j] = pre_win+pre_lose;
      if(prob[i][j]>1.0) prob[i][j]=1.0;

      if(pre_win+pre_lose == 0.0){
	sun[i][j]=0.0;
      } else {
	sun[i][j] = ((sun[i-i][j-1]+pre_win*pu*pw)*pre_win + (sun[i][j-1]-pre_lose*pd*pl)*pre_lose) / (pre_win+pre_lose);
      }

      if(sun[i][j]>1.0) sun[i][j]=1.0;
      if (isfinite(sun[i][j])!=0) sun[i][j]=0.0;
      if(sun[i][j]<0.0) sun[i][j]=0.0;

      win[i][j] = sun[i][j]*ps + (1-sun[i][j])*pr;
      if(win[i][j]>1.0) win[i][j]=1.0;
    }
  }

  for(int j=k; j < k*2; j++){

    pre_win=0.0;
    pre_lose = (1-win[j-k][j-1])*prob[j-k][j-1];
    prob[j-k][j] = pre_win+pre_lose;
    if (prob[j-k][j] > 1.0) prob[j-k][j]=1.0;

    sun[j-k][j] = (sun[j-k][j-1]-pre_lose*pd*pl)*pre_lose;
    if (isfinite(sun[j-k][j])!=0) sun[j-k][j]=0.0;
    if(sun[j-k][j]<0.0) sun[j-k][j]=0.0;

    win[j-k][j] = sun[j-k][j]*ps + (1-sun[j-k][j])*pr;
    if(win[j-k][j]>1.0) win[j-k][j]=1.0;

    for(int i=j-k+1; i<k *2; i++){
      
      pre_win = win[i-1][j-1]*prob[i-1][j-1];
      pre_lose = (1-win[i][j-1])*prob[i][j-1];
      
      prob[i][j] = pre_win+pre_lose;
      if(prob[i][j]>1.0) prob[i][j]=1.0;

      if(pre_win+pre_lose == 0.0){
	sun[i][j]=0.0;
      } else {
	sun[i][j] = ((sun[i-i][j-1]+pre_win*pu*pw)*pre_win + (sun[i][j-1]-pre_lose*pd*pl)*pre_lose) / (pre_win+pre_lose);
      }
      if(sun[i][j]>1.0) sun[i][j]=1.0;
      if (isfinite(sun[i][j])!=0) sun[i][j]=0.0;
      if(sun[i][j]<0.0) sun[i][j]=0.0;

      win[i][j] = sun[i][j]*ps + (1-sun[i][j])*pr;
      if(win[i][j]>1.0) win[i][j]=1.0;

    }
  }
}

void solve(){

   for (int i = 0; i < t; i++){
    read();
    init();
    dp();
    double ans=0;
    for(int j = k; j < k*2; j++){
      ans += prob[j][k*2-1];
    }
    printf("Case #%d: %.6f\n", i+1, ans);
  }
}
