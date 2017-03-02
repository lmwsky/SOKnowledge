#!/usr/bin/python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup

def removeTags(htmlText):
    """
    delete all tags in html text(except code tag,all codeBlock is replace with string,
    '@lc[1-9][0-9]*@' or @sc[1-9][0-9]*@ is a regular expression which can match codeBlock name string),
    'l'--large stands for the <code><code> contents are large,and the <code> tags are wrapped in <pre> tag,
    's' --small stands for the <code><code> contents are small,and the <code> tags are not wrapped in <pre> tag,
    return the clean text,and codeBlock names and codeBlock
    :param htmlText:a piece of  html text with a lot of tags
    :return: cleanText -- all tags removed,but replace the <code><code> element with codeBlocksNames,

              largeCodeBlocksNames -- all the replaced long codeBlock names,etc.'@lc1@'
              largeCodeBlocks -- all the replaced long codeBlock.

    """

    soup = BeautifulSoup(htmlText, "lxml")
    codeTags = soup.find_all(name="code")

    cleanText = ""

    largeCodeDict={}
    smallCodeDict={}

    largeCodeBlocksNum = 1
    smallCodeBlocksNum = 1

    if htmlText is not None and len(htmlText) > 0:
        for tag in codeTags:
            if tag.string:
                if tag.parent.name == "pre":
                    name = "@lc" + str(largeCodeBlocksNum) + "@"
                    largeCodeDict[name]=tag.string
                    tag.string = name
                    largeCodeBlocksNum += 1
                else:
                    name = "@sc" + str(smallCodeBlocksNum) + "@"
                    smallCodeDict[name]=tag.string
                    tag.string = name
                    smallCodeBlocksNum += 1

        cleanText = soup.get_text()
    return [cleanText, largeCodeDict, smallCodeDict]

"""
def cleanSOText(htmlText):
    # the max code block size allowed save in text
    maxSingleCodeBlockSize = 30
    if htmlText is None or len(htmlText) == 0:
        return ["", [], []]
    soup = BeautifulSoup(htmlText, "lxml")
    codeBlocksNum = 1
    codeBlocks = []
    codeBlocksNames = []
    tokenizeText = ""
    codeTags = soup.find_all(name="code")
    for tag in codeTags:
        if tag.parent.name == "pre":
            if tag.string and (len(tag.string) > maxSingleCodeBlockSize or tag.string.find(" ") != -1):
                name = "@code" + str(codeBlocksNum) + "@"
                codeBlocks.append(tag.string)
                codeBlocksNames.append(name)
                tag.string = name
                codeBlocksNum += 1

    cleanText = soup.get_text()
    sents = nltk.sent_tokenize(cleanText)

    wordsText = []
    for s in sents:
        words = nltk.word_tokenize(s)
        wordsText.append(" ".join(words))
    tokenizeText = "\n".join(wordsText)

    return [cleanText, codeBlocksNames, codeBlocks, tokenizeText]
"""

if __name__ == '__main__':
    htmlText = """<p>Solutions are welcome in any language. :-) I'm looking for the fastest way to obtain the value of π, as a personal challenge. More specifically I'm using ways that don't involve using <code>#define</code>d constants like <code>M_PI</code>, or hard-coding the number in.</p>

<p>The program below tests the various ways I know of. The inline assembly version is, in theory, the fastest option, though clearly not portable; I've included it as a baseline to compare the other versions against. In my tests, with built-ins, the <code>4 * atan(1)</code> version is fastest on GCC 4.2, because it auto-folds the <code>atan(1)</code> into a constant. With <code>-fno-builtin</code> specified, the <code>atan2(0, -1)</code> version is fastest.</p>

<p>Here's the main testing program (<code>pitimes.c</code>):</p>

<pre class="lang-c prettyprint-override"><code>#include &lt;math.h&gt;
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

<pre class="lang-c prettyprint-override"><code>double
fldpi()
{
    double pi;
    asm("fldpi" : "=t" (pi));
    return pi;
}
</code></pre>

<p>And a build script that builds all the configurations I'm testing (<code>build.sh</code>):</p>

<pre><code>#!/bin/sh
gcc -O3 -Wall -c           -m32 -o fldpi-32.o fldpi.c
gcc -O3 -Wall -c           -m64 -o fldpi-64.o fldpi.c

gcc -O3 -Wall -ffast-math  -m32 -o pitimes1-32 pitimes.c fldpi-32.o
gcc -O3 -Wall              -m32 -o pitimes2-32 pitimes.c fldpi-32.o -lm
gcc -O3 -Wall -fno-builtin -m32 -o pitimes3-32 pitimes.c fldpi-32.o -lm
gcc -O3 -Wall -ffast-math  -m64 -o pitimes1-64 pitimes.c fldpi-64.o -lm
gcc -O3 -Wall              -m64 -o pitimes2-64 pitimes.c fldpi-64.o -lm
gcc -O3 -Wall -fno-builtin -m64 -o pitimes3-64 pitimes.c fldpi-64.o -lm
</code></pre>

<p>Apart from testing between various compiler flags (I've compared 32-bit against 64-bit too, because the optimisations are different), I've also tried switching the order of the tests around. The <code>atan2(0, -1)</code> version still comes out top every time, though.</p>
"""
    [cleanText, largeCodeDict,smallCodeDict] = removeTags(htmlText)
    print(htmlText)
    print(cleanText)
    print (largeCodeDict)
    print (smallCodeDict)
