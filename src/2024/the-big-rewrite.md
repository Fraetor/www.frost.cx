<header class="article-header">
    <h1>The Big Rewrite</h1>
    Published <time datetime="2024-05-31">2024-05-31</time> by James Frost.
    <p class="tagline">Considerations around large software rewrites.</p>
</header>

**The Big Rewrite** is where you rewrite a large part of a software system from scratch. There are [existing articles](https://www.joelonsoftware.com/2000/04/06/things-you-should-never-do-part-i/) on it being a bad idea, but I will go into some more nuanced reasoning in this article.

## Why would you rewrite?

The Big Rewrite is tempting because it does bring many real benefits through allowing you to go back and fix all your previous mistakes, without being bound by your existing system.

Often the key reason is to increase maintainability and development velocity. This is where a large code base ends up ill understood, and changes are very difficult to make without breaking something else, often in an unclear way. Rewriting from scratch removes all of these interdependencies, allowing you to freely work on whatever needs doing. It also gives you the chance to promise to yourself that you won't let it get as bad again, though you probably said that last time...

Performance is another key reason, and with the onset of *Software as a Service* (SaaS) it is also a direct cost driver. A rewrite allows you to reorganise what data structures are used within your system, and more optimally process things. This allows you to make a cheaper and more responsive system capable of handling more extreme inputs.

Usability is another area that can be improved, using the understanding gleamed from having had users of your existing software you now know which features to promote, which to hide away, and which to drop completely. This allows you to make the product your customer wants.

Finally a rewrite can often be easier than working on the existing code, especially if it is poorly understood.

## What can you lose?

The largest risk is that it takes a lot of time and effort to completely rewrite a system, and this often prevents you from taking any opportunities in the mean time. You also are taking effort from improving your current system, which in a competitive market will lose you customers.

Another significant risk is that your current customers are paying you for your *current* software. If you do a from-scratch rewrite you risk missing features that current users depend on, especially your more advanced users. These users may have outsized benefits for you, as they will support and promote your system.

Finally there is the risk that you spend all this time and effort, only to not improve over the original, or that wider business priorities change and the rewrite is never completed, wasting the whole endeavour. This plays into wider project management issues, as well as concerns about sunk cost, etc.

## An alternative?

With all of these risks it is clear that a rewrite is a risky endeavour. How then, do we get the benefits? Fortunately there are alternatives.

The main issue in The Big Rewrite is that is it big. If you are able to rewrite smaller segments of your system you'll be able to incrementally improve the overall system while working on more easily understood sections. These segments are also much more palatable to discard if they turns out not to meet some key requirement.

Doing this is much easier if your system is architected in a modular way. This isn't anything new, and has been recommended practice for many years, but not all software does it. If you are working on a system like this, you may be tempted to go in for a big rewrite, but generally this is not needed.

While it is more work, and will be slow at first, highly coupled systems can be made more modular over time. Incrementally is the key word here, with a module first being isolated from the general code without behaviour change before any attempt to rewrite it is made. This may temporarily involve having large sections of duplicated code as systems are untangled, but is very helpful in isolating modules within the system that can then be rewritten. This is well described in [this talk on removing global state from a legacy scientific codebase](https://www.youtube.com/watch?v=H8rMv4kSzxM).

Finally, it is worth remembering that a rewrite's size is relative to the available resources. What an independent developer considers a big rewrite would often be considered a small part by a large company.

<iframe width="560" height="315" src="https://www.youtube-nocookie.com/embed/xCGu5Z_vaps" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
