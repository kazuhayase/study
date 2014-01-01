/*
  Encode a set S as an integer represented with bits
  f(S) = \sigma_{i \in S} 2^i

  empty set \psi := 0
  set of a single element {i} := 1<<i;
  set of all n elements {0,1,...,n-1} := (1<<n) - 1;
  decide whether i is in S; if (S>>i & 1)
  add an element i to S := S | 1<<i;
  remove an element i from S := S & ~(1<<i);
  sum of sets S and T := S | T
  intersection of sets S and T := S & T

  enumerate all subsets incrementally as \psi(empty set), {0}, {1}, {0,1}, ... {0,1,...n-1}
      for (int S=0; S < 1<<n; S++){ //do something }

  enumerate all subsets of "a set sup" decrementally.
      int sub = sup;
      do { 
        // do something
	sub = (sub-1) & sup;
      } while(sub != sup); // sub=0 (next)-> (0-1)&sup=sup 

  enumerate all subsets of "size k" lexicographic-incrementally
     int comb = (1<<k) - 1;
     while (comb < 1 << n) {
       int x = comb & -comb, y = comb + x;
       comb = ((comb & ~y) / x>>1) | y;
     }





*/


