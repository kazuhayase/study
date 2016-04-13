import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;

public class ShortestPathWithMagicTest {

    protected ShortestPathWithMagic solution;

    @Before
    public void setUp() {
        solution = new ShortestPathWithMagic();
    }

    public static void assertEquals(double expected, double actual) {
        if (Double.isNaN(expected)) {
            Assert.assertTrue("expected: <NaN> but was: <" + actual + ">", Double.isNaN(actual));
            return;
        }
        double delta = Math.max(1e-9, 1e-9 * Math.abs(expected));
        Assert.assertEquals(expected, actual, delta);
    }

    @Test
    public void testCase0() {
        String[] dist = new String[]{"094", "904", "440"};
        int k = 1;

        double expected = 4.5;
        double actual = solution.getTime(dist, k);

        assertEquals(expected, actual);
    }

    @Test
    public void testCase1() {
        String[] dist = new String[]{"094", "904", "440"};
        int k = 2;

        double expected = 4.0;
        double actual = solution.getTime(dist, k);

        assertEquals(expected, actual);
    }

    @Test
    public void testCase2() {
        String[] dist = new String[]{"094", "904", "440"};
        int k = 50;

        double expected = 4.0;
        double actual = solution.getTime(dist, k);

        assertEquals(expected, actual);
    }

    @Test
    public void testCase3() {
        String[] dist = new String[]{"094", "904", "440"};
        int k = 0;

        double expected = 8.0;
        double actual = solution.getTime(dist, k);

        assertEquals(expected, actual);
    }

    @Test
    public void testCase4() {
        String[] dist = new String[]{"076237", "708937", "680641", "296059", "334508", "771980"};
        int k = 1;

        double expected = 3.5;
        double actual = solution.getTime(dist, k);

        assertEquals(expected, actual);
    }

    @Test
    public void testCase5() {
        String[] dist = new String[]{"00", "00"};
        int k = 50;

        double expected = 0.0;
        double actual = solution.getTime(dist, k);

        assertEquals(expected, actual);
    }

}
