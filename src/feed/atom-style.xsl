<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="3.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:atom="http://www.w3.org/2005/Atom">
<xsl:output method="html" version="1.0" encoding="UTF-8" indent="yes"/>
<xsl:template match="/">
<html xmlns="http://www.w3.org/1999/xhtml" lang="en">
<head>
  <title><xsl:value-of select="/atom:feed/atom:title"/> Web Feed</title>
  <meta charset="utf-8"/>
  <meta http-equiv="content-type" content="text/html; charset=utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <style>
  main {
    max-width: 50em;
    margin: 3em auto;
    font-family: system-ui, san-serif;
  }
  .admonition {
    background-color: #fff5b1;
    outline: solid 1em #fff5b1;
    margin-bottom: 5em;
  }
  h1 {
    display: flex;
    align-items: center;
  }
  h1 svg {
    margin-right: 0.5em;
  }
  .entry {
    margin-bottom: 2em;
  }
  .entry h3 {
    margin-bottom: 0.25em;
  }
  .entry h3 a {
    text-decoration: none;
  }
  </style>
</head>
<body>
  <main>
  <div class="admonition">
    <p>
      <strong>This is a Web Feed,</strong> also known as an RSS feed. <strong>Subscribe</strong> by copying the URL from the address bar into your newsreader.
    </p>
    <p>
      Visit <a href="https://aboutfeeds.com">About Feeds</a> to get started with newsreaders and subscribing. It’s free!
    </p>
  </div>
  <h1>
    <!-- https://commons.wikimedia.org/wiki/File:Feed-icon.svg -->
    <svg xmlns="http://www.w3.org/2000/svg" version="1.1"
          viewBox="0 0 256 256"
          style="flex-shrink: 0; width: 1em; height: 1em;">
      <defs>
        <linearGradient x1="0.085" y1="0.085" x2="0.915" y2="0.915" id="RSSg">
          <stop offset="0.0" stop-color="#E3702D"/>
          <stop offset="0.1071" stop-color="#EA7D31"/>
          <stop offset="0.3503" stop-color="#F69537"/>
          <stop offset="0.5" stop-color="#FB9E3A"/>
          <stop offset="0.7016" stop-color="#EA7C31"/>
          <stop offset="0.8866" stop-color="#DE642B"/>
          <stop offset="1.0" stop-color="#D95B29"/>
        </linearGradient>
      </defs>
      <rect width="256" height="256" rx="55" ry="55" x="0" y="0" fill="#CC5D15"/>
      <rect width="246" height="246" rx="50" ry="50" x="5" y="5" fill="#F49C52"/>
      <rect width="236" height="236" rx="47" ry="47" x="10" y="10" fill="url(#RSSg)"/>
      <circle cx="68" cy="189" r="24" fill="#FFF"/>
      <path d="M160 213h-34a82 82 0 0 0 -82 -82v-34a116 116 0 0 1 116 116z" fill="#FFF"/>
      <path d="M184 213A140 140 0 0 0 44 73 V 38a175 175 0 0 1 175 175z" fill="#FFF"/>
    </svg>
    Web Feed Preview
  </h1>
  <h2><xsl:value-of select="/atom:feed/atom:title"/></h2>
  <p><xsl:value-of select="/atom:feed/atom:subtitle"/></p>
  <p>
    <a>
      <xsl:attribute name="href">
        <xsl:value-of select="/atom:feed/atom:link[2]/@href"/>
      </xsl:attribute>
      Visit website →
    </a>
  </p>
  <h2>Recent Items</h2>
  <xsl:for-each select="/atom:feed/atom:entry">
    <div class="entry">
      <h3>
        <a>
          <xsl:attribute name="href">
            <xsl:value-of select="atom:link/@href"/>
          </xsl:attribute>
          <xsl:value-of select="atom:title"/>
        </a>
      </h3>
      <div>
        <xsl:choose>
          <xsl:when test="atom:published">
            Published: <time><xsl:value-of select="atom:published"/></time>
          </xsl:when>
          <xsl:otherwise>
            Updated: <time><xsl:value-of select="atom:updated"/></time>
          </xsl:otherwise>
        </xsl:choose>
      </div>
    </div>
    </xsl:for-each>
  </main>
</body>
</html>
</xsl:template>
</xsl:stylesheet>
