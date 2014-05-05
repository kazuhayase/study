#include<vector>
#include<cmath>

using namespace std;
const double EPS = 1E-8;
typedef vector<double> vec;
typedef vector<vec> mat;

// solve Ax = b. A is square matrix.
// if no solution or no unique solution, return an array of length=0
vec gauss_jordan(const mat& A, const vec& b){
  int n = A.size();
  mat B(n, vec(n+1));
  for(int i=0; i<n; i++)
    for(int j=0; j<n; j++) B[i][j] = A[i][j];
  // A <- Ab
  for(int i=0; i<n; i++) B[i][n] = b[i];

  for(int i=0; i<n; i++) {
    // move equation with max coefficient to the variable to i-th
    int pivot = i;
    for (int j=i; j<n; j++){
      if (abs(B[j][i]) > abs(B[pivot][i])) pivot = j;
    }
    swap(B[i], B[pivot]);

    // no solution or no unique solution
    if (abs(B[i][i]) < EPS) return vec();

    // set the cofficient to the variable to be 1
    for (int j = i+1; j <=n; j++) B[i][j] /= B[i][i];
    for (int j = 0; j <n; j++) {
      if (i != j){
	// delete the i-th variable in the j-th equation
	for (int k = i+1; k <= n; k++) B[j][k] -= B[j][i] * B[i][k];
      }
    }
  }
  vec x(n);
  // b is the solution
  for(int i=0; i<n; i++) x[i] = B[i][n];
  return x;
}

  
