import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;

public class SixteenBricksTest {

    protected SixteenBricks solution;

    @Before
    public void setUp() {
        solution = new SixteenBricks();
    }

    @Test
    public void testCase0() {
        int[] height = new int[]{1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1};

        int expected = 32;
        int actual = solution.maximumSurface(height);

        Assert.assertEquals(expected, actual);
    }

    @Test
    public void testCase1() {
        int[] height = new int[]{1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2};

        int expected = 64;
        int actual = solution.maximumSurface(height);

        Assert.assertEquals(expected, actual);
    }

    @Test
    public void testCase2() {
        int[] height = new int[]{77, 78, 58, 34, 30, 20, 8, 71, 37, 74, 21, 45, 39, 16, 4, 59};

        int expected = 1798;
        int actual = solution.maximumSurface(height);

        Assert.assertEquals(expected, actual);
    }

}
