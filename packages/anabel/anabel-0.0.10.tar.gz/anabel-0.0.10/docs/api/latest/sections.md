---
title: anabel.sections
summary: High-level section modeling API.
template: pdoc.html
...
<main>
<header>
<!-- <h1 class="title">Module <code>anabel.sections</code></h1> -->
</header>
<section id="section-intro">
<h1 id="section-modeling">Section Modeling</h1>
<p>High-level section modeling API.</p>
</section>
<section>
</section>
<section>
</section>
<section>
<h2 class="section-title" id="header-functions">Functions</h2>
<dl>
<dt id="anabel.sections.Composite_Section"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">Composite_Section</span></span>(<span>Y, DY, DZ, quad, y_shift=0.0, mat=None)</span>
</code></dt>
<dd>
<div class="desc">
</div>
</dd>
<dt id="anabel.sections.I_Sect"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">I_Sect</span></span>(<span>b, d, alpha, beta, quad, yref=0.0, MatData=None)</span>
</code></dt>
<dd>
<div class="desc">
</div>
</dd>
<dt id="anabel.sections.TC_Sect"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">TC_Sect</span></span>(<span>d, bf, tw, quad, yref=0.0, tf=None, ymf=None, MatData=None, **kwds)</span>
</code></dt>
<dd>
<div class="desc"><pre><code>____________
|   |  |   |
----|  |----
    |  |
    |  |
    |  |
    ----</code></pre>
</div>
</dd>
<dt id="anabel.sections.T_Sect"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">T_Sect</span></span>(<span>d, quad, b=None, bf=None, tf=None, tw=None, alpha=None, beta=None, yref=0.0, MatData=None)</span>
</code></dt>
<dd>
<div class="desc"><pre><code>_____________
|           |
-------------
    |   |
    |   |
    |   |
    -----</code></pre>
</div>
</dd>
<dt id="anabel.sections.W_Sect"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">W_Sect</span></span>(<span>b, d, alpha, beta, quadf, quadw, yref=0.0, MatData=None)</span>
</code></dt>
<dd>
<div class="desc">
</div>
</dd>
<dt id="anabel.sections.ei"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">ei</span></span>(<span>y, epsa, kappa)</span>
</code></dt>
<dd>
<div class="desc">
</div>
</dd>
<dt id="anabel.sections.load_aisc"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">load_aisc</span></span>(<span>SectionName, props='')</span>
</code></dt>
<dd>
<div class="desc"><p>Load cross section properties from AISC database.</p>
<p>props: A list of AISC properties, or one of the following: - ‘simple’: <code>A</code>, <code>Ix</code>, <code>Zx</code></p>
</div>
</dd>
</dl>
</section>
<section>
<h2 class="section-title" id="header-classes">Classes</h2>
<dl>
<dt id="anabel.sections.CompositeSection"><code class="flex name class">
<span>class <span class="ident">CompositeSection</span></span>
<span>(</span><span>Y, DY, DZ, quad, y_shift=0.0, mat=None)</span>
</code></dt>
<dd>
<div class="desc">
</div>
<h3>Ancestors</h3>
<ul class="hlist">
<li><a title="anabel.sections.Section" href="#anabel.sections.Section">Section</a></li>
</ul>
<h3>Subclasses</h3>
<ul class="hlist">
<li><a title="anabel.sections.Rectangle" href="#anabel.sections.Rectangle">Rectangle</a></li>
<li><a title="anabel.sections.Tee" href="#anabel.sections.Tee">Tee</a></li>
</ul>
<h3>Methods</h3>
<dl>
<dt id="anabel.sections.CompositeSection.plot"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">plot</span></span>(<span>self, show_properties=True, plain=False, show_quad=True, show_dims=True, annotate=True)</span>
</code></dt>
<dd>
<div class="desc"><p>Plot a composite cross section.</p>
</div>
</dd>
</dl>
</dd>
<dt id="anabel.sections.Rectangle"><code class="flex name class">
<span>class <span class="ident">Rectangle</span></span>
<span>(</span><span>b, d, quad=None, yref=0.0, mat=None, **kwds)</span>
</code></dt>
<dd>
<div class="desc"><p>Rectangular cross section</p>
</div>
<h3>Ancestors</h3>
<ul class="hlist">
<li><a title="anabel.sections.CompositeSection" href="#anabel.sections.CompositeSection">CompositeSection</a></li>
<li><a title="anabel.sections.Section" href="#anabel.sections.Section">Section</a></li>
<li><a title="anabel.sections.VerticalSection" href="#anabel.sections.VerticalSection">VerticalSection</a></li>
</ul>
<h3>Inherited members</h3>
<ul class="hlist">
<li><code><b><a title="anabel.sections.CompositeSection" href="#anabel.sections.CompositeSection">CompositeSection</a></b></code>:
<ul class="hlist">
<li><code><a title="anabel.sections.CompositeSection.plot" href="#anabel.sections.CompositeSection.plot">plot</a></code></li>
</ul>
</li>
</ul>
</dd>
<dt id="anabel.sections.Section"><code class="flex name class">
<span>class <span class="ident">Section</span></span>
</code></dt>
<dd>
<div class="desc">
</div>
<h3>Subclasses</h3>
<ul class="hlist">
<li><a title="anabel.sections.CompositeSection" href="#anabel.sections.CompositeSection">CompositeSection</a></li>
</ul>
<h3>Methods</h3>
<dl>
<dt id="anabel.sections.Section.assemble"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">assemble</span></span>(<span>self)</span>
</code></dt>
<dd>
<div class="desc">
</div>
</dd>
</dl>
</dd>
<dt id="anabel.sections.Tee"><code class="flex name class">
<span>class <span class="ident">Tee</span></span>
<span>(</span><span>d=None, quad=None, b=None, bf=None, tf=None, tw=None, alpha=None, beta=None, yref=None, mat=None)</span>
</code></dt>
<dd>
<div class="desc"><p><img src="img/sections/tee-dims.svg" /></p>
<pre><code>      bf
_____________ 
|           | tf
-------------
    |   |
    |   |
    |   |
    -----
     tw</code></pre>
