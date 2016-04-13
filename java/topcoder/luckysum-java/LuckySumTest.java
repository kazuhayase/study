import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;

public class LuckySumTest {

    protected LuckySum solution;

    @Before
    public void setUp() {
        solution = new LuckySum();
    }

    @Test
    public void testCase0() {
        String note = "?";

        long expected = 8L;
        long actual = solution.construct(note);

        Assert.assertEquals(expected, actual);
    }

    @Test
    public void testCase1() {
        String note = "?1";

        long expected = 11L;
        long actual = solution.construct(note);

        Assert.assertEquals(expected, actual);
    }

    @Test
    public void testCase2() {
        String note = "4?8";

        long expected = 448L;
        long actual = solution.construct(note);

        Assert.assertEquals(expected, actual);
    }

    @Test
    public void testCase3() {
        String note = "2??";

        long expected = -1L;
        long actual = solution.construct(note);

        Assert.assertEquals(expected, actual);
    }

    @Test
    public void testCase4() {
        String note = "??????????????";

        long expected = 11888888888888L;
        long actual = solution.construct(note);

        Assert.assertEquals(expected, actual);
    }

}
