---
title: anabel.template
summary: Wrappers, decorators and utilities for constructing expression templates.
template: pdoc.html
...
<main>
<header>
<!-- <h1 class="title">Module <code>anabel.template</code></h1> -->
</header>
<section id="section-intro">
<h1 id="templating">Templating</h1>
<p>Wrappers, decorators and utilities for constructing expression templates.</p>
</section>
<section>
</section>
<section>
</section>
<section>
<h2 class="section-title" id="header-functions">Functions</h2>
<dl>
<dt id="anabel.template.assemble"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">assemble</span></span>(<span>f)</span>
</code></dt>
<dd>
<div class="desc">
</div>
</dd>
<dt id="anabel.template.generator"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">generator</span></span>(<span>dim: Union[int, Tuple[Tuple[int, int]]] = None, statevar: str = 'state', main: str = 'main', jacx: str = 'jacx', form: str = &#x27;x,y,s=s,p=p,**e-&gt;x,y,s&#x27;, params: str = 'params', dimvar: str = None, origin: tuple = None, order: int = 0, **kwargs) ‑> Callable</span>
</code></dt>
<dd>
<div class="desc"><p>Decorator that wraps a basic local map generator.</p>
<h2 id="attributes">Attributes</h2>
<p><code>origin</code>: A structure containing arguments which may act as an ‘origin’ for the target function.</p>
<p><code>shape</code>: tuple Description of the shape of the dual and primal spaces.</p>
<h2 id="generated-arguments">Generated Arguments</h2>
<dl>
<dt><code>_expose_closure</code>: bool</dt>
<dd>Expose closed-over local variables as an attribute.
</dd>
<dt><code>_jit</code>: bool</dt>
<dd>If <code>True</code>{.python}, JIT-compiles the target function
</dd>
</dl>
<h2 id="studies">Studies</h2>
<p><a href="/stdy/elle-0008">Structural dynamics (<code>elle-0008</code>)</a></p>
</div>
</dd>
<dt id="anabel.template.generator_no2"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">generator_no2</span></span>(<span>)</span>
</code></dt>
<dd>
<div class="desc"><p>def F(): name = “my-element” def main(x, y, state, **kwds, _name=name): pass</p>
</div>
</dd>
<dt id="anabel.template.get_unspecified_parameters"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">get_unspecified_parameters</span></span>(<span>func, recurse=False)</span>
</code></dt>
<dd>
<div class="desc"><p>created 2021-03-31</p>
</div>
</dd>
<dt id="anabel.template.serialize"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">serialize</span></span>(<span>f)</span>
</code></dt>
<dd>
<div class="desc"><blockquote>
<p>Requires JAX</p>
</blockquote>
</div>
</dd>
<dt id="anabel.template.template"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">template</span></span>(<span>dim: Union[int, Tuple[Tuple[int, int]]] = None, statevar: str = 'state', main: str = 'main', jacx: str = 'jacx', form: str = &#x27;x,y,s=s,p=p,**e-&gt;x,y,s&#x27;, params: str = 'params', dimvar: str = None, origin: tuple = None, order: int = 0, **kwargs) ‑> Callable</span>
</code></dt>
<dd>
<div class="desc"><p>Decorator that wraps a basic local map generator.</p>
<h2 id="attributes">Attributes</h2>
<p><code>origin</code>: A structure containing arguments which may act as an ‘origin’ for the target function.</p>
<p><code>shape</code>: tuple Description of the shape of the dual and primal spaces.</p>
<h2 id="generated-arguments">Generated Arguments</h2>
<dl>
<dt><code>_expose_closure</code>: bool</dt>
<dd>Expose closed-over local variables as an attribute.
</dd>
<dt><code>_jit</code>: bool</dt>
<dd>If <code>True</code>{.python}, JIT-compiles the target function
</dd>
</dl>
<h2 id="studies">Studies</h2>
<p><a href="/stdy/elle-0008">Structural dynamics (<code>elle-0008</code>)</a></p>
</div>
</dd>
<dt id="anabel.template.wrap"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">wrap</span></span>(<span>f, *args, **kwds)</span>
</code></dt>
<dd>
<div class="desc"><p>Wrap a pre-defined function to act as a local dual map.</p>
</div>
</dd>
</dl>
</section>
<section>
<h2 class="section-title" id="header-classes">Classes</h2>
<dl>
<dt id="anabel.template.Dual"><code class="flex name class">
<span>class <span class="ident">Dual</span></span>
</code></dt>
<dd>
<div class="desc">
</div>
</dd>
</dl>
</section>
</main>