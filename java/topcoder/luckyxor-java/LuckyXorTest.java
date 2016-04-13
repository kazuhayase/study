import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;

public class LuckyXorTest {

    protected LuckyXor solution;

    @Before
    public void setUp() {
        solution = new LuckyXor();
    }

    @Test
    public void testCase0() {
        int a = 4;

        int expected = 40;
        int actual = solution.construct(a);

        Assert.assertEquals(expected, actual);
    }

    @Test
    public void testCase1() {
        int a = 19;

        int expected = 20;
        int actual = solution.construct(a);

        Assert.assertEquals(expected, actual);
    }

    @Test
    public void testCase2() {
        int a = 88;

        int expected = 92;
        int actual = solution.construct(a);

        Assert.assertEquals(expected, actual);
    }

    @Test
    public void testCase3() {
        int a = 36;

        int expected = -1;
        int actual = solution.construct(a);

        Assert.assertEquals(expected, actual);
    }

}