<h2 id="parameters">Parameters</h2>
<p>tf,tw, bf, d: float shape parameters</p>
</div>
<h3>Ancestors</h3>
<ul class="hlist">
<li><a title="anabel.sections.CompositeSection" href="#anabel.sections.CompositeSection">CompositeSection</a></li>
<li><a title="anabel.sections.Section" href="#anabel.sections.Section">Section</a></li>
<li><a title="anabel.sections.VerticalSection" href="#anabel.sections.VerticalSection">VerticalSection</a></li>
</ul>
<h3>Methods</h3>
<dl>
<dt id="anabel.sections.Tee.annotate"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">annotate</span></span>(<span>self, ax)</span>
</code></dt>
<dd>
<div class="desc">
</div>
</dd>
<dt id="anabel.sections.Tee.properties"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">properties</span></span>(<span>self)</span>
</code></dt>
<dd>
<div class="desc">
</div>
</dd>
</dl>
<h3>Inherited members</h3>
<ul class="hlist">
<li><code><b><a title="anabel.sections.CompositeSection" href="#anabel.sections.CompositeSection">CompositeSection</a></b></code>:
<ul class="hlist">
<li><code><a title="anabel.sections.CompositeSection.plot" href="#anabel.sections.CompositeSection.plot">plot</a></code></li>
</ul>
</li>
</ul>
</dd>
<dt id="anabel.sections.VerticalSection"><code class="flex name class">
<span>class <span class="ident">VerticalSection</span></span>
</code></dt>
<dd>
<div class="desc">
</div>
<h3>Subclasses</h3>
<ul class="hlist">
<li><a title="anabel.sections.Rectangle" href="#anabel.sections.Rectangle">Rectangle</a></li>
<li><a title="anabel.sections.Tee" href="#anabel.sections.Tee">Tee</a></li>
</ul>
<h3>Methods</h3>
<dl>
<dt id="anabel.sections.VerticalSection.plot_limit"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">plot_limit</span></span>(<span>self, fy=1.0, **kwds)</span>
</code></dt>
<dd>
<div class="desc">
</div>
</dd>
<dt id="anabel.sections.VerticalSection.plot_yield"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">plot_yield</span></span>(<span>self, fy=1.0, **kwds)</span>
</code></dt>
<dd>
<div class="desc">
</div>
</dd>
</dl>
</dd>
</dl>
</section>
</main>