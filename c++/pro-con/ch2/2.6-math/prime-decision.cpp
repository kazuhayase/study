#include <vector>
#include <map>

using namespace std;

// decision if n is prime or not
// O(n^1/2)

bool is_prime(int n){
  for (int i=2; i*i<=n; i++){
    if(n % i == 0) return false;
  }
  return n != 1;
}

// enumerate prime numbers
// O(n^1/2)

vector<int> divisor (int n){
  vector<int> res;
  for (int i=1; i*i<=n; i++){
    if(n % i == 0) {
      res.push_back(i);
      if (i != n / i) res.push_back(n / i);
    }
  }
  return res;
}


// prime factoring
// O(n^1/2)

map<int, int> prime_factor(int n){
  map<int, int> res;
  for (int i=2; i*i<n; i++){
    while (n % i == 0){
      ++res[i];
      n /= i;
    }
  }
  if (n != 1) res[n] = 1;
  return res;
}
