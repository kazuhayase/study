public class PointDistance {

	public int[] findPoint(int x1, int y1, int x2, int y2) {
		int mx = (x1+x2) /2;
		int my = (y1+y2) /2;
		int vx = x2 - x1;
		int vy = y2 - y1;
		int x3 = mx+vx;
		int y3 = my+vy;
		int[] ret = new int[2];
		ret[0]=x3;
		ret[1]=y3;
		return ret;
	}

}
