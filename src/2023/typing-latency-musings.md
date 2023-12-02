<header class="article-header">
    <h1>Musing Around Typing Latency</h1>
    Published <time datetime="2023-09-18">2023-09-18</time> by James Frost.
    <p class="tagline">Contemplation on why typing can seem slow on modern computers.</p>
</header>

Modern computers are fast. In the time it takes you to blink, a computer can
read a thousand novels worth of data, and perform numerous calculations upon it.
However there are some bits of computers that are relatively slow, or at least
haven't improved significantly since the 1980s.

One example of this is input latency. An Apple II from over 40 years ago has
better latency between pressing a key on its keyboard, and a letter appearing on
screen. This has an impact on how snappy the computer feels overall, and of
latency gets too high the computer gets hard to use. But why are computers
nowadays slower than computers 40 years ago at this? It comes down to two main
things:

* You computer is doing more work.
* Peripherals moving from an interrupt driven system to a polling driven system.

The first one is insidious. It may not seem that typing into a text editor is
any more work today than it was in the past, but there are a bunch of things
going on in the background. Early text editors did little more than put glyphs
on screen in response to key presses. Now days your text editor might be
constantly running a spelling check, parsing any syntax in the text to highlight
appropriately, listen to signals from the host OS, such as closing or minimising
the window, and looking out for characters that may render differently, such as
Hebrew.

The very fact that a modern text editor runs in a window also represents more
work. In the past the glyphs (bitmaps of the characters) would be directly
written into the frame buffer, which the display would directly render. With a
window, the glyphs (which first have to be rendered from code to support modern
TrueType fonts) now get written into a temporary buffer, before all of the
windows are put together by something known as the compositor. This means that
windows work a lot more reliably, and allows the OS to do lots of fancy window
management, but does slow things down. This is why many games recommend being
run in "exclusive full screen", which bypasses to compositor.

The other change is in the hardware the computer is running on. Most modern
computers have some kind of GPU (though it may be built into the CPU package).
Where they do, the glyph must be copied over to the GPU before it can be
displayed. Older computers typically shared the memory between the frame buffer
and main CPU, which is why many 8 bit computers start displaying lots of funky
patterns on screen when they are processing lots of data. The GPU does allow for
much more complicated graphical effects to be done more quickly, but can be
slower for simple blitting of glyphs.

In the past computers were typically interrupt driven. When an external event
happened, such as a key being pressed, the CPU drops whatever it was doing and
immediately jumps to processing some code to handle that interrupt. This is very
good for latency, but throughput suffers, as the CPU might then need to reload a
bunch of data it had nearly finished with. So modern computers use polling
instead. This is simply checking whether a key has been pressed fairly
frequently. So the CPU now doesn't know that a key has been pressed until it
checks.

## Analysis of Typing Latency in Visual Studio Code

Up to 17 ms of frame latency from the 60 Hz refresh rate, plus any additional
monitor latency (5ms is a reasonable switching time). Then we have the graphics
driver latency, which to be fair, is probably fairly small, but I don't really
know. Then we have the VSCode latency, from when it receives a keypress from the
OS to when it makes the glyph appear on screen. This has apparently been
improved in the most recent update, so it is probably not too bad. Then we have
the OS's processing of the keyboard event, which is hopefully small, but
probably existent, before we get onto the limited polling rate of the USB
keyboard. It is 125 Hz for common ones, which gives us 8 ms of extra latency.
Finally we get to the keyboard itself, which probably adds some small amount of
extra latency, though perhaps the simpler ones are better here.

Assuming 1ms for each of the small latencies (which I honestly have no idea
about), this gives us a total latency of about 34 ms. Science tells us that 50
ms is where it has an impact on FPS game performance, but it is probably
noticeable much before that.

Without significant change to architectures, hardware can improve this.

* High refresh rate monitor     (8 ms)
* Low latency monitor           (1 ms)
* High polling rate keyboard    (1 ms)
* 5 instances of small latency  (5 ms)

This brings us to 15 ms, which while much better, is still quite a lot for
making a letter appear on a screen, given the speed of modern computers. The
biggest driver of latency is the monitor, which the leading ones currently can
probably reduce to about 5 ms in total. That leaves us with the software latency
to deal with, which is much harder to do so. There is also the fact that I have
no idea what the graphics driver/OS latencies actually are, and I really just
guessed them.

All in all modern computers can be made fast, especially when optimised to do
so. The iPad Pro has a specifically optimised hardware and software stack to get
this kind of latency down to about 10 ms, but that only just starts to match the
original Apple II.
