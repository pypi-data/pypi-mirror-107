---
title: anabel.transient
summary: General transformations and utilities for transient modeling.
template: pdoc.html
...
<main>
<header>
<!-- <h1 class="title">Module <code>anabel.transient</code></h1> -->
</header>
<section id="section-intro">
<h1 id="transient">Transient</h1>
<p>General transformations and utilities for transient modeling.</p>
</section>
<section>
</section>
<section>
</section>
<section>
<h2 class="section-title" id="header-functions">Functions</h2>
<dl>
<dt id="anabel.transient.linear_hot"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">linear_hot</span></span>(<span>f, df)</span>
</code></dt>
<dd>
<div class="desc"><p>Add a linear higher order term to a function</p>
<h2 id="examples">Examples</h2>
<p>First define some matrices</p>
<div class="sourceCode" id="cb1"><pre class="sourceCode python"><code class="sourceCode python"><span id="cb1-1"><a href="#cb1-1" aria-hidden="true" tabindex="-1"></a><span class="op">&gt;&gt;</span>A <span class="op">=</span> jnp.array([[<span class="fl">1.0</span>, <span class="fl">0.0</span>, <span class="fl">0.0</span>],</span>
<span id="cb1-2"><a href="#cb1-2" aria-hidden="true" tabindex="-1"></a>                 [<span class="fl">0.0</span>, <span class="fl">4.0</span>, <span class="fl">2.0</span>],</span>
<span id="cb1-3"><a href="#cb1-3" aria-hidden="true" tabindex="-1"></a>                 [<span class="fl">0.0</span>, <span class="fl">2.0</span>, <span class="fl">4.0</span>]])</span>
<span id="cb1-4"><a href="#cb1-4" aria-hidden="true" tabindex="-1"></a><span class="op">&gt;&gt;</span>B <span class="op">=</span> jnp.array([[<span class="op">-</span><span class="fl">0.23939017</span>,  <span class="fl">0.58743526</span>, <span class="op">-</span><span class="fl">0.77305379</span>],</span>
<span id="cb1-5"><a href="#cb1-5" aria-hidden="true" tabindex="-1"></a>                 [ <span class="fl">0.81921268</span>, <span class="op">-</span><span class="fl">0.30515101</span>, <span class="op">-</span><span class="fl">0.48556508</span>],</span>
<span id="cb1-6"><a href="#cb1-6" aria-hidden="true" tabindex="-1"></a>                 [<span class="op">-</span><span class="fl">0.52113619</span>, <span class="op">-</span><span class="fl">0.74953498</span>, <span class="op">-</span><span class="fl">0.40818426</span>]])</span>
<span id="cb1-7"><a href="#cb1-7" aria-hidden="true" tabindex="-1"></a><span class="op">&gt;&gt;</span>C <span class="op">=</span> A<span class="op">@</span>B</span></code></pre></div>
<p>Next define a linear function, <code>f: x -&gt; Ax</code>:</p>
<div class="sourceCode" id="cb2"><pre class="sourceCode python"><code class="sourceCode python"><span id="cb2-1"><a href="#cb2-1" aria-hidden="true" tabindex="-1"></a><span class="op">&gt;&gt;</span>f <span class="op">=</span> anon.dual.wrap(</span>
<span id="cb2-2"><a href="#cb2-2" aria-hidden="true" tabindex="-1"></a>    <span class="kw">lambda</span> x,<span class="op">*</span>args,<span class="op">**</span>kwds: x, A<span class="op">@</span>x, {},</span>
<span id="cb2-3"><a href="#cb2-3" aria-hidden="true" tabindex="-1"></a>    dim<span class="op">=</span><span class="dv">3</span></span>
<span id="cb2-4"><a href="#cb2-4" aria-hidden="true" tabindex="-1"></a>)</span></code></pre></div>
<p>Create a new function with a linear higher order term (<code>ff: x,dx -&gt; f(x) + Bdx</code>)</p>
<div class="sourceCode" id="cb3"><pre class="sourceCode python"><code class="sourceCode python"><span id="cb3-1"><a href="#cb3-1" aria-hidden="true" tabindex="-1"></a><span class="op">&gt;&gt;</span>ff <span class="op">=</span> linear_hot(f, B)</span>
<span id="cb3-2"><a href="#cb3-2" aria-hidden="true" tabindex="-1"></a></span>
<span id="cb3-3"><a href="#cb3-3" aria-hidden="true" tabindex="-1"></a><span class="op">&gt;&gt;</span>x <span class="op">=</span> dx <span class="op">=</span> jnp.ones((<span class="dv">3</span>,<span class="dv">1</span>))</span>
<span id="cb3-4"><a href="#cb3-4" aria-hidden="true" tabindex="-1"></a></span>
<span id="cb3-5"><a href="#cb3-5" aria-hidden="true" tabindex="-1"></a><span class="op">&gt;&gt;</span>f(x)</span>
<span id="cb3-6"><a href="#cb3-6" aria-hidden="true" tabindex="-1"></a>(DeviceArray([[<span class="fl">1.</span>],</span>
<span id="cb3-7"><a href="#cb3-7" aria-hidden="true" tabindex="-1"></a>            [<span class="fl">1.</span>],</span>
<span id="cb3-8"><a href="#cb3-8" aria-hidden="true" tabindex="-1"></a>            [<span class="fl">1.</span>]], dtype<span class="op">=</span>float32),</span>
<span id="cb3-9"><a href="#cb3-9" aria-hidden="true" tabindex="-1"></a>DeviceArray([[<span class="fl">1.</span>],</span>
<span id="cb3-10"><a href="#cb3-10" aria-hidden="true" tabindex="-1"></a>            [<span class="fl">6.</span>],</span>
<span id="cb3-11"><a href="#cb3-11" aria-hidden="true" tabindex="-1"></a>            [<span class="fl">6.</span>]], dtype<span class="op">=</span>float32),</span>
<span id="cb3-12"><a href="#cb3-12" aria-hidden="true" tabindex="-1"></a>{})</span>
<span id="cb3-13"><a href="#cb3-13" aria-hidden="true" tabindex="-1"></a></span>
<span id="cb3-14"><a href="#cb3-14" aria-hidden="true" tabindex="-1"></a><span class="op">&gt;&gt;</span>ff((x, dx))</span>
<span id="cb3-15"><a href="#cb3-15" aria-hidden="true" tabindex="-1"></a>((DeviceArray([[<span class="fl">1.</span>],</span>
<span id="cb3-16"><a href="#cb3-16" aria-hidden="true" tabindex="-1"></a>            [<span class="fl">1.</span>],</span>
<span id="cb3-17"><a href="#cb3-17" aria-hidden="true" tabindex="-1"></a>            [<span class="fl">1.</span>]], dtype<span class="op">=</span>float32),</span>
<span id="cb3-18"><a href="#cb3-18" aria-hidden="true" tabindex="-1"></a>DeviceArray([[<span class="fl">1.</span>],</span>
<span id="cb3-19"><a href="#cb3-19" aria-hidden="true" tabindex="-1"></a>            [<span class="fl">1.</span>],</span>
<span id="cb3-20"><a href="#cb3-20" aria-hidden="true" tabindex="-1"></a>            [<span class="fl">1.</span>]], dtype<span class="op">=</span>float32)),</span>
<span id="cb3-21"><a href="#cb3-21" aria-hidden="true" tabindex="-1"></a>DeviceArray([[<span class="fl">0.57499135</span>],</span>
<span id="cb3-22"><a href="#cb3-22" aria-hidden="true" tabindex="-1"></a>            [<span class="fl">6.0284967</span> ],</span>
<span id="cb3-23"><a href="#cb3-23" aria-hidden="true" tabindex="-1"></a>            [<span class="fl">4.3211446</span> ]], dtype<span class="op">=</span>float32),</span>
<span id="cb3-24"><a href="#cb3-24" aria-hidden="true" tabindex="-1"></a>{})</span></code></pre></div>
<h2 id="studies">Studies</h2>
<p><a href="/stdy/elle-0008">elle-0008</a></p>
</div>
</dd>
</dl>
</section>
<section>
</section>
</main>