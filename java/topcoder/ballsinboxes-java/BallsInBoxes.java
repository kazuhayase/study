public class BallsInBoxes {

	public long maxTurns(long N, long K) {
		if (K == 1){
			return N - 1;
		}
		if (N - K == 1){
			return 1;
		}
		if (N == K){
			return 0;
		}
		
		return 0;
	}

}
