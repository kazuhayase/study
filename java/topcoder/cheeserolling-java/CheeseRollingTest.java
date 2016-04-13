import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;

public class CheeseRollingTest {

    protected CheeseRolling solution;

    @Before
    public void setUp() {
        solution = new CheeseRolling();
    }

    @Test
    public void testCase0() {
        String[] wins = new String[]{"NN", "YN"};

        long[] expected = new long[]{0L, 2L};
        long[] actual = solution.waysToWin(wins);

        Assert.assertArrayEquals(expected, actual);
    }

    @Test
    public void testCase1() {
        String[] wins = new String[]{"NYNY", "NNYN", "YNNY", "NYNN"};

        long[] expected = new long[]{8L, 0L, 16L, 0L};
        long[] actual = solution.waysToWin(wins);

        Assert.assertArrayEquals(expected, actual);
    }

    @Test
    public void testCase2() {
        String[] wins = new String[]{"NYNYNYNY", "NNYNYNYY", "YNNNNNNN", "NYYNNYNY", "YNYYNYYY", "NYYNNNNN", "YNYYNYNN", "NNYNNYYN"};

        long[] expected = new long[]{4096L, 8960L, 0L, 2048L, 23808L, 0L, 1408L, 0L};
        long[] actual = solution.waysToWin(wins);

        Assert.assertArrayEquals(expected, actual);
    }

    @Test
    public void testCase3() {
        String[] wins = new String[]{"NYNNNNYYNYYNNYNN", "NNNNNNNNNYYNYYNY", "YYNYYNNNNYYYYYYN", "YYNNYYYNYNNYYYNY", "YYNNNYYNYYNNNNYY", "YYYNNNNYYNNYYNYN", "NYYNNYNYNYNYYYYN", "NYYYYNNNYYNYNYYY", "YYYNNNYNNYYYYNNN", "NNNYNYNNNNNNYYNY", "NNNYYYYYNYNYYYNN", "YYNNYNNNNYNNYNNY", "YNNNYNNYNNNNNYNN", "NNNNYYNNYNNYNNYY", "YYNYNNNNYYYYYNNN", "YNYNNYYNYNYNYNYN"};

        long[] expected = new long[]{331616878592L, 37267079168L, 2426798866432L, 2606831599616L, 994941665280L, 1162501849088L, 1888166674432L, 4632734203904L, 832881524736L, 84707409920L, 3007127748608L, 55490052096L, 17818550272L, 254672666624L, 629921447936L, 1959311671296L};
        long[] actual = solution.waysToWin(wins);

        Assert.assertArrayEquals(expected, actual);
    }

    @Test
    public void testCase4() {
        String[] wins = new String[]{"NYYYYYYYYYYYYYYY", "NNYYYYYYYYYYYYYY", "NNNYYYYYYYYYYYYY", "NNNNYYYYYYYYYYYY", "NNNNNYYYYYYYYYYY", "NNNNNNYYYYYYYYYY", "NNNNNNNYYYYYYYYY", "NNNNNNNNYYYYYYYY", "NNNNNNNNNYYYYYYY", "NNNNNNNNNNYYYYYY", "NNNNNNNNNNNYYYYY", "NNNNNNNNNNNNYYYY", "NNNNNNNNNNNNNYYY", "NNNNNNNNNNNNNNYY", "NNNNNNNNNNNNNNNY", "NNNNNNNNNNNNNNNN"};

        long[] expected = new long[]{20922789888000L, 0L, 0L, 0L, 0L, 0L, 0L, 0L, 0L, 0L, 0L, 0L, 0L, 0L, 0L, 0L};
        long[] actual = solution.waysToWin(wins);

        Assert.assertArrayEquals(expected, actual);
    }

}
