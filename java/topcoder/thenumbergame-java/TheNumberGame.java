public class TheNumberGame {
	
	public String intToStr(int x){
		char[] xx = new char[20];
		int i=0;
		while(x>0){
			int res = x % 10;
			xx[i++] = (char) ('0' + res);
			x /= 10;
		}
		xx[i]='\0';
		return String.valueOf(xx);
	}

	public String determineOutcome(int A, int B) {
		String strA = String.valueOf(A);
		String strB = String.valueOf(B);
		String revB = new StringBuilder(strB).reverse().toString();
		int lenA = strA.length();
		int lenB = strB.length();
		boolean yes = false;
		for(int i=0; i<lenA; i++){
			if(i+lenB < lenA+1){
				if(strA.substring(i,i+lenB).equals(strB) || strA.substring(i,i+lenB).equals(revB)){	
					yes = true;	
				}
			}
		}
		if(yes){
			return "Manao wins";
		} else {
			return "Manao loses";
		}
	}

}
