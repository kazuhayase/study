public class BearCheats {

	public String eyesight(int A, int B) {
		int gap = 0;
		while(A>0){
			if (A % 10 != B % 10){
				gap++;
			}
			A /= 10;
			B /= 10;
		}
		if(gap<2){
			return "happy";
		} else {
			return "glasses";
		}
	}

}
