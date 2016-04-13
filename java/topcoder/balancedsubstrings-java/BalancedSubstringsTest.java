import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;

public class BalancedSubstringsTest {

    protected BalancedSubstrings solution;

    @Before
    public void setUp() {
        solution = new BalancedSubstrings();
    }

    @Test
    public void testCase0() {
        String s = "011";

        int expected = 4;
        int actual = solution.countSubstrings(s);

        Assert.assertEquals(expected, actual);
    }

    @Test
    public void testCase1() {
        String s = "10111";

        int expected = 10;
        int actual = solution.countSubstrings(s);

        Assert.assertEquals(expected, actual);
    }

    @Test
    public void testCase2() {
        String s = "00000";

        int expected = 15;
        int actual = solution.countSubstrings(s);

        Assert.assertEquals(expected, actual);
    }

    @Test
    public void testCase3() {
        String s = "0000001000000";

        int expected = 91;
        int actual = solution.countSubstrings(s);

        Assert.assertEquals(expected, actual);
    }

    @Test
    public void testCase4() {
        String s = "100110001001";

        int expected = 49;
        int actual = solution.countSubstrings(s);

        Assert.assertEquals(expected, actual);
    }

}
