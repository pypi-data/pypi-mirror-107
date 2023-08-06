---
title: anabel.assemble
summary: Core model building classes.
template: pdoc.html
...
<main>
<header>
<!-- <h1 class="title">Module <code>anabel.assemble</code></h1> -->
</header>
<section id="section-intro">
<h1 id="assemblers2">Assemblers(<code>2</code>)</h1>
<p>Core model building classes.</p>
</section>
<section>
</section>
<section>
</section>
<section>
</section>
<section>
<h2 class="section-title" id="header-classes">Classes</h2>
<dl>
<dt id="anabel.assemble.MeshGroup"><code class="flex name class">
<span>class <span class="ident">MeshGroup</span></span>
<span>(</span><span>*args, ndm=2, ndf=1, mesh=None, **kwds)</span>
</code></dt>
<dd>
<div class="desc"><p>Homogeneous 2D mesh group.</p>
<h2 id="parameters">Parameters</h2>
<dl>
<dt><strong><code>ndm</code></strong> : <code>int</code></dt>
<dd>number of model dimensions
</dd>
<dt><strong><code>ndf</code></strong> : <code>int</code></dt>
<dd>number of degrees of freedom (dofs) at each node
</dd>
</dl>
</div>
<h3>Ancestors</h3>
<ul class="hlist">
<li>anabel.assemble.UniformAssembler</li>
<li>anabel.assemble.Assembler</li>
</ul>
<h3>Static methods</h3>
<dl>
<dt id="anabel.assemble.MeshGroup.read"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">read</span></span>(<span>filename: str, *args, **kwds)</span>
</code></dt>
<dd>
<div class="desc"><p>Create a class instance by reading in a mesh file.</p>
<p>This function should work with any mesh format that is supported in the external <a href="https://github.com/nschloe/meshio"><code>meshio</code></a> Python library.</p>
<h2 id="parameters">Parameters</h2>
<dl>
<dt><strong><code>filetype</code></strong> : <code>str</code></dt>
<dd>In addition to those supported in <code>meshio</code>, the following formats are supported: <code>m228</code>: Simple text file; see docstrings in source code of <code>_read_m228</code>.
</dd>
</dl>
</div>
</dd>
</dl>
<h3>Instance variables</h3>
<dl>
<dt id="anabel.assemble.MeshGroup.dofs"><code class="name">var <span class="ident">dofs</span></code></dt>
<dd>
<div class="desc"><p>Plain DOF numbering scheme.</p>
<h2 id="returns">Returns</h2>
<dl>
<dt><strong><code>dofs</code></strong> : <code>Sequence (</code>nn<code>, </code>ndf<code>)</code></dt>
<dd>A sequence with shape <code>nn</code> by <code>ndf</code> where: [<code>ndf</code>] [<code>nn</code>]
</dd>
<dt><code>2021-05-07</code></dt>
<dd>
</dd>
</dl>
</div>
</dd>
<dt id="anabel.assemble.MeshGroup.nr"><code class="name">var <span class="ident">nr</span></code></dt>
<dd>
<div class="desc"><p>Return number of fixed degrees of freedom</p>
</div>
</dd>
</dl>
<h3>Methods</h3>
<dl>
<dt id="anabel.assemble.MeshGroup.assemble_integral"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">assemble_integral</span></span>(<span>self, elem=None, verbose=False, **kwds) ‑> Callable</span>
</code></dt>
<dd>
<div class="desc"><h2 id="parameters">Parameters</h2>
<dl>
<dt><strong><code>elem</code></strong> : <code>f(u,xyz) -&gt; R^[ndf*nen]</code></dt>
<dd>
</dd>
</dl>
<h2 id="returns">Returns</h2>
<dl>
<dt><strong><code>f</code></strong> : <code>f(U, (xi, dV)) -&gt; R^[nf]</code></dt>
<dd>quad(elem(U[el], X[el])*dV
</dd>
</dl>
</div>
</dd>
<dt id="anabel.assemble.MeshGroup.assemble_linear"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">assemble_linear</span></span>(<span>self, elem=None, verbose=False, **kwds) ‑> Callable</span>
</code></dt>
<dd>
<div class="desc"><p><code>elem(None,xyz) -&gt; R^[ndf*nen]</code></p>
<h2 id="returns">Returns</h2>
<dl>
<dt><strong><code>f</code></strong> : <code>f(U, (xi, dV)) -&gt; R^[nf]</code></dt>
<dd>quad(elem(None, X[el])*dV
</dd>
</dl>
</div>
</dd>
<dt id="anabel.assemble.MeshGroup.compose"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">compose</span></span>(<span>self, elem=None, verbose=False, solver=None)</span>
</code></dt>
<dd>
<div class="desc"><h2 id="parameters">Parameters</h2>
<dl>
<dt><strong><code>elem</code></strong> : <code>Callable</code></dt>
<dd>local function to be integrated over.
</dd>
<dt><strong><code>solver</code></strong> : <code>str</code></dt>
<dd>Either of the following. “sparse”: use <code>scipy.sparse.linalg.spsolve</code> “cg”: Conjugate gradient using <code>jax.scipy.sparse.linalg.cg</code> <code>None</code>: default to <code>anabel.backend.linalg.solve</code>
</dd>
</dl>
<p>2021-05-07</p>
</div>
</dd>
<dt id="anabel.assemble.MeshGroup.compose_quad"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">compose_quad</span></span>(<span>self, f=None, jit=True, verbose=False, **kwds)</span>
</code></dt>
<dd>
<div class="desc">
</div>
</dd>
<dt id="anabel.assemble.MeshGroup.norm"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">norm</span></span>(<span>self, u, h, quad)</span>
</code></dt>
<dd>
<div class="desc">
</div>
</dd>
<dt id="anabel.assemble.MeshGroup.plot"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">plot</span></span>(<span>self, values=None, func=None, scale=1.0, interact=False, savefig: str = None, **kwds)</span>
</code></dt>
<dd>
<div class="desc"><h2 id="parameters">Parameters</h2>
<dl>
<dt><strong><code>u</code></strong> : <code>Union[ Callable, Sequence ]</code></dt>
<dd>Values to plot over domain.
</dd>
<dt><strong><code>savefig</code></strong> : <code>str</code></dt>
<dd>File path to save image to.
</dd>
</dl>
<p>Plot mesh using <code>pyvista</code> interface to VTK.</p>
<p>Pure numpy is used for generality.</p>
<p>Claudio Perez</p>
</div>
</dd>
<dt id="anabel.assemble.MeshGroup.write"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">write</span></span>(<span>self, filename: str, **kwds)</span>
</code></dt>
<dd>
<div class="desc"><p>Export mesh using <code>meshio</code>.</p>
</div>
</dd>
</dl>
</dd>
<dt id="anabel.assemble.Model"><code class="flex name class">
<span>class <span class="ident">Model</span></span>
<span>(</span><span>ndm: int, ndf: int)</span>
</code></dt>
<dd>
<div class="desc"><p>Base class for assembler objects.</p>
<p>An assembler is typically characterized by collections of nodes, elements and parameters. The purpose of the assembler is to provide a convenient interface for interacting with and managing these entities.</p>
<p>Basic structural model class</p>
<h2 id="parameters">Parameters</h2>
<dl>
<dt><strong><code>ndm</code></strong> : <code>int</code></dt>
<dd>number of model dimensions
</dd>
<dt><strong><code>ndf</code></strong> : <code>int</code></dt>
<dd>number of degrees of freedom (dofs) at each node
</dd>
</dl>
</div>
<h3>Ancestors</h3>
<ul class="hlist">
<li>anabel.assemble.Assembler</li>
</ul>
<h3>Subclasses</h3>
<ul class="hlist">
<li>anabel.assemble.Domain</li>
<li><a title="anabel.assemble.rModel" href="#anabel.assemble.rModel">rModel</a></li>
</ul>
<h3>Instance variables</h3>
<dl>
<dt id="anabel.assemble.Model.NOS"><code class="name">var <span class="ident">NOS</span> : int</code></dt>
<dd>
<div class="desc"><p>Degree of static indeterminacy</p>
</div>
</dd>
<dt id="anabel.assemble.Model.basic_forces"><code class="name">var <span class="ident">basic_forces</span> : numpy.ndarray</code></dt>
<dd>
<div class="desc">
</div>
</dd>
<dt id="anabel.assemble.Model.cforces"><code class="name">var <span class="ident">cforces</span> : numpy.ndarray</code></dt>
<dd>
<div class="desc">
</div>
</dd>
<dt id="anabel.assemble.Model.dofs"><code class="name">var <span class="ident">dofs</span></code></dt>
<dd>
<div class="desc"><p>Plain DOF numbering scheme.</p>
<p>2021-05-07</p>
</div>
</dd>
<dt id="anabel.assemble.Model.eforces"><code class="name">var <span class="ident">eforces</span></code></dt>
<dd>
<div class="desc"><p>Array of elastic element forces</p>
</div>
</dd>
<dt id="anabel.assemble.Model.idx_c"><code class="name">var <span class="ident">idx_c</span></code></dt>
<dd>
<div class="desc">
</div>
</dd>
<dt id="anabel.assemble.Model.idx_e"><code class="name">var <span class="ident">idx_e</span></code></dt>
<dd>
<div class="desc"><p>Indices of elastic basic (not plastic) forces</p>
</div>
</dd>
<dt id="anabel.assemble.Model.idx_f"><code class="name">var <span class="ident">idx_f</span></code></dt>
<dd>
<div class="desc">
</div>
</dd>
<dt id="anabel.assemble.Model.idx_i"><code class="name">var <span class="ident">idx_i</span></code></dt>
<dd>
<div class="desc">
</div>
</dd>
<dt id="anabel.assemble.Model.idx_x"><code class="name">var <span class="ident">idx_x</span></code></dt>
<dd>
<div class="desc">
</div>
</dd>
<dt id="anabel.assemble.Model.nQ"><code class="name">var <span class="ident">nQ</span></code></dt>
<dd>
<div class="desc">
</div>
</dd>
<dt id="anabel.assemble.Model.ne"><code class="name">var <span class="ident">ne</span> : int</code></dt>
<dd>
<div class="desc"><p>number of elements in model</p>
</div>
</dd>
<dt id="anabel.assemble.Model.nf"><code class="name">var <span class="ident">nf</span> : int</code></dt>
<dd>
<div class="desc"><p>Number of free model degrees of freedom</p>
</div>
</dd>
<dt id="anabel.assemble.Model.nq"><code class="name">var <span class="ident">nq</span></code></dt>
<dd>
<div class="desc"><p>Number of basic element forces</p>
</div>
</dd>
<dt id="anabel.assemble.Model.nr"><code class="name">var <span class="ident">nr</span> : int</code></dt>
<dd>
<div class="desc"><p>number of constrained dofs in model</p>
</div>
</dd>
<dt id="anabel.assemble.Model.nt"><code class="name">var <span class="ident">nt</span> : int</code></dt>
<dd>
<div class="desc"><p>Total number of model degrees of freedom.</p>
</div>
</dd>
<dt id="anabel.assemble.Model.nv"><code class="name">var <span class="ident">nv</span></code></dt>
<dd>
<div class="desc"><p>Number of basic deformation variables</p>
</div>
</dd>
<dt id="anabel.assemble.Model.rdnt_forces"><code class="name">var <span class="ident">rdnt_forces</span> : numpy.ndarray</code></dt>
<dd>
<div class="desc">
</div>
</dd>
<dt id="anabel.assemble.Model.rdofs"><code class="name">var <span class="ident">rdofs</span></code></dt>
<dd>
<div class="desc"><p>Sequence of restrained dofs in model</p>
</div>
</dd>
<dt id="anabel.assemble.Model.rel"><code class="name">var <span class="ident">rel</span></code></dt>
<dd>
<div class="desc">
</div>
</dd>
</dl>
<h3>Methods</h3>
<dl>
<dt id="anabel.assemble.Model.add_element"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">add_element</span></span>(<span>self, element)</span>
</code></dt>
<dd>
<div class="desc"><p>Add a general element to model</p>
<h2 id="parameters">Parameters</h2>
<dl>
<dt><strong><code>element</code></strong> : <code>emme.elements.Element</code></dt>
<dd>
</dd>
</dl>
</div>
</dd>
<dt id="anabel.assemble.Model.add_elements"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">add_elements</span></span>(<span>self, elements)</span>
</code></dt>
<dd>
<div class="desc"><p>Add a general element to model</p>
<h2 id="parameters">Parameters</h2>
<dl>
<dt><strong><code>element</code></strong> : <code>emme.elements.Element</code></dt>
<dd>
</dd>
</dl>
</div>
</dd>
<dt id="anabel.assemble.Model.assemble_force"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">assemble_force</span></span>(<span>self, elem=None, **kwds) ‑> Callable</span>
</code></dt>
<dd>
<div class="desc"><p>A simple force composer for skeletal structures.</p>
</div>
</dd>
<dt id="anabel.assemble.Model.beam"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">beam</span></span>(<span>self, tag: str, iNode, jNode, mat=None, sec=None, Qpl=None, **kwds)</span>
</code></dt>
<dd>
<div class="desc"><p>Create and add a beam object to model</p>
<h2 id="parameters">Parameters</h2>
<dl>
<dt><strong><code>tag</code></strong> : <code>str</code></dt>
<dd>string used for identifying object
</dd>
<dt><strong><code>iNode</code></strong> : <code>emme.Node</code> or <code>str</code></dt>
<dd>node object at element i-end
</dd>
<dt><strong><code>jNode</code></strong> : <code>emme.Node</code> or <code>str</code></dt>
<dd>node object at element j-end
</dd>
<dt><strong><code>mat</code></strong> : <code>emme.Material</code></dt>
<dd>
</dd>
<dt><strong><code>sec</code></strong> : <code>emme.Section</code></dt>
<dd>
</dd>
</dl>
</div>
</dd>
<dt id="anabel.assemble.Model.boun"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">boun</span></span>(<span>self, node, ones)</span>
</code></dt>
<dd>
<div class="desc">
</div>
</dd>
<dt id="anabel.assemble.Model.clean"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">clean</span></span>(<span>self, keep=None)</span>
</code></dt>
<dd>
<div class="desc">
</div>
</dd>
<dt id="anabel.assemble.Model.compose"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">compose</span></span>(<span>self, resp='d', jit=True, verbose=False, **kwds)</span>
</code></dt>
<dd>
<div class="desc">
</div>
</dd>
<dt id="anabel.assemble.Model.compose_displ"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">compose_displ</span></span>(<span>self, solver=None, solver_opts={}, elem=None, jit_force=True, **kwds)</span>
</code></dt>
<dd>
<div class="desc"><p>dynamically creates functions <code>collect_loads</code> and <code>collect_coord</code>.</p>
</div>
</dd>
<dt id="anabel.assemble.Model.compose_force"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">compose_force</span></span>(<span>self, jit=True, **kwds)</span>
</code></dt>
<dd>
<div class="desc">
</div>
</dd>
<dt id="anabel.assemble.Model.compose_param"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">compose_param</span></span>(<span>self, f=None, jit_force=True, verbose=False, **kwds)</span>
</code></dt>
<dd>
<div class="desc">
</div>
</dd>
<dt id="anabel.assemble.Model.displ"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">displ</span></span>(<span>self, val)</span>
</code></dt>
<dd>
<div class="desc">
</div>
</dd>
<dt id="anabel.assemble.Model.elem"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">elem</span></span>(<span>self, elem, nodes, tag)</span>
</code></dt>
<dd>
<div class="desc">
</div>
</dd>
<dt id="anabel.assemble.Model.fix"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">fix</span></span>(<span>self, node, dirn=['x', 'y', 'rz'])</span>
</code></dt>
<dd>
<div class="desc"><p>Define a fixed boundary condition at specified degrees of freedom of the supplied node</p>
<h2 id="parameters">Parameters</h2>
<dl>
<dt><strong><code>node</code></strong> : <code>anabel.Node</code></dt>
<dd>
</dd>
<dt><strong><code>dirn</code></strong> : <code>Sequence[String]</code></dt>
<dd>
</dd>
</dl>
</div>
</dd>
<dt id="anabel.assemble.Model.frame"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">frame</span></span>(<span>self, bays, stories, column_mat=None, column_sec=None, girder_mat=None, girder_sec=None)</span>
</code></dt>
<dd>
<div class="desc"><p>Macro for generating rectangular building frames</p>
<h2 id="parameters">Parameters</h2>
<dl>
<dt><strong><code>bays</code></strong> : <code>tuple</code></dt>
<dd>tuple containing bay width, and number of bays
</dd>
<dt><strong><code>stories</code></strong> : <code>tuple</code></dt>
<dd>tuple
</dd>
</dl>
<p>column_mat:</p>
</div>
</dd>
<dt id="anabel.assemble.Model.girder"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">girder</span></span>(<span>self, nodes, mats=None, xsecs=None, story=None)</span>
</code></dt>
<dd>
<div class="desc">
</div>
</dd>
<dt id="anabel.assemble.Model.hinge"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">hinge</span></span>(<span>self, elem, node)</span>
</code></dt>
<dd>
<div class="desc">
</div>
</dd>
<dt id="anabel.assemble.Model.load"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">load</span></span>(<span>self, obj, *args, pattern=None, **kwds)</span>
</code></dt>
<dd>
<div class="desc"><p>Apply a load to a model object</p>
<p>Claudio Perez 2021-04-01</p>
</div>
</dd>
<dt id="anabel.assemble.Model.load_node"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">load_node</span></span>(<span>self, node, load, **kwds)</span>
</code></dt>
<dd>
<div class="desc"><p>Claudio Perez 2021-04-01</p>
</div>
</dd>
<dt id="anabel.assemble.Model.load_state"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">load_state</span></span>(<span>self, state)</span>
</code></dt>
<dd>
<div class="desc">
</div>
</dd>
<dt id="anabel.assemble.Model.material"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">material</span></span>(<span>self, tag: str, E: float)</span>
</code></dt>
<dd>
<div class="desc">
</div>
</dd>
<dt id="anabel.assemble.Model.node"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">node</span></span>(<span>self, tag: str, x: float, y=None, z=None, mass: float = None)</span>
</code></dt>
<dd>
<div class="desc"><p>Add a new emme.Node object to the model</p>
<h2 id="parameters">Parameters</h2>
<dl>
<dt><strong><code>x</code></strong>, <strong><code>y</code></strong>, <strong><code>z</code></strong> : <code>float</code></dt>
<dd>Node coordinates.
</dd>
</dl>
</div>
</dd>
<dt id="anabel.assemble.Model.numDOF"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">numDOF</span></span>(<span>self)</span>
</code></dt>
<dd>
<div class="desc">
</div>
</dd>
<dt id="anabel.assemble.Model.pin"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">pin</span></span>(<span>self, *nodes)</span>
</code></dt>
<dd>
<div class="desc"><p>Create a pinned reaction by fixing all translational degrees of freedom at the specified nodes.</p>
<h2 id="parameters">Parameters</h2>
<dl>
<dt><strong><code>node</code></strong> : <code>anabel.Node</code></dt>
<dd>
</dd>
</dl>
</div>
</dd>
<dt id="anabel.assemble.Model.redundant"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">redundant</span></span>(<span>self, elem: object, nature)</span>
</code></dt>
<dd>
<div class="desc"><p>nature:</p>
</div>
</dd>
<dt id="anabel.assemble.Model.roller"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">roller</span></span>(<span>self, node)</span>
</code></dt>
<dd>
<div class="desc"><p>Create a roller reaction at specified node</p>
</div>
</dd>
<dt id="anabel.assemble.Model.state"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">state</span></span>(<span>self, method='Linear')</span>
</code></dt>
<dd>
<div class="desc">
</div>
</dd>
<dt id="anabel.assemble.Model.taprod"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">taprod</span></span>(<span>self, tag: str, iNode, jNode, mat=None, xsec=None, Qpl=None, A=None, E=None)</span>
</code></dt>
<dd>
<div class="desc"><p>Construct a tapered rod element with variable E and A values.</p>
</div>
</dd>
<dt id="anabel.assemble.Model.truss"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">truss</span></span>(<span>self, tag: str, iNode, jNode, elem=None, mat=None, xsec=None, Qpl=None, A=None, E=None)</span>
</code></dt>
<dd>
<div class="desc">
</div>
</dd>
<dt id="anabel.assemble.Model.truss3d"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">truss3d</span></span>(<span>self, tag: str, iNode, jNode, mat=None, xsec=None)</span>
</code></dt>
<dd>
<div class="desc"><p>Add an emme.Truss3d object to model</p>
<h2 id="parameters">Parameters</h2>
</div>
</dd>
<dt id="anabel.assemble.Model.update"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">update</span></span>(<span>self, U)</span>
</code></dt>
<dd>
<div class="desc">
</div>
</dd>
<dt id="anabel.assemble.Model.xsection"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">xsection</span></span>(<span>self, tag: str, A: float, I: float)</span>
</code></dt>
<dd>
<div class="desc">
</div>
</dd>
</dl>
</dd>
<dt id="anabel.assemble.Model"><code class="flex name class">
<span>class <span class="ident">SkeletalModel</span></span>
<span>(</span><span>ndm: int, ndf: int)</span>
</code></dt>
<dd>
<div class="desc"><p>Base class for assembler objects.</p>
<p>An assembler is typically characterized by collections of nodes, elements and parameters. The purpose of the assembler is to provide a convenient interface for interacting with and managing these entities.</p>
<p>Basic structural model class</p>
<h2 id="parameters">Parameters</h2>
<dl>
<dt><strong><code>ndm</code></strong> : <code>int</code></dt>
<dd>number of model dimensions
</dd>
<dt><strong><code>ndf</code></strong> : <code>int</code></dt>
<dd>number of degrees of freedom (dofs) at each node
</dd>
</dl>
</div>
<h3>Ancestors</h3>
<ul class="hlist">
<li>anabel.assemble.Assembler</li>
</ul>
<h3>Subclasses</h3>
<ul class="hlist">
<li>anabel.assemble.Domain</li>
<li><a title="anabel.assemble.rModel" href="#anabel.assemble.rModel">rModel</a></li>
</ul>
<h3>Instance variables</h3>
<dl>
<dt id="anabel.assemble.Model.NOS"><code class="name">var <span class="ident">NOS</span> : int</code></dt>
<dd>
<div class="desc"><p>Degree of static indeterminacy</p>
</div>
</dd>
<dt id="anabel.assemble.Model.basic_forces"><code class="name">var <span class="ident">basic_forces</span> : numpy.ndarray</code></dt>
<dd>
<div class="desc">
</div>
</dd>
<dt id="anabel.assemble.Model.cforces"><code class="name">var <span class="ident">cforces</span> : numpy.ndarray</code></dt>
<dd>
<div class="desc">
</div>
</dd>
<dt id="anabel.assemble.Model.dofs"><code class="name">var <span class="ident">dofs</span></code></dt>
<dd>
<div class="desc"><p>Plain DOF numbering scheme.</p>
<p>2021-05-07</p>
</div>
</dd>
<dt id="anabel.assemble.Model.eforces"><code class="name">var <span class="ident">eforces</span></code></dt>
<dd>
<div class="desc"><p>Array of elastic element forces</p>
</div>
</dd>
<dt id="anabel.assemble.Model.idx_c"><code class="name">var <span class="ident">idx_c</span></code></dt>
<dd>
<div class="desc">
</div>
</dd>
<dt id="anabel.assemble.Model.idx_e"><code class="name">var <span class="ident">idx_e</span></code></dt>
<dd>
<div class="desc"><p>Indices of elastic basic (not plastic) forces</p>
</div>
</dd>
<dt id="anabel.assemble.Model.idx_f"><code class="name">var <span class="ident">idx_f</span></code></dt>
<dd>
<div class="desc">
</div>
</dd>
<dt id="anabel.assemble.Model.idx_i"><code class="name">var <span class="ident">idx_i</span></code></dt>
<dd>
<div class="desc">
</div>
</dd>
<dt id="anabel.assemble.Model.idx_x"><code class="name">var <span class="ident">idx_x</span></code></dt>
<dd>
<div class="desc">
</div>
</dd>
<dt id="anabel.assemble.Model.nQ"><code class="name">var <span class="ident">nQ</span></code></dt>
<dd>
<div class="desc">
</div>
</dd>
<dt id="anabel.assemble.Model.ne"><code class="name">var <span class="ident">ne</span> : int</code></dt>
<dd>
<div class="desc"><p>number of elements in model</p>
</div>
</dd>
<dt id="anabel.assemble.Model.nf"><code class="name">var <span class="ident">nf</span> : int</code></dt>
<dd>
<div class="desc"><p>Number of free model degrees of freedom</p>
</div>
</dd>
<dt id="anabel.assemble.Model.nq"><code class="name">var <span class="ident">nq</span></code></dt>
<dd>
<div class="desc"><p>Number of basic element forces</p>
</div>
</dd>
<dt id="anabel.assemble.Model.nr"><code class="name">var <span class="ident">nr</span> : int</code></dt>
<dd>
<div class="desc"><p>number of constrained dofs in model</p>
</div>
</dd>
<dt id="anabel.assemble.Model.nt"><code class="name">var <span class="ident">nt</span> : int</code></dt>
<dd>
<div class="desc"><p>Total number of model degrees of freedom.</p>
</div>
</dd>
<dt id="anabel.assemble.Model.nv"><code class="name">var <span class="ident">nv</span></code></dt>
<dd>
<div class="desc"><p>Number of basic deformation variables</p>
</div>
</dd>
<dt id="anabel.assemble.Model.rdnt_forces"><code class="name">var <span class="ident">rdnt_forces</span> : numpy.ndarray</code></dt>
<dd>
<div class="desc">
</div>
</dd>
<dt id="anabel.assemble.Model.rdofs"><code class="name">var <span class="ident">rdofs</span></code></dt>
<dd>
<div class="desc"><p>Sequence of restrained dofs in model</p>
</div>
</dd>
<dt id="anabel.assemble.Model.rel"><code class="name">var <span class="ident">rel</span></code></dt>
<dd>
<div class="desc">
</div>
</dd>
</dl>
<h3>Methods</h3>
<dl>
<dt id="anabel.assemble.Model.add_element"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">add_element</span></span>(<span>self, element)</span>
</code></dt>
<dd>
<div class="desc"><p>Add a general element to model</p>
<h2 id="parameters">Parameters</h2>
<dl>
<dt><strong><code>element</code></strong> : <code>emme.elements.Element</code></dt>
<dd>
</dd>
</dl>
</div>
</dd>
<dt id="anabel.assemble.Model.add_elements"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">add_elements</span></span>(<span>self, elements)</span>
</code></dt>
<dd>
<div class="desc"><p>Add a general element to model</p>
<h2 id="parameters">Parameters</h2>
<dl>
<dt><strong><code>element</code></strong> : <code>emme.elements.Element</code></dt>
<dd>
</dd>
</dl>
</div>
</dd>
<dt id="anabel.assemble.Model.assemble_force"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">assemble_force</span></span>(<span>self, elem=None, **kwds) ‑> Callable</span>
</code></dt>
<dd>
<div class="desc"><p>A simple force composer for skeletal structures.</p>
</div>
</dd>
<dt id="anabel.assemble.Model.beam"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">beam</span></span>(<span>self, tag: str, iNode, jNode, mat=None, sec=None, Qpl=None, **kwds)</span>
</code></dt>
<dd>
<div class="desc"><p>Create and add a beam object to model</p>
<h2 id="parameters">Parameters</h2>
<dl>
<dt><strong><code>tag</code></strong> : <code>str</code></dt>
<dd>string used for identifying object
</dd>
<dt><strong><code>iNode</code></strong> : <code>emme.Node</code> or <code>str</code></dt>
<dd>node object at element i-end
</dd>
<dt><strong><code>jNode</code></strong> : <code>emme.Node</code> or <code>str</code></dt>
<dd>node object at element j-end
</dd>
<dt><strong><code>mat</code></strong> : <code>emme.Material</code></dt>
<dd>
</dd>
<dt><strong><code>sec</code></strong> : <code>emme.Section</code></dt>
<dd>
</dd>
</dl>
</div>
</dd>
<dt id="anabel.assemble.Model.boun"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">boun</span></span>(<span>self, node, ones)</span>
</code></dt>
<dd>
<div class="desc">
</div>
</dd>
<dt id="anabel.assemble.Model.clean"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">clean</span></span>(<span>self, keep=None)</span>
</code></dt>
<dd>
<div class="desc">
</div>
</dd>
<dt id="anabel.assemble.Model.compose"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">compose</span></span>(<span>self, resp='d', jit=True, verbose=False, **kwds)</span>
</code></dt>
<dd>
<div class="desc">
</div>
</dd>
<dt id="anabel.assemble.Model.compose_displ"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">compose_displ</span></span>(<span>self, solver=None, solver_opts={}, elem=None, jit_force=True, **kwds)</span>
</code></dt>
<dd>
<div class="desc"><p>dynamically creates functions <code>collect_loads</code> and <code>collect_coord</code>.</p>
</div>
</dd>
<dt id="anabel.assemble.Model.compose_force"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">compose_force</span></span>(<span>self, jit=True, **kwds)</span>
</code></dt>
<dd>
<div class="desc">
</div>
</dd>
<dt id="anabel.assemble.Model.compose_param"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">compose_param</span></span>(<span>self, f=None, jit_force=True, verbose=False, **kwds)</span>
</code></dt>
<dd>
<div class="desc">
</div>
</dd>
<dt id="anabel.assemble.Model.displ"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">displ</span></span>(<span>self, val)</span>
</code></dt>
<dd>
<div class="desc">
</div>
</dd>
<dt id="anabel.assemble.Model.elem"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">elem</span></span>(<span>self, elem, nodes, tag)</span>
</code></dt>
<dd>
<div class="desc">
</div>
</dd>
<dt id="anabel.assemble.Model.fix"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">fix</span></span>(<span>self, node, dirn=['x', 'y', 'rz'])</span>
</code></dt>
<dd>
<div class="desc"><p>Define a fixed boundary condition at specified degrees of freedom of the supplied node</p>
<h2 id="parameters">Parameters</h2>
<dl>
<dt><strong><code>node</code></strong> : <code>anabel.Node</code></dt>
<dd>
</dd>
<dt><strong><code>dirn</code></strong> : <code>Sequence[String]</code></dt>
<dd>
</dd>
</dl>
</div>
</dd>
<dt id="anabel.assemble.Model.frame"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">frame</span></span>(<span>self, bays, stories, column_mat=None, column_sec=None, girder_mat=None, girder_sec=None)</span>
</code></dt>
<dd>
<div class="desc"><p>Macro for generating rectangular building frames</p>
<h2 id="parameters">Parameters</h2>
<dl>
<dt><strong><code>bays</code></strong> : <code>tuple</code></dt>
<dd>tuple containing bay width, and number of bays
</dd>
<dt><strong><code>stories</code></strong> : <code>tuple</code></dt>
<dd>tuple
</dd>
</dl>
<p>column_mat:</p>
</div>
</dd>
<dt id="anabel.assemble.Model.girder"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">girder</span></span>(<span>self, nodes, mats=None, xsecs=None, story=None)</span>
</code></dt>
<dd>
<div class="desc">
</div>
</dd>
<dt id="anabel.assemble.Model.hinge"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">hinge</span></span>(<span>self, elem, node)</span>
</code></dt>
<dd>
<div class="desc">
</div>
</dd>
<dt id="anabel.assemble.Model.load"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">load</span></span>(<span>self, obj, *args, pattern=None, **kwds)</span>
</code></dt>
<dd>
<div class="desc"><p>Apply a load to a model object</p>
<p>Claudio Perez 2021-04-01</p>
</div>
</dd>
<dt id="anabel.assemble.Model.load_node"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">load_node</span></span>(<span>self, node, load, **kwds)</span>
</code></dt>
<dd>
<div class="desc"><p>Claudio Perez 2021-04-01</p>
</div>
</dd>
<dt id="anabel.assemble.Model.load_state"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">load_state</span></span>(<span>self, state)</span>
</code></dt>
<dd>
<div class="desc">
</div>
</dd>
<dt id="anabel.assemble.Model.material"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">material</span></span>(<span>self, tag: str, E: float)</span>
</code></dt>
<dd>
<div class="desc">
</div>
</dd>
<dt id="anabel.assemble.Model.node"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">node</span></span>(<span>self, tag: str, x: float, y=None, z=None, mass: float = None)</span>
</code></dt>
<dd>
<div class="desc"><p>Add a new emme.Node object to the model</p>
<h2 id="parameters">Parameters</h2>
<dl>
<dt><strong><code>x</code></strong>, <strong><code>y</code></strong>, <strong><code>z</code></strong> : <code>float</code></dt>
<dd>Node coordinates.
</dd>
</dl>
</div>
</dd>
<dt id="anabel.assemble.Model.numDOF"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">numDOF</span></span>(<span>self)</span>
</code></dt>
<dd>
<div class="desc">
</div>
</dd>
<dt id="anabel.assemble.Model.pin"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">pin</span></span>(<span>self, *nodes)</span>
</code></dt>
<dd>
<div class="desc"><p>Create a pinned reaction by fixing all translational degrees of freedom at the specified nodes.</p>
<h2 id="parameters">Parameters</h2>
<dl>
<dt><strong><code>node</code></strong> : <code>anabel.Node</code></dt>
<dd>
</dd>
</dl>
</div>
</dd>
<dt id="anabel.assemble.Model.redundant"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">redundant</span></span>(<span>self, elem: object, nature)</span>
</code></dt>
<dd>
<div class="desc"><p>nature:</p>
</div>
</dd>
<dt id="anabel.assemble.Model.roller"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">roller</span></span>(<span>self, node)</span>
</code></dt>
<dd>
<div class="desc"><p>Create a roller reaction at specified node</p>
</div>
</dd>
<dt id="anabel.assemble.Model.state"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">state</span></span>(<span>self, method='Linear')</span>
</code></dt>
<dd>
<div class="desc">
</div>
</dd>
<dt id="anabel.assemble.Model.taprod"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">taprod</span></span>(<span>self, tag: str, iNode, jNode, mat=None, xsec=None, Qpl=None, A=None, E=None)</span>
</code></dt>
<dd>
<div class="desc"><p>Construct a tapered rod element with variable E and A values.</p>
</div>
</dd>
<dt id="anabel.assemble.Model.truss"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">truss</span></span>(<span>self, tag: str, iNode, jNode, elem=None, mat=None, xsec=None, Qpl=None, A=None, E=None)</span>
</code></dt>
<dd>
<div class="desc">
</div>
</dd>
<dt id="anabel.assemble.Model.truss3d"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">truss3d</span></span>(<span>self, tag: str, iNode, jNode, mat=None, xsec=None)</span>
</code></dt>
<dd>
<div class="desc"><p>Add an emme.Truss3d object to model</p>
<h2 id="parameters">Parameters</h2>
</div>
</dd>
<dt id="anabel.assemble.Model.update"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">update</span></span>(<span>self, U)</span>
</code></dt>
<dd>
<div class="desc">
</div>
</dd>
<dt id="anabel.assemble.Model.xsection"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">xsection</span></span>(<span>self, tag: str, A: float, I: float)</span>
</code></dt>
<dd>
<div class="desc">
</div>
</dd>
</dl>
</dd>
<dt id="anabel.assemble.rModel"><code class="flex name class">
<span>class <span class="ident">rModel</span></span>
<span>(</span><span>ndm, ndf)</span>
</code></dt>
<dd>
<div class="desc"><p>Base class for assembler objects.</p>
<p>An assembler is typically characterized by collections of nodes, elements and parameters. The purpose of the assembler is to provide a convenient interface for interacting with and managing these entities.</p>
<p>Basic structural model class</p>
<h2 id="parameters">Parameters</h2>
<dl>
<dt><strong><code>ndm</code></strong> : <code>int</code></dt>
<dd>number of model dimensions
</dd>
<dt><strong><code>ndf</code></strong> : <code>int</code></dt>
<dd>number of degrees of freedom (dofs) at each node
</dd>
</dl>
</div>
<h3>Ancestors</h3>
<ul class="hlist">
<li><a title="anabel.assemble.Model" href="#anabel.assemble.Model">Model</a></li>
<li>anabel.assemble.Assembler</li>
</ul>
<h3>Instance variables</h3>
<dl>
<dt id="anabel.assemble.rModel.cforces"><code class="name">var <span class="ident">cforces</span></code></dt>
<dd>
<div class="desc">
</div>
</dd>
<dt id="anabel.assemble.rModel.nv"><code class="name">var <span class="ident">nv</span></code></dt>
<dd>
<div class="desc"><p>Returns number of element deformations in model</p>
</div>
</dd>
<dt id="anabel.assemble.rModel.triv_forces"><code class="name">var <span class="ident">triv_forces</span></code></dt>
<dd>
<div class="desc"><p>list of trivial axial forces</p>
</div>
</dd>
</dl>
<h3>Methods</h3>
<dl>
<dt id="anabel.assemble.rModel.isortho"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">isortho</span></span>(<span>self, elem)</span>
</code></dt>
<dd>
<div class="desc">
</div>
</dd>
<dt id="anabel.assemble.rModel.numDOF"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">numDOF</span></span>(<span>self)</span>
</code></dt>
<dd>
<div class="desc">
</div>
</dd>
<dt id="anabel.assemble.rModel.numdofs"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">numdofs</span></span>(<span>self)</span>
</code></dt>
<dd>
<div class="desc">
</div>
</dd>
</dl>
<h3>Inherited members</h3>
<ul class="hlist">
<li><code><b><a title="anabel.assemble.Model" href="#anabel.assemble.Model">Model</a></b></code>:
<ul class="hlist">
<li><code><a title="anabel.assemble.Model.NOS" href="#anabel.assemble.Model.NOS">NOS</a></code></li>
<li><code><a title="anabel.assemble.Model.add_element" href="#anabel.assemble.Model.add_element">add_element</a></code></li>
<li><code><a title="anabel.assemble.Model.add_elements" href="#anabel.assemble.Model.add_elements">add_elements</a></code></li>
<li><code><a title="anabel.assemble.Model.assemble_force" href="#anabel.assemble.Model.assemble_force">assemble_force</a></code></li>
<li><code><a title="anabel.assemble.Model.beam" href="#anabel.assemble.Model.beam">beam</a></code></li>
<li><code><a title="anabel.assemble.Model.compose_displ" href="#anabel.assemble.Model.compose_displ">compose_displ</a></code></li>
<li><code><a title="anabel.assemble.Model.dofs" href="#anabel.assemble.Model.dofs">dofs</a></code></li>
<li><code><a title="anabel.assemble.Model.eforces" href="#anabel.assemble.Model.eforces">eforces</a></code></li>
<li><code><a title="anabel.assemble.Model.fix" href="#anabel.assemble.Model.fix">fix</a></code></li>
<li><code><a title="anabel.assemble.Model.frame" href="#anabel.assemble.Model.frame">frame</a></code></li>
<li><code><a title="anabel.assemble.Model.idx_e" href="#anabel.assemble.Model.idx_e">idx_e</a></code></li>
<li><code><a title="anabel.assemble.Model.load" href="#anabel.assemble.Model.load">load</a></code></li>
<li><code><a title="anabel.assemble.Model.load_node" href="#anabel.assemble.Model.load_node">load_node</a></code></li>
<li><code><a title="anabel.assemble.Model.ne" href="#anabel.assemble.Model.ne">ne</a></code></li>
<li><code><a title="anabel.assemble.Model.nf" href="#anabel.assemble.Model.nf">nf</a></code></li>
<li><code><a title="anabel.assemble.Model.node" href="#anabel.assemble.Model.node">node</a></code></li>
<li><code><a title="anabel.assemble.Model.nq" href="#anabel.assemble.Model.nq">nq</a></code></li>
<li><code><a title="anabel.assemble.Model.nr" href="#anabel.assemble.Model.nr">nr</a></code></li>
<li><code><a title="anabel.assemble.Model.nt" href="#anabel.assemble.Model.nt">nt</a></code></li>
<li><code><a title="anabel.assemble.Model.pin" href="#anabel.assemble.Model.pin">pin</a></code></li>
<li><code><a title="anabel.assemble.Model.rdofs" href="#anabel.assemble.Model.rdofs">rdofs</a></code></li>
<li><code><a title="anabel.assemble.Model.redundant" href="#anabel.assemble.Model.redundant">redundant</a></code></li>
<li><code><a title="anabel.assemble.Model.roller" href="#anabel.assemble.Model.roller">roller</a></code></li>
<li><code><a title="anabel.assemble.Model.taprod" href="#anabel.assemble.Model.taprod">taprod</a></code></li>
<li><code><a title="anabel.assemble.Model.truss3d" href="#anabel.assemble.Model.truss3d">truss3d</a></code></li>
</ul>
</li>
</ul>
</dd>
</dl>
</section>
</main>