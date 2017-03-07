#!/usr/bin/python
# -*- coding: utf-8 -*-
from unittest import TestCase

from SOKnowledge.data_processor.scripts.finish.text_processor import remove_tags


class TestRemoveTags(TestCase):
    def test_removeTags(self):
        shortHtmlText = """<p>Solutions are welcome in any language. :-) I'm looking for the fastest way to obtain the value of π, as a personal challenge. More specifically I'm using ways that don't involve using <code># define</code>d constants like <code>M_PI</code>, or hard-coding the number in.</p>"""

        longHtmlText = """<pre class="lang-c prettyprint-override"><code>#include &lt;math.h&gt;
#include &lt;stdio.h&gt;
#include &lt;time.h&gt;

#define ITERS 10000000
#define TESTWITH(x) {                                                       \
    diff = 0.0;                                                             \
    time1 = clock();                                                        \
    for (i = 0; i &lt; ITERS; ++i)                                             \
        diff += (x) - M_PI;                                                 \
    time2 = clock();                                                        \
    printf("%s\t=&gt; %e, time =&gt; %f\n", #x, diff, diffclock(time2, time1));   \
}

static inline double
diffclock(clock_t time1, clock_t time0)
{
    return (double) (time1 - time0) / CLOCKS_PER_SEC;
}

int
main()
{
    int i;
    clock_t time1, time2;
    double diff;

    /* Warmup. The atan2 case catches GCC's atan folding (which would
     * optimise the ``4 * atan(1) - M_PI'' to a no-op), if -fno-builtin
     * is not used. */
    TESTWITH(4 * atan(1))
    TESTWITH(4 * atan2(1, 1))

#if defined(__GNUC__) &amp;&amp; (defined(__i386__) || defined(__amd64__))
    extern double fldpi();
    TESTWITH(fldpi())
#endif

    /* Actual tests start here. */
    TESTWITH(atan2(0, -1))
    TESTWITH(acos(-1))
    TESTWITH(2 * asin(1))
    TESTWITH(4 * atan2(1, 1))
    TESTWITH(4 * atan(1))

    return 0;
}
</code></pre>

<p>And the inline assembly stuff (<code>fldpi.c</code>), noting that it will only work for x86 and x64 systems:</p>
"""

        resultDict = remove_tags(shortHtmlText)
        self.assertEqual(resultDict['largeCodeDict'], {})
        self.assertNotEquals(resultDict['smallCodeDict'], {})
        self.assertEqual(resultDict['smallCodeDict']['_sc1_'], '# define')
        self.assertEqual(resultDict['smallCodeDict']['_sc2_'], 'M_PI')

        resultDict = remove_tags(longHtmlText)
        self.assertNotEquals(resultDict['smallCodeDict'], {})
        self.assertNotEquals(resultDict['largeCodeDict'], {})
        self.assertIsNotNone(resultDict['largeCodeDict']['_lc1_'])
