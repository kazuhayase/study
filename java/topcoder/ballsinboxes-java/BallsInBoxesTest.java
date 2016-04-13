import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;

public class BallsInBoxesTest {

    protected BallsInBoxes solution;

    @Before
    public void setUp() {
        solution = new BallsInBoxes();
    }

    @Test
    public void testCase0() {
        long N = 10L;
        long K = 10L;

        long expected = 0L;
        long actual = solution.maxTurns(N, K);

        Assert.assertEquals(expected, actual);
    }

    @Test
    public void testCase1() {
        long N = 100L;
        long K = 1L;

        long expected = 99L;
        long actual = solution.maxTurns(N, K);

        Assert.assertEquals(expected, actual);
    }

    @Test
    public void testCase2() {
        long N = 1000L;
        long K = 999L;

        long expected = 1L;
        long actual = solution.maxTurns(N, K);

        Assert.assertEquals(expected, actual);
    }

    @Test
    public void testCase3() {
        long N = 10L;
        long K = 5L;

        long expected = 3L;
        long actual = solution.maxTurns(N, K);

        Assert.assertEquals(expected, actual);
    }

}
