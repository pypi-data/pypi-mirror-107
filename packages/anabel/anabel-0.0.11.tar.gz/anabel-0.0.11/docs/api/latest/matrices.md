---
title: anabel.matrices
summary: This module provides functions and classes for constructing various structural analysis matrices.
template: pdoc.html
...
<main>
<header>
<!-- <h1 class="title">Module <code>anabel.matrices</code></h1> -->
</header>
<section id="section-intro">
<h1 id="matrix-api">Matrix API</h1>
<p>This module provides functions and classes for constructing various structural analysis matrices.</p>
</section>
<section>
</section>
<section>
</section>
<section>
<h2 class="section-title" id="header-functions">Functions</h2>
<dl>
<dt id="anabel.matrices.A_matrix"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">A_matrix</span></span>(<span>Domain, matrix=None)</span>
</code></dt>
<dd>
<div class="desc"><p>Returns a Kinematic_matrix object</p>
</div>
</dd>
<dt id="anabel.matrices.AssemblyTensor"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">AssemblyTensor</span></span>(<span>Model)</span>
</code></dt>
<dd>
<div class="desc">
</div>
</dd>
<dt id="anabel.matrices.Aub_matrix"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">Aub_matrix</span></span>(<span>model, alpha)</span>
</code></dt>
<dd>
<div class="desc"><p>Return the interaction upperbound matrix</p>
</div>
</dd>
<dt id="anabel.matrices.B_matrix"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">B_matrix</span></span>(<span>model, matrix=None, rng=None)</span>
</code></dt>
<dd>
<div class="desc"><p>Returns a Static_matrix object</p>
</div>
</dd>
<dt id="anabel.matrices.Bh_matrix"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">Bh_matrix</span></span>(<span>model)</span>
</code></dt>
<dd>
<div class="desc"><p>Returns a Static_matrix object</p>
</div>
</dd>
<dt id="anabel.matrices.F_matrix"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">F_matrix</span></span>(<span>Domain)</span>
</code></dt>
<dd>
<div class="desc"><p>Returns a Flexibility_matrix object</p>
</div>
</dd>
<dt id="anabel.matrices.Fs_matrix"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">Fs_matrix</span></span>(<span>model, Roption=True)</span>
</code></dt>
<dd>
<div class="desc"><p>Returns a Flexibility_matrix object</p>
</div>
</dd>
<dt id="anabel.matrices.K_matrix"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">K_matrix</span></span>(<span>Model)</span>
</code></dt>
<dd>
<div class="desc"><p>Returns a Stiffness_matrix object</p>
</div>
</dd>
<dt id="anabel.matrices.K_tensor"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">K_tensor</span></span>(<span>Model, U=None)</span>
</code></dt>
<dd>
<div class="desc"><p>Returns a Stiffness_matrix object</p>
</div>
</dd>
<dt id="anabel.matrices.Ks_matrix"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">Ks_matrix</span></span>(<span>model)</span>
</code></dt>
<dd>
<div class="desc"><p>Returns a Flexibility_matrix object</p>
</div>
</dd>
<dt id="anabel.matrices.Kt_matrix"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">Kt_matrix</span></span>(<span>Model, State)</span>
</code></dt>
<dd>
<div class="desc"><p>Returns a Stiffness_matrix object</p>
</div>
</dd>
<dt id="anabel.matrices.Localize"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">Localize</span></span>(<span>U_vector, P_vector, model=None)</span>
</code></dt>
<dd>
<div class="desc">
</div>
</dd>
<dt id="anabel.matrices.P0_vector"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">P0_vector</span></span>(<span>model)</span>
</code></dt>
<dd>
<div class="desc">
</div>
</dd>
<dt id="anabel.matrices.P_vector"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">P_vector</span></span>(<span>model, vector=None)</span>
</code></dt>
<dd>
<div class="desc">
</div>
</dd>
<dt id="anabel.matrices.Pw_vector"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">Pw_vector</span></span>(<span>model)</span>
</code></dt>
<dd>
<div class="desc">
</div>
</dd>
<dt id="anabel.matrices.Q0_vector"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">Q0_vector</span></span>(<span>model)</span>
</code></dt>
<dd>
<div class="desc"><p>Returns a vector of initial element forces</p>
</div>
</dd>
<dt id="anabel.matrices.Q_vector"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">Q_vector</span></span>(<span>model, vector=None)</span>
</code></dt>
<dd>
<div class="desc"><p>Returns a iForce_vector object</p>
</div>
</dd>
<dt id="anabel.matrices.Qp_vector"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">Qp_vector</span></span>(<span>model)</span>
</code></dt>
<dd>
<div class="desc"><p>Returns a vector of element plastic capacities</p>
</div>
</dd>
<dt id="anabel.matrices.Qpl_vector"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">Qpl_vector</span></span>(<span>model)</span>
</code></dt>
<dd>
<div class="desc"><p>Returns a vector of element plastic capacities</p>
</div>
</dd>
<dt id="anabel.matrices.U_vector"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">U_vector</span></span>(<span>model, vector=None)</span>
</code></dt>
<dd>
<div class="desc"><p>Returns a Displacement_vector object</p>
</div>
</dd>
<dt id="anabel.matrices.V0_vector"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">V0_vector</span></span>(<span>model)</span>
</code></dt>
<dd>
<div class="desc"><p>Returns a Deformation_vector object</p>
</div>
</dd>
<dt id="anabel.matrices.V_vector"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">V_vector</span></span>(<span>model, vector=None)</span>
</code></dt>
<dd>
<div class="desc"><p>Returns a Deformation_vector object</p>
</div>
</dd>
<dt id="anabel.matrices.del_zeros"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">del_zeros</span></span>(<span>mat)</span>
</code></dt>
<dd>
<div class="desc">
</div>
</dd>
<dt id="anabel.matrices.elem_dofs"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">elem_dofs</span></span>(<span>Elem)</span>
</code></dt>
<dd>
<div class="desc">
</div>
</dd>
<dt id="anabel.matrices.nB_matrix"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">nB_matrix</span></span>(<span>model, rng=None)</span>
</code></dt>
<dd>
<div class="desc"><p>Returns a Static_matrix object</p>
</div>
</dd>
<dt id="anabel.matrices.transfer_vars"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">transfer_vars</span></span>(<span>item1, item2)</span>
</code></dt>
<dd>
<div class="desc">
</div>
</dd>
</dl>
</section>
<section>
<h2 class="section-title" id="header-classes">Classes</h2>
<dl>
<dt id="anabel.matrices.Deformation_vector"><code class="flex name class">
<span>class <span class="ident">Deformation_vector</span></span>
<span>(</span><span>arry, model, row_data, Vector=None)</span>
</code></dt>
<dd>
<div class="desc"><p>ndarray(shape, dtype=float, buffer=None, offset=0, strides=None, order=None)</p>
<p>An array object represents a multidimensional, homogeneous array of fixed-size items. An associated data-type object describes the format of each element in the array (its byte-order, how many bytes it occupies in memory, whether it is an integer, a floating point number, or something else, etc.)</p>
<p>Arrays should be constructed using <code>array</code>, <code>zeros</code> or <code>empty</code> (refer to the See Also section below). The parameters given here refer to a low-level method (<code>ndarray(…)</code>) for instantiating an array.</p>
<p>For more information, refer to the <code>numpy</code> module and examine the methods and attributes of an array.</p>
<h2 id="parameters">Parameters</h2>
<p>(for the <strong>new</strong> method; see Notes below)</p>
<dl>
<dt><strong><code>shape</code></strong> : <code>tuple</code> of <code>ints</code></dt>
<dd>Shape of created array.
</dd>
<dt><strong><code>dtype</code></strong> : <code>data-type</code>, optional</dt>
<dd>Any object that can be interpreted as a numpy data type.
</dd>
<dt><strong><code>buffer</code></strong> : <code>object exposing buffer interface</code>, optional</dt>
<dd>Used to fill the array with data.
</dd>
<dt><strong><code>offset</code></strong> : <code>int</code>, optional</dt>
<dd>Offset of array data in buffer.
</dd>
<dt><strong><code>strides</code></strong> : <code>tuple</code> of <code>ints</code>, optional</dt>
<dd>Strides of data in memory.
</dd>
<dt><strong><code>order</code></strong> : <code>{'C', 'F'}</code>, optional</dt>
<dd>Row-major (C-style) or column-major (Fortran-style) order.
</dd>
</dl>
<h2 id="attributes">Attributes</h2>
<dl>
<dt><strong><code>T</code></strong> : <code>ndarray</code></dt>
<dd>Transpose of the array.
</dd>
<dt><strong><code>data</code></strong> : <code>buffer</code></dt>
<dd>The array’s elements, in memory.
</dd>
<dt><strong><code>dtype</code></strong> : <code>dtype object</code></dt>
<dd>Describes the format of the elements in the array.
</dd>
<dt><strong><code>flags</code></strong> : <code>dict</code></dt>
<dd>Dictionary containing information related to memory use, e.g., ‘C_CONTIGUOUS,’ ‘OWNDATA,’ ‘WRITEABLE,’ etc.
</dd>
<dt><strong><code>flat</code></strong> : <code>numpy.flatiter object</code></dt>
<dd>Flattened version of the array as an iterator. The iterator allows assignments, e.g., <code>x.flat = 3</code> (See <code>ndarray.flat</code> for assignment examples; TODO).
</dd>
<dt><strong><code>imag</code></strong> : <code>ndarray</code></dt>
<dd>Imaginary part of the array.
</dd>
<dt><strong><code>real</code></strong> : <code>ndarray</code></dt>
<dd>Real part of the array.
</dd>
<dt><strong><code>size</code></strong> : <code>int</code></dt>
<dd>Number of elements in the array.
</dd>
<dt><strong><code>itemsize</code></strong> : <code>int</code></dt>
<dd>The memory use of each array element in bytes.
</dd>
<dt><strong><code>nbytes</code></strong> : <code>int</code></dt>
<dd>The total number of bytes required to store the array data, i.e., <code>itemsize * size</code>.
</dd>
<dt><strong><code>ndim</code></strong> : <code>int</code></dt>
<dd>The array’s number of dimensions.
</dd>
<dt><strong><code>shape</code></strong> : <code>tuple</code> of <code>ints</code></dt>
<dd>Shape of the array.
</dd>
<dt><strong><code>strides</code></strong> : <code>tuple</code> of <code>ints</code></dt>
<dd>The step-size required to move from one element to the next in memory. For example, a contiguous <code>(3, 4)</code> array of type <code>int16</code> in C-order has strides <code>(8, 2)</code>. This implies that to move from element to element in memory requires jumps of 2 bytes. To move from row-to-row, one needs to jump 8 bytes at a time (<code>2 * 4</code>).
</dd>
<dt><strong><code>ctypes</code></strong> : <code>ctypes object</code></dt>
<dd>Class containing properties of the array needed for interaction with ctypes.
</dd>
<dt><strong><code>base</code></strong> : <code>ndarray</code></dt>
<dd>If the array is a view into another array, that array is its <code>base</code> (unless that array is also a view). The <code>base</code> array is where the array data is actually stored.
</dd>
</dl>
<h2 id="see-also">See Also</h2>
<dl>
<dt><code>array</code></dt>
<dd>Construct an array.
</dd>
<dt><code>zeros</code></dt>
<dd>Create an array, each element of which is zero.
</dd>
<dt><code>empty</code></dt>
<dd>Create an array, but leave its allocated memory unchanged (i.e., it contains “garbage”).
</dd>
<dt><code>dtype</code></dt>
<dd>Create a data-type.
</dd>
</dl>
<h2 id="notes">Notes</h2>
<p>There are two modes of creating an array using <code>__new__</code>:</p>
<ol type="1">
<li>If <code>buffer</code> is None, then only <code>shape</code>, <code>dtype</code>, and <code>order</code> are used.</li>
<li>If <code>buffer</code> is an object exposing the buffer interface, then all keywords are interpreted.</li>
</ol>
<p>No <code>__init__</code> method is needed because the array is fully initialized after the <code>__new__</code> method.</p>
<h2 id="examples">Examples</h2>
<p>These examples illustrate the low-level <code>ndarray</code> constructor. Refer to the <code>See Also</code> section above for easier ways of constructing an ndarray.</p>
<p>First mode, <code>buffer</code> is None:</p>
<pre class="python-repl"><code>&gt;&gt;&gt; np.ndarray(shape=(2,2), dtype=float, order=&#39;F&#39;)
array([[0.0e+000, 0.0e+000], # random
       [     nan, 2.5e-323]])</code></pre>
<p>Second mode:</p>
<pre class="python-repl"><code>&gt;&gt;&gt; np.ndarray((2,), buffer=np.array([1,2,3]),
...            offset=np.int_().itemsize,
...            dtype=int) # offset = 1*itemsize, i.e. skip first element
array([2, 3])</code></pre>
</div>
<h3>Ancestors</h3>
<ul class="hlist">
<li><a title="anabel.matrices.Structural_Vector" href="#anabel.matrices.Structural_Vector">Structural_Vector</a></li>
<li>numpy.ndarray</li>
</ul>
<h3>Class variables</h3>
<dl>
<dt id="anabel.matrices.Deformation_vector.tag"><code class="name">var <span class="ident">tag</span></code></dt>
<dd>
<div class="desc">
</div>
</dd>
</dl>
<h3>Instance variables</h3>
<dl>
<dt id="anabel.matrices.Deformation_vector.c"><code class="name">var <span class="ident">c</span></code></dt>
<dd>
<div class="desc"><p>Removes rows corresponding to element hinges/releases</p>
</div>
</dd>
<dt id="anabel.matrices.Deformation_vector.i"><code class="name">var <span class="ident">i</span></code></dt>
<dd>
<div class="desc"><p>Removes rows corresponding to redundant forces</p>
</div>
</dd>
<dt id="anabel.matrices.Deformation_vector.x"><code class="name">var <span class="ident">x</span></code></dt>
<dd>
<div class="desc"><p>Removes rows of corresponding to primary forces</p>
</div>
</dd>
</dl>
</dd>
<dt id="anabel.matrices.Diag_matrix"><code class="flex name class">
<span>class <span class="ident">Diag_matrix</span></span>
<span>(</span><span>arry, rc_data, model)</span>
</code></dt>
<dd>
<div class="desc"><p>Block diagonal matrix of element flexibility/stiffness matrices for structural model</p>
<p>this class represents the block diagonal matrix of element flexibility or stiffness matrices for a structural model.</p>
<h1 id="parameters">Parameters</h1>
<p>model</p>
</div>
<h3>Ancestors</h3>
<ul class="hlist">
<li><a title="anabel.matrices.Structural_Matrix" href="#anabel.matrices.Structural_Matrix">Structural_Matrix</a></li>
<li>numpy.ndarray</li>
</ul>
<h3>Class variables</h3>
<dl>
<dt id="anabel.matrices.Diag_matrix.tag"><code class="name">var <span class="ident">tag</span></code></dt>
<dd>
<div class="desc">
</div>
</dd>
</dl>
<h3>Instance variables</h3>
<dl>
<dt id="anabel.matrices.Diag_matrix.c"><code class="name">var <span class="ident">c</span></code></dt>
<dd>
<div class="desc"><p>Removes columns corresponding to element hinges/releases</p>
</div>
</dd>
</dl>
<h3>Inherited members</h3>
<ul class="hlist">
<li><code><b><a title="anabel.matrices.Structural_Matrix" href="#anabel.matrices.Structural_Matrix">Structural_Matrix</a></b></code>:
<ul class="hlist">
<li><code><a title="anabel.matrices.Structural_Matrix.del_zeros" href="#anabel.matrices.Structural_Matrix.del_zeros">del_zeros</a></code></li>
<li><code><a title="anabel.matrices.Structural_Matrix.ker" href="#anabel.matrices.Structural_Matrix.ker">ker</a></code></li>
<li><code><a title="anabel.matrices.Structural_Matrix.lns" href="#anabel.matrices.Structural_Matrix.lns">lns</a></code></li>
<li><code><a title="anabel.matrices.Structural_Matrix.nls" href="#anabel.matrices.Structural_Matrix.nls">nls</a></code></li>
<li><code><a title="anabel.matrices.Structural_Matrix.rank" href="#anabel.matrices.Structural_Matrix.rank">rank</a></code></li>
<li><code><a title="anabel.matrices.Structural_Matrix.remove" href="#anabel.matrices.Structural_Matrix.remove">remove</a></code></li>
<li><code><a title="anabel.matrices.Structural_Matrix.round" href="#anabel.matrices.Structural_Matrix.round">round</a></code></li>
</ul>
</li>
</ul>
</dd>
<dt id="anabel.matrices.Displacement_vector"><code class="flex name class">
<span>class <span class="ident">Displacement_vector</span></span>
<span>(</span><span>Kinematic_matrix, Vector=None)</span>
</code></dt>
<dd>
<div class="desc"><p>ndarray(shape, dtype=float, buffer=None, offset=0, strides=None, order=None)</p>
<p>An array object represents a multidimensional, homogeneous array of fixed-size items. An associated data-type object describes the format of each element in the array (its byte-order, how many bytes it occupies in memory, whether it is an integer, a floating point number, or something else, etc.)</p>
<p>Arrays should be constructed using <code>array</code>, <code>zeros</code> or <code>empty</code> (refer to the See Also section below). The parameters given here refer to a low-level method (<code>ndarray(…)</code>) for instantiating an array.</p>
<p>For more information, refer to the <code>numpy</code> module and examine the methods and attributes of an array.</p>
<h2 id="parameters">Parameters</h2>
<p>(for the <strong>new</strong> method; see Notes below)</p>
<dl>
<dt><strong><code>shape</code></strong> : <code>tuple</code> of <code>ints</code></dt>
<dd>Shape of created array.
</dd>
<dt><strong><code>dtype</code></strong> : <code>data-type</code>, optional</dt>
<dd>Any object that can be interpreted as a numpy data type.
</dd>
<dt><strong><code>buffer</code></strong> : <code>object exposing buffer interface</code>, optional</dt>
<dd>Used to fill the array with data.
</dd>
<dt><strong><code>offset</code></strong> : <code>int</code>, optional</dt>
<dd>Offset of array data in buffer.
</dd>
<dt><strong><code>strides</code></strong> : <code>tuple</code> of <code>ints</code>, optional</dt>
<dd>Strides of data in memory.
</dd>
<dt><strong><code>order</code></strong> : <code>{'C', 'F'}</code>, optional</dt>
<dd>Row-major (C-style) or column-major (Fortran-style) order.
</dd>
</dl>
<h2 id="attributes">Attributes</h2>
<dl>
<dt><strong><code>T</code></strong> : <code>ndarray</code></dt>
<dd>Transpose of the array.
</dd>
<dt><strong><code>data</code></strong> : <code>buffer</code></dt>
<dd>The array’s elements, in memory.
</dd>
<dt><strong><code>dtype</code></strong> : <code>dtype object</code></dt>
<dd>Describes the format of the elements in the array.
</dd>
<dt><strong><code>flags</code></strong> : <code>dict</code></dt>
<dd>Dictionary containing information related to memory use, e.g., ‘C_CONTIGUOUS,’ ‘OWNDATA,’ ‘WRITEABLE,’ etc.
</dd>
<dt><strong><code>flat</code></strong> : <code>numpy.flatiter object</code></dt>
<dd>Flattened version of the array as an iterator. The iterator allows assignments, e.g., <code>x.flat = 3</code> (See <code>ndarray.flat</code> for assignment examples; TODO).
</dd>
<dt><strong><code>imag</code></strong> : <code>ndarray</code></dt>
<dd>Imaginary part of the array.
</dd>
<dt><strong><code>real</code></strong> : <code>ndarray</code></dt>
<dd>Real part of the array.
</dd>
<dt><strong><code>size</code></strong> : <code>int</code></dt>
<dd>Number of elements in the array.
</dd>
<dt><strong><code>itemsize</code></strong> : <code>int</code></dt>
<dd>The memory use of each array element in bytes.
</dd>
<dt><strong><code>nbytes</code></strong> : <code>int</code></dt>
<dd>The total number of bytes required to store the array data, i.e., <code>itemsize * size</code>.
</dd>
<dt><strong><code>ndim</code></strong> : <code>int</code></dt>
<dd>The array’s number of dimensions.
</dd>
<dt><strong><code>shape</code></strong> : <code>tuple</code> of <code>ints</code></dt>
<dd>Shape of the array.
</dd>
<dt><strong><code>strides</code></strong> : <code>tuple</code> of <code>ints</code></dt>
<dd>The step-size required to move from one element to the next in memory. For example, a contiguous <code>(3, 4)</code> array of type <code>int16</code> in C-order has strides <code>(8, 2)</code>. This implies that to move from element to element in memory requires jumps of 2 bytes. To move from row-to-row, one needs to jump 8 bytes at a time (<code>2 * 4</code>).
</dd>
<dt><strong><code>ctypes</code></strong> : <code>ctypes object</code></dt>
<dd>Class containing properties of the array needed for interaction with ctypes.
</dd>
<dt><strong><code>base</code></strong> : <code>ndarray</code></dt>
<dd>If the array is a view into another array, that array is its <code>base</code> (unless that array is also a view). The <code>base</code> array is where the array data is actually stored.
</dd>
</dl>
<h2 id="see-also">See Also</h2>
<dl>
<dt><code>array</code></dt>
<dd>Construct an array.
</dd>
<dt><code>zeros</code></dt>
<dd>Create an array, each element of which is zero.
</dd>
<dt><code>empty</code></dt>
<dd>Create an array, but leave its allocated memory unchanged (i.e., it contains “garbage”).
</dd>
<dt><code>dtype</code></dt>
<dd>Create a data-type.
</dd>
</dl>
<h2 id="notes">Notes</h2>
<p>There are two modes of creating an array using <code>__new__</code>:</p>
<ol type="1">
<li>If <code>buffer</code> is None, then only <code>shape</code>, <code>dtype</code>, and <code>order</code> are used.</li>
<li>If <code>buffer</code> is an object exposing the buffer interface, then all keywords are interpreted.</li>
</ol>
<p>No <code>__init__</code> method is needed because the array is fully initialized after the <code>__new__</code> method.</p>
<h2 id="examples">Examples</h2>
<p>These examples illustrate the low-level <code>ndarray</code> constructor. Refer to the <code>See Also</code> section above for easier ways of constructing an ndarray.</p>
<p>First mode, <code>buffer</code> is None:</p>
<pre class="python-repl"><code>&gt;&gt;&gt; np.ndarray(shape=(2,2), dtype=float, order=&#39;F&#39;)
array([[0.0e+000, 0.0e+000], # random
       [     nan, 2.5e-323]])</code></pre>
<p>Second mode:</p>
<pre class="python-repl"><code>&gt;&gt;&gt; np.ndarray((2,), buffer=np.array([1,2,3]),
...            offset=np.int_().itemsize,
...            dtype=int) # offset = 1*itemsize, i.e. skip first element
array([2, 3])</code></pre>
</div>
<h3>Ancestors</h3>
<ul class="hlist">
<li><a title="anabel.matrices.column_vector" href="#anabel.matrices.column_vector">column_vector</a></li>
<li><a title="anabel.matrices.Structural_Vector" href="#anabel.matrices.Structural_Vector">Structural_Vector</a></li>
<li>numpy.ndarray</li>
</ul>
<h3>Class variables</h3>
<dl>
<dt id="anabel.matrices.Displacement_vector.tag"><code class="name">var <span class="ident">tag</span></code></dt>
<dd>
<div class="desc">
</div>
</dd>
</dl>
<h3>Instance variables</h3>
<dl>
<dt id="anabel.matrices.Displacement_vector.f"><code class="name">var <span class="ident">f</span></code></dt>
<dd>
<div class="desc"><p>Removes rows corresponding to fixed dofs</p>
</div>
</dd>
</dl>
</dd>
<dt id="anabel.matrices.Flexibility_matrix"><code class="flex name class">
<span>class <span class="ident">Flexibility_matrix</span></span>
<span>(</span><span>model, Roption=True)</span>
</code></dt>
<dd>
<div class="desc"><h1 id="parameters">Parameters</h1>
<p>model</p>
<hr />
</div>
<h3>Ancestors</h3>
<ul class="hlist">
<li><a title="anabel.matrices.Structural_Matrix" href="#anabel.matrices.Structural_Matrix">Structural_Matrix</a></li>
<li>numpy.ndarray</li>
</ul>
<h3>Class variables</h3>
<dl>
<dt id="anabel.matrices.Flexibility_matrix.tag"><code class="name">var <span class="ident">tag</span></code></dt>
<dd>
<div class="desc">
</div>
</dd>
</dl>
<h3>Instance variables</h3>
<dl>
<dt id="anabel.matrices.Flexibility_matrix.c"><code class="name">var <span class="ident">c</span></code></dt>
<dd>
<div class="desc"><p>Removes rows corresponding to element hinges/releases</p>
</div>
</dd>
</dl>
<h3>Inherited members</h3>
<ul class="hlist">
<li><code><b><a title="anabel.matrices.Structural_Matrix" href="#anabel.matrices.Structural_Matrix">Structural_Matrix</a></b></code>:
<ul class="hlist">
<li><code><a title="anabel.matrices.Structural_Matrix.del_zeros" href="#anabel.matrices.Structural_Matrix.del_zeros">del_zeros</a></code></li>
<li><code><a title="anabel.matrices.Structural_Matrix.ker" href="#anabel.matrices.Structural_Matrix.ker">ker</a></code></li>
<li><code><a title="anabel.matrices.Structural_Matrix.lns" href="#anabel.matrices.Structural_Matrix.lns">lns</a></code></li>
<li><code><a title="anabel.matrices.Structural_Matrix.nls" href="#anabel.matrices.Structural_Matrix.nls">nls</a></code></li>
<li><code><a title="anabel.matrices.Structural_Matrix.rank" href="#anabel.matrices.Structural_Matrix.rank">rank</a></code></li>
<li><code><a title="anabel.matrices.Structural_Matrix.remove" href="#anabel.matrices.Structural_Matrix.remove">remove</a></code></li>
<li><code><a title="anabel.matrices.Structural_Matrix.round" href="#anabel.matrices.Structural_Matrix.round">round</a></code></li>
</ul>
</li>
</ul>
</dd>
<dt id="anabel.matrices.Kinematic_matrix"><code class="flex name class">
<span>class <span class="ident">Kinematic_matrix</span></span>
<span>(</span><span>model, matrix=None, rng=None)</span>
</code></dt>
<dd>
<div class="desc"><p>Class for the kinematic matrix of a structural model with 2d/3d truss and 2d frame elements the function forms the kinematic matrix A for all degrees of freedom and all element deformations of the structural model specified in data structure MODEL the function is currently limited to 2d/3d truss and 2d frame elements</p>
<h2 id="returns">Returns</h2>
<dl>
<dt><code>Kinematic matrix</code></dt>
<dd>
</dd>
</dl>
</div>
<h3>Ancestors</h3>
<ul class="hlist">
<li><a title="anabel.matrices.Structural_Matrix" href="#anabel.matrices.Structural_Matrix">Structural_Matrix</a></li>
<li>numpy.ndarray</li>
</ul>
<h3>Class variables</h3>
<dl>
<dt id="anabel.matrices.Kinematic_matrix.ranges"><code class="name">var <span class="ident">ranges</span></code></dt>
<dd>
<div class="desc">
</div>
</dd>
</dl>
<h3>Instance variables</h3>
<dl>
<dt id="anabel.matrices.Kinematic_matrix.c"><code class="name">var <span class="ident">c</span></code></dt>
<dd>
<div class="desc"><p>Removes rows corresponding to element hinges/releases</p>
</div>
</dd>
<dt id="anabel.matrices.Kinematic_matrix.c0"><code class="name">var <span class="ident">c0</span></code></dt>
<dd>
<div class="desc">
</div>
</dd>
<dt id="anabel.matrices.Kinematic_matrix.d"><code class="name">var <span class="ident">d</span></code></dt>
<dd>
<div class="desc"><p>Removes columns corresponding to free dofs</p>
</div>
</dd>
<dt id="anabel.matrices.Kinematic_matrix.e"><code class="name">var <span class="ident">e</span></code></dt>
<dd>
<div class="desc">
</div>
</dd>
<dt id="anabel.matrices.Kinematic_matrix.f"><code class="name">var <span class="ident">f</span></code></dt>
<dd>
<div class="desc"><p>Removes columns corresponding to fixed dofs</p>
</div>
</dd>
<dt id="anabel.matrices.Kinematic_matrix.i"><code class="name">var <span class="ident">i</span></code></dt>
<dd>
<div class="desc"><p>Removes rows corresponding to redundant forces</p>
</div>
</dd>
<dt id="anabel.matrices.Kinematic_matrix.o"><code class="name">var <span class="ident">o</span></code></dt>
<dd>
<div class="desc">
</div>
</dd>
</dl>
<h3>Methods</h3>
<dl>
<dt id="anabel.matrices.Kinematic_matrix.combine"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">combine</span></span>(<span>self, component)</span>
</code></dt>
<dd>
<div class="desc">
</div>
</dd>
</dl>
<h3>Inherited members</h3>
<ul class="hlist">
<li><code><b><a title="anabel.matrices.Structural_Matrix" href="#anabel.matrices.Structural_Matrix">Structural_Matrix</a></b></code>:
<ul class="hlist">
<li><code><a title="anabel.matrices.Structural_Matrix.del_zeros" href="#anabel.matrices.Structural_Matrix.del_zeros">del_zeros</a></code></li>
<li><code><a title="anabel.matrices.Structural_Matrix.ker" href="#anabel.matrices.Structural_Matrix.ker">ker</a></code></li>
<li><code><a title="anabel.matrices.Structural_Matrix.lns" href="#anabel.matrices.Structural_Matrix.lns">lns</a></code></li>
<li><code><a title="anabel.matrices.Structural_Matrix.nls" href="#anabel.matrices.Structural_Matrix.nls">nls</a></code></li>
<li><code><a title="anabel.matrices.Structural_Matrix.rank" href="#anabel.matrices.Structural_Matrix.rank">rank</a></code></li>
<li><code><a title="anabel.matrices.Structural_Matrix.remove" href="#anabel.matrices.Structural_Matrix.remove">remove</a></code></li>
<li><code><a title="anabel.matrices.Structural_Matrix.round" href="#anabel.matrices.Structural_Matrix.round">round</a></code></li>
</ul>
</li>
</ul>
</dd>
<dt id="anabel.matrices.Mass_matrix"><code class="flex name class">
<span>class <span class="ident">Mass_matrix</span></span>
<span>(</span><span>mat)</span>
</code></dt>
<dd>
<div class="desc"><p>ndarray(shape, dtype=float, buffer=None, offset=0, strides=None, order=None)</p>
<p>An array object represents a multidimensional, homogeneous array of fixed-size items. An associated data-type object describes the format of each element in the array (its byte-order, how many bytes it occupies in memory, whether it is an integer, a floating point number, or something else, etc.)</p>
<p>Arrays should be constructed using <code>array</code>, <code>zeros</code> or <code>empty</code> (refer to the See Also section below). The parameters given here refer to a low-level method (<code>ndarray(…)</code>) for instantiating an array.</p>
<p>For more information, refer to the <code>numpy</code> module and examine the methods and attributes of an array.</p>
<h2 id="parameters">Parameters</h2>
<p>(for the <strong>new</strong> method; see Notes below)</p>
<dl>
<dt><strong><code>shape</code></strong> : <code>tuple</code> of <code>ints</code></dt>
<dd>Shape of created array.
</dd>
<dt><strong><code>dtype</code></strong> : <code>data-type</code>, optional</dt>
<dd>Any object that can be interpreted as a numpy data type.
</dd>
<dt><strong><code>buffer</code></strong> : <code>object exposing buffer interface</code>, optional</dt>
<dd>Used to fill the array with data.
</dd>
<dt><strong><code>offset</code></strong> : <code>int</code>, optional</dt>
<dd>Offset of array data in buffer.
</dd>
<dt><strong><code>strides</code></strong> : <code>tuple</code> of <code>ints</code>, optional</dt>
<dd>Strides of data in memory.
</dd>
<dt><strong><code>order</code></strong> : <code>{'C', 'F'}</code>, optional</dt>
<dd>Row-major (C-style) or column-major (Fortran-style) order.
</dd>
</dl>
<h2 id="attributes">Attributes</h2>
<dl>
<dt><strong><code>T</code></strong> : <code>ndarray</code></dt>
<dd>Transpose of the array.
</dd>
<dt><strong><code>data</code></strong> : <code>buffer</code></dt>
<dd>The array’s elements, in memory.
</dd>
<dt><strong><code>dtype</code></strong> : <code>dtype object</code></dt>
<dd>Describes the format of the elements in the array.
</dd>
<dt><strong><code>flags</code></strong> : <code>dict</code></dt>
<dd>Dictionary containing information related to memory use, e.g., ‘C_CONTIGUOUS,’ ‘OWNDATA,’ ‘WRITEABLE,’ etc.
</dd>
<dt><strong><code>flat</code></strong> : <code>numpy.flatiter object</code></dt>
<dd>Flattened version of the array as an iterator. The iterator allows assignments, e.g., <code>x.flat = 3</code> (See <code>ndarray.flat</code> for assignment examples; TODO).
</dd>
<dt><strong><code>imag</code></strong> : <code>ndarray</code></dt>
<dd>Imaginary part of the array.
</dd>
<dt><strong><code>real</code></strong> : <code>ndarray</code></dt>
<dd>Real part of the array.
</dd>
<dt><strong><code>size</code></strong> : <code>int</code></dt>
<dd>Number of elements in the array.
</dd>
<dt><strong><code>itemsize</code></strong> : <code>int</code></dt>
<dd>The memory use of each array element in bytes.
</dd>
<dt><strong><code>nbytes</code></strong> : <code>int</code></dt>
<dd>The total number of bytes required to store the array data, i.e., <code>itemsize * size</code>.
</dd>
<dt><strong><code>ndim</code></strong> : <code>int</code></dt>
<dd>The array’s number of dimensions.
</dd>
<dt><strong><code>shape</code></strong> : <code>tuple</code> of <code>ints</code></dt>
<dd>Shape of the array.
</dd>
<dt><strong><code>strides</code></strong> : <code>tuple</code> of <code>ints</code></dt>
<dd>The step-size required to move from one element to the next in memory. For example, a contiguous <code>(3, 4)</code> array of type <code>int16</code> in C-order has strides <code>(8, 2)</code>. This implies that to move from element to element in memory requires jumps of 2 bytes. To move from row-to-row, one needs to jump 8 bytes at a time (<code>2 * 4</code>).
</dd>
<dt><strong><code>ctypes</code></strong> : <code>ctypes object</code></dt>
<dd>Class containing properties of the array needed for interaction with ctypes.
</dd>
<dt><strong><code>base</code></strong> : <code>ndarray</code></dt>
<dd>If the array is a view into another array, that array is its <code>base</code> (unless that array is also a view). The <code>base</code> array is where the array data is actually stored.
</dd>
</dl>
<h2 id="see-also">See Also</h2>
<dl>
<dt><code>array</code></dt>
<dd>Construct an array.
</dd>
<dt><code>zeros</code></dt>
<dd>Create an array, each element of which is zero.
</dd>
<dt><code>empty</code></dt>
<dd>Create an array, but leave its allocated memory unchanged (i.e., it contains “garbage”).
</dd>
<dt><code>dtype</code></dt>
<dd>Create a data-type.
</dd>
</dl>
<h2 id="notes">Notes</h2>
<p>There are two modes of creating an array using <code>__new__</code>:</p>
<ol type="1">
<li>If <code>buffer</code> is None, then only <code>shape</code>, <code>dtype</code>, and <code>order</code> are used.</li>
<li>If <code>buffer</code> is an object exposing the buffer interface, then all keywords are interpreted.</li>
</ol>
<p>No <code>__init__</code> method is needed because the array is fully initialized after the <code>__new__</code> method.</p>
<h2 id="examples">Examples</h2>
<p>These examples illustrate the low-level <code>ndarray</code> constructor. Refer to the <code>See Also</code> section above for easier ways of constructing an ndarray.</p>
<p>First mode, <code>buffer</code> is None:</p>
<pre class="python-repl"><code>&gt;&gt;&gt; np.ndarray(shape=(2,2), dtype=float, order=&#39;F&#39;)
array([[0.0e+000, 0.0e+000], # random
       [     nan, 2.5e-323]])</code></pre>
<p>Second mode:</p>
<pre class="python-repl"><code>&gt;&gt;&gt; np.ndarray((2,), buffer=np.array([1,2,3]),
...            offset=np.int_().itemsize,
...            dtype=int) # offset = 1*itemsize, i.e. skip first element
array([2, 3])</code></pre>
</div>
<h3>Ancestors</h3>
<ul class="hlist">
<li><a title="anabel.matrices.Structural_Matrix" href="#anabel.matrices.Structural_Matrix">Structural_Matrix</a></li>
<li>numpy.ndarray</li>
</ul>
<h3>Class variables</h3>
<dl>
<dt id="anabel.matrices.Mass_matrix.tag"><code class="name">var <span class="ident">tag</span></code></dt>
<dd>
<div class="desc">
</div>
</dd>
</dl>
<h3>Instance variables</h3>
<dl>
<dt id="anabel.matrices.Mass_matrix.f"><code class="name">var <span class="ident">f</span></code></dt>
<dd>
<div class="desc">
</div>
</dd>
<dt id="anabel.matrices.Mass_matrix.m"><code class="name">var <span class="ident">m</span></code></dt>
<dd>
<div class="desc">
</div>
</dd>
</dl>
<h3>Inherited members</h3>
<ul class="hlist">
<li><code><b><a title="anabel.matrices.Structural_Matrix" href="#anabel.matrices.Structural_Matrix">Structural_Matrix</a></b></code>:
<ul class="hlist">
<li><code><a title="anabel.matrices.Structural_Matrix.del_zeros" href="#anabel.matrices.Structural_Matrix.del_zeros">del_zeros</a></code></li>
<li><code><a title="anabel.matrices.Structural_Matrix.ker" href="#anabel.matrices.Structural_Matrix.ker">ker</a></code></li>
<li><code><a title="anabel.matrices.Structural_Matrix.lns" href="#anabel.matrices.Structural_Matrix.lns">lns</a></code></li>
<li><code><a title="anabel.matrices.Structural_Matrix.nls" href="#anabel.matrices.Structural_Matrix.nls">nls</a></code></li>
<li><code><a title="anabel.matrices.Structural_Matrix.rank" href="#anabel.matrices.Structural_Matrix.rank">rank</a></code></li>
<li><code><a title="anabel.matrices.Structural_Matrix.remove" href="#anabel.matrices.Structural_Matrix.remove">remove</a></code></li>
<li><code><a title="anabel.matrices.Structural_Matrix.round" href="#anabel.matrices.Structural_Matrix.round">round</a></code></li>
</ul>
</li>
</ul>
</dd>
<dt id="anabel.matrices.Static_matrix"><code class="flex name class">
<span>class <span class="ident">Static_matrix</span></span>
<span>(</span><span>model, matrix=None, rng=None)</span>
</code></dt>
<dd>
<div class="desc"><p>B_MATRIX static matrix of structural model with 2d/3d truss and 2d frame elements the function forms the static matrix B for all degrees of freedom and all basic forces of the structural model specified in data structure MODEL; the function is currently limited to 2d/3d truss and 2d frame elements</p>
<h2 id="parameters">Parameters</h2>
<dl>
<dt><strong><code>model</code></strong> : <code>emme.Model object</code></dt>
<dd>
</dd>
<dt><strong><code>Partitions</code></strong></dt>
<dd>
</dd>
</dl>
<p>=========================================================================================</p>
<ul>
<li><p>B.f : nf x ntq</p></li>
<li><p>B.c : nf x nq</p></li>
<li><p>B.fc : nf x nq</p></li>
<li><p>B.i : ni x nq</p></li>
<li><p>B.x : nx x nq</p></li>
</ul>
<p>where:</p>
<ul>
<li>ni: number of primary (non-redundant) forces.</li>
<li>nq: number of total, continuous forces.</li>
<li>nx: number of redundant forces.</li>
</ul>
</div>
<h3>Ancestors</h3>
<ul class="hlist">
<li><a title="anabel.matrices.Structural_Matrix" href="#anabel.matrices.Structural_Matrix">Structural_Matrix</a></li>
<li>numpy.ndarray</li>
</ul>
<h3>Class variables</h3>
<dl>
<dt id="anabel.matrices.Static_matrix.ranges"><code class="name">var <span class="ident">ranges</span></code></dt>
<dd>
<div class="desc">
</div>
</dd>
</dl>
<h3>Instance variables</h3>
<dl>
<dt id="anabel.matrices.Static_matrix.bari"><code class="name">var <span class="ident">bari</span></code></dt>
<dd>
<div class="desc">
</div>
</dd>
<dt id="anabel.matrices.Static_matrix.barx"><code class="name">var <span class="ident">barx</span></code></dt>
<dd>
<div class="desc">
</div>
</dd>
<dt id="anabel.matrices.Static_matrix.barxi"><code class="name">var <span class="ident">barxi</span></code></dt>
<dd>
<div class="desc">
</div>
</dd>
<dt id="anabel.matrices.Static_matrix.c"><code class="name">var <span class="ident">c</span></code></dt>
<dd>
<div class="desc">
</div>
</dd>
<dt id="anabel.matrices.Static_matrix.c0"><code class="name">var <span class="ident">c0</span></code></dt>
<dd>
<div class="desc">
</div>
</dd>
<dt id="anabel.matrices.Static_matrix.d"><code class="name">var <span class="ident">d</span></code></dt>
<dd>
<div class="desc"><p>Removes rows corresponding to free dofs</p>
</div>
</dd>
<dt id="anabel.matrices.Static_matrix.f"><code class="name">var <span class="ident">f</span></code></dt>
<dd>
<div class="desc">
</div>
</dd>
<dt id="anabel.matrices.Static_matrix.fc"><code class="name">var <span class="ident">fc</span></code></dt>
<dd>
<div class="desc">
</div>
</dd>
<dt id="anabel.matrices.Static_matrix.i"><code class="name">var <span class="ident">i</span></code></dt>
<dd>
<div class="desc"><p>Removes rows of B_matrix corresponding to primary (non-redundant) forces</p>
</div>
</dd>
<dt id="anabel.matrices.Static_matrix.o"><code class="name">var <span class="ident">o</span></code></dt>
<dd>
<div class="desc"><p>Remove columns corresponding to element force releases, then delete zeros</p>
</div>
</dd>
<dt id="anabel.matrices.Static_matrix.x"><code class="name">var <span class="ident">x</span></code></dt>
<dd>
<div class="desc"><p>Removes rows of B_matrix corresponding to primary (non-redundant) forces</p>
</div>
</dd>
</dl>
<h3>Inherited members</h3>
<ul class="hlist">
<li><code><b><a title="anabel.matrices.Structural_Matrix" href="#anabel.matrices.Structural_Matrix">Structural_Matrix</a></b></code>:
<ul class="hlist">
<li><code><a title="anabel.matrices.Structural_Matrix.del_zeros" href="#anabel.matrices.Structural_Matrix.del_zeros">del_zeros</a></code></li>
<li><code><a title="anabel.matrices.Structural_Matrix.ker" href="#anabel.matrices.Structural_Matrix.ker">ker</a></code></li>
<li><code><a title="anabel.matrices.Structural_Matrix.lns" href="#anabel.matrices.Structural_Matrix.lns">lns</a></code></li>
<li><code><a title="anabel.matrices.Structural_Matrix.nls" href="#anabel.matrices.Structural_Matrix.nls">nls</a></code></li>
<li><code><a title="anabel.matrices.Structural_Matrix.rank" href="#anabel.matrices.Structural_Matrix.rank">rank</a></code></li>
<li><code><a title="anabel.matrices.Structural_Matrix.remove" href="#anabel.matrices.Structural_Matrix.remove">remove</a></code></li>
<li><code><a title="anabel.matrices.Structural_Matrix.round" href="#anabel.matrices.Structural_Matrix.round">round</a></code></li>
</ul>
</li>
</ul>
</dd>
<dt id="anabel.matrices.Stiffness_matrix"><code class="flex name class">
<span>class <span class="ident">Stiffness_matrix</span></span>
<span>(</span><span>arry, model, Roption=None)</span>
</code></dt>
<dd>
<div class="desc"><p>… Parameters ============ model</p>
<hr />
</div>
<h3>Ancestors</h3>
<ul class="hlist">
<li><a title="anabel.matrices.Structural_Matrix" href="#anabel.matrices.Structural_Matrix">Structural_Matrix</a></li>
<li>numpy.ndarray</li>
</ul>
<h3>Class variables</h3>
<dl>
<dt id="anabel.matrices.Stiffness_matrix.tag"><code class="name">var <span class="ident">tag</span></code></dt>
<dd>
<div class="desc">
</div>
</dd>
</dl>
<h3>Instance variables</h3>
<dl>
<dt id="anabel.matrices.Stiffness_matrix.f"><code class="name">var <span class="ident">f</span></code></dt>
<dd>
<div class="desc">
</div>
</dd>
</dl>
<h3>Inherited members</h3>
<ul class="hlist">
<li><code><b><a title="anabel.matrices.Structural_Matrix" href="#anabel.matrices.Structural_Matrix">Structural_Matrix</a></b></code>:
<ul class="hlist">
<li><code><a title="anabel.matrices.Structural_Matrix.del_zeros" href="#anabel.matrices.Structural_Matrix.del_zeros">del_zeros</a></code></li>
<li><code><a title="anabel.matrices.Structural_Matrix.ker" href="#anabel.matrices.Structural_Matrix.ker">ker</a></code></li>
<li><code><a title="anabel.matrices.Structural_Matrix.lns" href="#anabel.matrices.Structural_Matrix.lns">lns</a></code></li>
<li><code><a title="anabel.matrices.Structural_Matrix.nls" href="#anabel.matrices.Structural_Matrix.nls">nls</a></code></li>
<li><code><a title="anabel.matrices.Structural_Matrix.rank" href="#anabel.matrices.Structural_Matrix.rank">rank</a></code></li>
<li><code><a title="anabel.matrices.Structural_Matrix.remove" href="#anabel.matrices.Structural_Matrix.remove">remove</a></code></li>
<li><code><a title="anabel.matrices.Structural_Matrix.round" href="#anabel.matrices.Structural_Matrix.round">round</a></code></li>
</ul>
</li>
</ul>
</dd>
<dt id="anabel.matrices.Structural_Matrix"><code class="flex name class">
<span>class <span class="ident">Structural_Matrix</span></span>
<span>(</span><span>mat)</span>
</code></dt>
<dd>
<div class="desc"><p>ndarray(shape, dtype=float, buffer=None, offset=0, strides=None, order=None)</p>
<p>An array object represents a multidimensional, homogeneous array of fixed-size items. An associated data-type object describes the format of each element in the array (its byte-order, how many bytes it occupies in memory, whether it is an integer, a floating point number, or something else, etc.)</p>
<p>Arrays should be constructed using <code>array</code>, <code>zeros</code> or <code>empty</code> (refer to the See Also section below). The parameters given here refer to a low-level method (<code>ndarray(…)</code>) for instantiating an array.</p>
<p>For more information, refer to the <code>numpy</code> module and examine the methods and attributes of an array.</p>
<h2 id="parameters">Parameters</h2>
<p>(for the <strong>new</strong> method; see Notes below)</p>
<dl>
<dt><strong><code>shape</code></strong> : <code>tuple</code> of <code>ints</code></dt>
<dd>Shape of created array.
</dd>
<dt><strong><code>dtype</code></strong> : <code>data-type</code>, optional</dt>
<dd>Any object that can be interpreted as a numpy data type.
</dd>
<dt><strong><code>buffer</code></strong> : <code>object exposing buffer interface</code>, optional</dt>
<dd>Used to fill the array with data.
</dd>
<dt><strong><code>offset</code></strong> : <code>int</code>, optional</dt>
<dd>Offset of array data in buffer.
</dd>
<dt><strong><code>strides</code></strong> : <code>tuple</code> of <code>ints</code>, optional</dt>
<dd>Strides of data in memory.
</dd>
<dt><strong><code>order</code></strong> : <code>{'C', 'F'}</code>, optional</dt>
<dd>Row-major (C-style) or column-major (Fortran-style) order.
</dd>
</dl>
<h2 id="attributes">Attributes</h2>
<dl>
<dt><strong><code>T</code></strong> : <code>ndarray</code></dt>
<dd>Transpose of the array.
</dd>
<dt><strong><code>data</code></strong> : <code>buffer</code></dt>
<dd>The array’s elements, in memory.
</dd>
<dt><strong><code>dtype</code></strong> : <code>dtype object</code></dt>
<dd>Describes the format of the elements in the array.
</dd>
<dt><strong><code>flags</code></strong> : <code>dict</code></dt>
<dd>Dictionary containing information related to memory use, e.g., ‘C_CONTIGUOUS,’ ‘OWNDATA,’ ‘WRITEABLE,’ etc.
</dd>
<dt><strong><code>flat</code></strong> : <code>numpy.flatiter object</code></dt>
<dd>Flattened version of the array as an iterator. The iterator allows assignments, e.g., <code>x.flat = 3</code> (See <code>ndarray.flat</code> for assignment examples; TODO).
</dd>
<dt><strong><code>imag</code></strong> : <code>ndarray</code></dt>
<dd>Imaginary part of the array.
</dd>
<dt><strong><code>real</code></strong> : <code>ndarray</code></dt>
<dd>Real part of the array.
</dd>
<dt><strong><code>size</code></strong> : <code>int</code></dt>
<dd>Number of elements in the array.
</dd>
<dt><strong><code>itemsize</code></strong> : <code>int</code></dt>
<dd>The memory use of each array element in bytes.
</dd>
<dt><strong><code>nbytes</code></strong> : <code>int</code></dt>
<dd>The total number of bytes required to store the array data, i.e., <code>itemsize * size</code>.
</dd>
<dt><strong><code>ndim</code></strong> : <code>int</code></dt>
<dd>The array’s number of dimensions.
</dd>
<dt><strong><code>shape</code></strong> : <code>tuple</code> of <code>ints</code></dt>
<dd>Shape of the array.
</dd>
<dt><strong><code>strides</code></strong> : <code>tuple</code> of <code>ints</code></dt>
<dd>The step-size required to move from one element to the next in memory. For example, a contiguous <code>(3, 4)</code> array of type <code>int16</code> in C-order has strides <code>(8, 2)</code>. This implies that to move from element to element in memory requires jumps of 2 bytes. To move from row-to-row, one needs to jump 8 bytes at a time (<code>2 * 4</code>).
</dd>
<dt><strong><code>ctypes</code></strong> : <code>ctypes object</code></dt>
<dd>Class containing properties of the array needed for interaction with ctypes.
</dd>
<dt><strong><code>base</code></strong> : <code>ndarray</code></dt>
<dd>If the array is a view into another array, that array is its <code>base</code> (unless that array is also a view). The <code>base</code> array is where the array data is actually stored.
</dd>
</dl>
<h2 id="see-also">See Also</h2>
<dl>
<dt><code>array</code></dt>
<dd>Construct an array.
</dd>
<dt><code>zeros</code></dt>
<dd>Create an array, each element of which is zero.
</dd>
<dt><code>empty</code></dt>
<dd>Create an array, but leave its allocated memory unchanged (i.e., it contains “garbage”).
</dd>
<dt><code>dtype</code></dt>
<dd>Create a data-type.
</dd>
</dl>
<h2 id="notes">Notes</h2>
<p>There are two modes of creating an array using <code>__new__</code>:</p>
<ol type="1">
<li>If <code>buffer</code> is None, then only <code>shape</code>, <code>dtype</code>, and <code>order</code> are used.</li>
<li>If <code>buffer</code> is an object exposing the buffer interface, then all keywords are interpreted.</li>
</ol>
<p>No <code>__init__</code> method is needed because the array is fully initialized after the <code>__new__</code> method.</p>
<h2 id="examples">Examples</h2>
<p>These examples illustrate the low-level <code>ndarray</code> constructor. Refer to the <code>See Also</code> section above for easier ways of constructing an ndarray.</p>
<p>First mode, <code>buffer</code> is None:</p>
<pre class="python-repl"><code>&gt;&gt;&gt; np.ndarray(shape=(2,2), dtype=float, order=&#39;F&#39;)
array([[0.0e+000, 0.0e+000], # random
       [     nan, 2.5e-323]])</code></pre>
<p>Second mode:</p>
<pre class="python-repl"><code>&gt;&gt;&gt; np.ndarray((2,), buffer=np.array([1,2,3]),
...            offset=np.int_().itemsize,
...            dtype=int) # offset = 1*itemsize, i.e. skip first element
array([2, 3])</code></pre>
</div>
<h3>Ancestors</h3>
<ul class="hlist">
<li>numpy.ndarray</li>
</ul>
<h3>Subclasses</h3>
<ul class="hlist">
<li><a title="anabel.matrices.Diag_matrix" href="#anabel.matrices.Diag_matrix">Diag_matrix</a></li>
<li><a title="anabel.matrices.Flexibility_matrix" href="#anabel.matrices.Flexibility_matrix">Flexibility_matrix</a></li>
<li><a title="anabel.matrices.Kinematic_matrix" href="#anabel.matrices.Kinematic_matrix">Kinematic_matrix</a></li>
<li><a title="anabel.matrices.Mass_matrix" href="#anabel.matrices.Mass_matrix">Mass_matrix</a></li>
<li><a title="anabel.matrices.Static_matrix" href="#anabel.matrices.Static_matrix">Static_matrix</a></li>
<li><a title="anabel.matrices.Stiffness_matrix" href="#anabel.matrices.Stiffness_matrix">Stiffness_matrix</a></li>
<li><a title="anabel.matrices.nKinematic_matrix" href="#anabel.matrices.nKinematic_matrix">nKinematic_matrix</a></li>
<li><a title="anabel.matrices.nStatic_matrix" href="#anabel.matrices.nStatic_matrix">nStatic_matrix</a></li>
</ul>
<h3>Class variables</h3>
<dl>
<dt id="anabel.matrices.Structural_Matrix.c_cidx"><code class="name">var <span class="ident">c_cidx</span></code></dt>
<dd>
<div class="desc">
</div>
</dd>
<dt id="anabel.matrices.Structural_Matrix.c_ridx"><code class="name">var <span class="ident">c_ridx</span></code></dt>
<dd>
<div class="desc">
</div>
</dd>
<dt id="anabel.matrices.Structural_Matrix.column_data"><code class="name">var <span class="ident">column_data</span></code></dt>
<dd>
<div class="desc">
</div>
</dd>
<dt id="anabel.matrices.Structural_Matrix.row_data"><code class="name">var <span class="ident">row_data</span></code></dt>
<dd>
<div class="desc">
</div>
</dd>
<dt id="anabel.matrices.Structural_Matrix.tag"><code class="name">var <span class="ident">tag</span></code></dt>
<dd>
<div class="desc">
</div>
</dd>
</dl>
<h3>Instance variables</h3>
<dl>
<dt id="anabel.matrices.Structural_Matrix.c"><code class="name">var <span class="ident">c</span></code></dt>
<dd>
<div class="desc">
</div>
</dd>
<dt id="anabel.matrices.Structural_Matrix.df"><code class="name">var <span class="ident">df</span></code></dt>
<dd>
<div class="desc">
</div>
</dd>
<dt id="anabel.matrices.Structural_Matrix.disp"><code class="name">var <span class="ident">disp</span></code></dt>
<dd>
<div class="desc">
</div>
</dd>
<dt id="anabel.matrices.Structural_Matrix.inv"><code class="name">var <span class="ident">inv</span></code></dt>
<dd>
<div class="desc">
</div>
</dd>
<dt id="anabel.matrices.Structural_Matrix.ker"><code class="name">var <span class="ident">ker</span></code></dt>
<dd>
<div class="desc"><p>Return a basis for the kernel (nullspace) of a matrix.</p>
</div>
</dd>
<dt id="anabel.matrices.Structural_Matrix.lns"><code class="name">var <span class="ident">lns</span></code></dt>
<dd>
<div class="desc"><p>Return a basis for the left nullspace of a matrix.</p>
</div>
</dd>
<dt id="anabel.matrices.Structural_Matrix.nls"><code class="name">var <span class="ident">nls</span></code></dt>
<dd>
<div class="desc"><p>return a basis for the nullspace of matrix.</p>
</div>
</dd>
<dt id="anabel.matrices.Structural_Matrix.rank"><code class="name">var <span class="ident">rank</span></code></dt>
<dd>
<div class="desc"><p>Return the rank of a matrix</p>
</div>
</dd>
</dl>
<h3>Methods</h3>
<dl>
<dt id="anabel.matrices.Structural_Matrix.add_cols"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">add_cols</span></span>(<span>self, component)</span>
</code></dt>
<dd>
<div class="desc">
</div>
</dd>
<dt id="anabel.matrices.Structural_Matrix.add_rows"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">add_rows</span></span>(<span>self, component)</span>
</code></dt>
<dd>
<div class="desc">
</div>
</dd>
<dt id="anabel.matrices.Structural_Matrix.del_zeros"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">del_zeros</span></span>(<span>self)</span>
</code></dt>
<dd>
<div class="desc"><p>Delete rows and columns of a matrix with all zeros</p>
</div>
</dd>
<dt id="anabel.matrices.Structural_Matrix.get"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">get</span></span>(<span>self, row_name, col_name)</span>
</code></dt>
<dd>
<div class="desc">
</div>
</dd>
<dt id="anabel.matrices.Structural_Matrix.lu"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">lu</span></span>(<span>self)</span>
</code></dt>
<dd>
<div class="desc">
</div>
</dd>
<dt id="anabel.matrices.Structural_Matrix.remove"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">remove</span></span>(<span>self, component)</span>
</code></dt>
<dd>
<div class="desc"><p>Remove items by looking up column_data/row_data</p>
</div>
</dd>
<dt id="anabel.matrices.Structural_Matrix.round"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">round</span></span>(<span>self, num)</span>
</code></dt>
<dd>
<div class="desc"><p>a.round(decimals=0, out=None)</p>
<p>Return <code>a</code> with each element rounded to the given number of decimals.</p>
<p>Refer to <code>numpy.around</code> for full documentation.</p>
<h2 id="see-also">See Also</h2>
<dl>
<dt><code>numpy.around</code></dt>
<dd>equivalent function
</dd>
</dl>
</div>
</dd>
<dt id="anabel.matrices.Structural_Matrix.rows"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">rows</span></span>(<span>self, component)</span>
</code></dt>
<dd>
<div class="desc">
</div>
</dd>
</dl>
</dd>
<dt id="anabel.matrices.Structural_Vector"><code class="flex name class">
<span>class <span class="ident">Structural_Vector</span></span>
<span>(</span><span>mat)</span>
</code></dt>
<dd>
<div class="desc"><p>ndarray(shape, dtype=float, buffer=None, offset=0, strides=None, order=None)</p>
<p>An array object represents a multidimensional, homogeneous array of fixed-size items. An associated data-type object describes the format of each element in the array (its byte-order, how many bytes it occupies in memory, whether it is an integer, a floating point number, or something else, etc.)</p>
<p>Arrays should be constructed using <code>array</code>, <code>zeros</code> or <code>empty</code> (refer to the See Also section below). The parameters given here refer to a low-level method (<code>ndarray(…)</code>) for instantiating an array.</p>
<p>For more information, refer to the <code>numpy</code> module and examine the methods and attributes of an array.</p>
<h2 id="parameters">Parameters</h2>
<p>(for the <strong>new</strong> method; see Notes below)</p>
<dl>
<dt><strong><code>shape</code></strong> : <code>tuple</code> of <code>ints</code></dt>
<dd>Shape of created array.
</dd>
<dt><strong><code>dtype</code></strong> : <code>data-type</code>, optional</dt>
<dd>Any object that can be interpreted as a numpy data type.
</dd>
<dt><strong><code>buffer</code></strong> : <code>object exposing buffer interface</code>, optional</dt>
<dd>Used to fill the array with data.
</dd>
<dt><strong><code>offset</code></strong> : <code>int</code>, optional</dt>
<dd>Offset of array data in buffer.
</dd>
<dt><strong><code>strides</code></strong> : <code>tuple</code> of <code>ints</code>, optional</dt>
<dd>Strides of data in memory.
</dd>
<dt><strong><code>order</code></strong> : <code>{'C', 'F'}</code>, optional</dt>
<dd>Row-major (C-style) or column-major (Fortran-style) order.
</dd>
</dl>
<h2 id="attributes">Attributes</h2>
<dl>
<dt><strong><code>T</code></strong> : <code>ndarray</code></dt>
<dd>Transpose of the array.
</dd>
<dt><strong><code>data</code></strong> : <code>buffer</code></dt>
<dd>The array’s elements, in memory.
</dd>
<dt><strong><code>dtype</code></strong> : <code>dtype object</code></dt>
<dd>Describes the format of the elements in the array.
</dd>
<dt><strong><code>flags</code></strong> : <code>dict</code></dt>
<dd>Dictionary containing information related to memory use, e.g., ‘C_CONTIGUOUS,’ ‘OWNDATA,’ ‘WRITEABLE,’ etc.
</dd>
<dt><strong><code>flat</code></strong> : <code>numpy.flatiter object</code></dt>
<dd>Flattened version of the array as an iterator. The iterator allows assignments, e.g., <code>x.flat = 3</code> (See <code>ndarray.flat</code> for assignment examples; TODO).
</dd>
<dt><strong><code>imag</code></strong> : <code>ndarray</code></dt>
<dd>Imaginary part of the array.
</dd>
<dt><strong><code>real</code></strong> : <code>ndarray</code></dt>
<dd>Real part of the array.
</dd>
<dt><strong><code>size</code></strong> : <code>int</code></dt>
<dd>Number of elements in the array.
</dd>
<dt><strong><code>itemsize</code></strong> : <code>int</code></dt>
<dd>The memory use of each array element in bytes.
</dd>
<dt><strong><code>nbytes</code></strong> : <code>int</code></dt>
<dd>The total number of bytes required to store the array data, i.e., <code>itemsize * size</code>.
</dd>
<dt><strong><code>ndim</code></strong> : <code>int</code></dt>
<dd>The array’s number of dimensions.
</dd>
<dt><strong><code>shape</code></strong> : <code>tuple</code> of <code>ints</code></dt>
<dd>Shape of the array.
</dd>
<dt><strong><code>strides</code></strong> : <code>tuple</code> of <code>ints</code></dt>
<dd>The step-size required to move from one element to the next in memory. For example, a contiguous <code>(3, 4)</code> array of type <code>int16</code> in C-order has strides <code>(8, 2)</code>. This implies that to move from element to element in memory requires jumps of 2 bytes. To move from row-to-row, one needs to jump 8 bytes at a time (<code>2 * 4</code>).
</dd>
<dt><strong><code>ctypes</code></strong> : <code>ctypes object</code></dt>
<dd>Class containing properties of the array needed for interaction with ctypes.
</dd>
<dt><strong><code>base</code></strong> : <code>ndarray</code></dt>
<dd>If the array is a view into another array, that array is its <code>base</code> (unless that array is also a view). The <code>base</code> array is where the array data is actually stored.
</dd>
</dl>
<h2 id="see-also">See Also</h2>
<dl>
<dt><code>array</code></dt>
<dd>Construct an array.
</dd>
<dt><code>zeros</code></dt>
<dd>Create an array, each element of which is zero.
</dd>
<dt><code>empty</code></dt>
<dd>Create an array, but leave its allocated memory unchanged (i.e., it contains “garbage”).
</dd>
<dt><code>dtype</code></dt>
<dd>Create a data-type.
</dd>
</dl>
<h2 id="notes">Notes</h2>
<p>There are two modes of creating an array using <code>__new__</code>:</p>
<ol type="1">
<li>If <code>buffer</code> is None, then only <code>shape</code>, <code>dtype</code>, and <code>order</code> are used.</li>
<li>If <code>buffer</code> is an object exposing the buffer interface, then all keywords are interpreted.</li>
</ol>
<p>No <code>__init__</code> method is needed because the array is fully initialized after the <code>__new__</code> method.</p>
<h2 id="examples">Examples</h2>
<p>These examples illustrate the low-level <code>ndarray</code> constructor. Refer to the <code>See Also</code> section above for easier ways of constructing an ndarray.</p>
<p>First mode, <code>buffer</code> is None:</p>
<pre class="python-repl"><code>&gt;&gt;&gt; np.ndarray(shape=(2,2), dtype=float, order=&#39;F&#39;)
array([[0.0e+000, 0.0e+000], # random
       [     nan, 2.5e-323]])</code></pre>
<p>Second mode:</p>
<pre class="python-repl"><code>&gt;&gt;&gt; np.ndarray((2,), buffer=np.array([1,2,3]),
...            offset=np.int_().itemsize,
...            dtype=int) # offset = 1*itemsize, i.e. skip first element
array([2, 3])</code></pre>
</div>
<h3>Ancestors</h3>
<ul class="hlist">
<li>numpy.ndarray</li>
</ul>
<h3>Subclasses</h3>
<ul class="hlist">
<li><a title="anabel.matrices.Deformation_vector" href="#anabel.matrices.Deformation_vector">Deformation_vector</a></li>
<li><a title="anabel.matrices.column_vector" href="#anabel.matrices.column_vector">column_vector</a></li>
<li><a title="anabel.matrices.iForce_vector" href="#anabel.matrices.iForce_vector">iForce_vector</a></li>
<li><a title="anabel.matrices.nDisplacement_vector" href="#anabel.matrices.nDisplacement_vector">nDisplacement_vector</a></li>
<li><a title="anabel.matrices.nForce_vector" href="#anabel.matrices.nForce_vector">nForce_vector</a></li>
<li><a title="anabel.matrices.row_vector" href="#anabel.matrices.row_vector">row_vector</a></li>
</ul>
<h3>Class variables</h3>
<dl>
<dt id="anabel.matrices.Structural_Vector.column_data"><code class="name">var <span class="ident">column_data</span></code></dt>
<dd>
<div class="desc">
</div>
</dd>
<dt id="anabel.matrices.Structural_Vector.row_data"><code class="name">var <span class="ident">row_data</span></code></dt>
<dd>
<div class="desc">
</div>
</dd>
<dt id="anabel.matrices.Structural_Vector.subs"><code class="name">var <span class="ident">subs</span></code></dt>
<dd>
<div class="desc">
</div>
</dd>
<dt id="anabel.matrices.Structural_Vector.tag"><code class="name">var <span class="ident">tag</span></code></dt>
<dd>
<div class="desc">
</div>
</dd>
</dl>
<h3>Instance variables</h3>
<dl>
<dt id="anabel.matrices.Structural_Vector.df"><code class="name">var <span class="ident">df</span></code></dt>
<dd>
<div class="desc">
</div>
</dd>
<dt id="anabel.matrices.Structural_Vector.disp"><code class="name">var <span class="ident">disp</span></code></dt>
<dd>
<div class="desc">
</div>
</dd>
<dt id="anabel.matrices.Structural_Vector.symb"><code class="name">var <span class="ident">symb</span></code></dt>
<dd>
<div class="desc">
</div>
</dd>
</dl>
<h3>Methods</h3>
<dl>
<dt id="anabel.matrices.Structural_Vector.get"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">get</span></span>(<span>self, key)</span>
</code></dt>
<dd>
<div class="desc">
</div>
</dd>
<dt id="anabel.matrices.Structural_Vector.rows"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">rows</span></span>(<span>self, component)</span>
</code></dt>
<dd>
<div class="desc">
</div>
</dd>
<dt id="anabel.matrices.Structural_Vector.set_item"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">set_item</span></span>(<span>self, key, value)</span>
</code></dt>
<dd>
<div class="desc">
</div>
</dd>
</dl>
</dd>
<dt id="anabel.matrices.column_vector"><code class="flex name class">
<span>class <span class="ident">column_vector</span></span>
<span>(</span><span>Matrix, Vector=None)</span>
</code></dt>
<dd>
<div class="desc"><p>ndarray(shape, dtype=float, buffer=None, offset=0, strides=None, order=None)</p>
<p>An array object represents a multidimensional, homogeneous array of fixed-size items. An associated data-type object describes the format of each element in the array (its byte-order, how many bytes it occupies in memory, whether it is an integer, a floating point number, or something else, etc.)</p>
<p>Arrays should be constructed using <code>array</code>, <code>zeros</code> or <code>empty</code> (refer to the See Also section below). The parameters given here refer to a low-level method (<code>ndarray(…)</code>) for instantiating an array.</p>
<p>For more information, refer to the <code>numpy</code> module and examine the methods and attributes of an array.</p>
<h2 id="parameters">Parameters</h2>
<p>(for the <strong>new</strong> method; see Notes below)</p>
<dl>
<dt><strong><code>shape</code></strong> : <code>tuple</code> of <code>ints</code></dt>
<dd>Shape of created array.
</dd>
<dt><strong><code>dtype</code></strong> : <code>data-type</code>, optional</dt>
<dd>Any object that can be interpreted as a numpy data type.
</dd>
<dt><strong><code>buffer</code></strong> : <code>object exposing buffer interface</code>, optional</dt>
<dd>Used to fill the array with data.
</dd>
<dt><strong><code>offset</code></strong> : <code>int</code>, optional</dt>
<dd>Offset of array data in buffer.
</dd>
<dt><strong><code>strides</code></strong> : <code>tuple</code> of <code>ints</code>, optional</dt>
<dd>Strides of data in memory.
</dd>
<dt><strong><code>order</code></strong> : <code>{'C', 'F'}</code>, optional</dt>
<dd>Row-major (C-style) or column-major (Fortran-style) order.
</dd>
</dl>
<h2 id="attributes">Attributes</h2>
<dl>
<dt><strong><code>T</code></strong> : <code>ndarray</code></dt>
<dd>Transpose of the array.
</dd>
<dt><strong><code>data</code></strong> : <code>buffer</code></dt>
<dd>The array’s elements, in memory.
</dd>
<dt><strong><code>dtype</code></strong> : <code>dtype object</code></dt>
<dd>Describes the format of the elements in the array.
</dd>
<dt><strong><code>flags</code></strong> : <code>dict</code></dt>
<dd>Dictionary containing information related to memory use, e.g., ‘C_CONTIGUOUS,’ ‘OWNDATA,’ ‘WRITEABLE,’ etc.
</dd>
<dt><strong><code>flat</code></strong> : <code>numpy.flatiter object</code></dt>
<dd>Flattened version of the array as an iterator. The iterator allows assignments, e.g., <code>x.flat = 3</code> (See <code>ndarray.flat</code> for assignment examples; TODO).
</dd>
<dt><strong><code>imag</code></strong> : <code>ndarray</code></dt>
<dd>Imaginary part of the array.
</dd>
<dt><strong><code>real</code></strong> : <code>ndarray</code></dt>
<dd>Real part of the array.
</dd>
<dt><strong><code>size</code></strong> : <code>int</code></dt>
<dd>Number of elements in the array.
</dd>
<dt><strong><code>itemsize</code></strong> : <code>int</code></dt>
<dd>The memory use of each array element in bytes.
</dd>
<dt><strong><code>nbytes</code></strong> : <code>int</code></dt>
<dd>The total number of bytes required to store the array data, i.e., <code>itemsize * size</code>.
</dd>
<dt><strong><code>ndim</code></strong> : <code>int</code></dt>
<dd>The array’s number of dimensions.
</dd>
<dt><strong><code>shape</code></strong> : <code>tuple</code> of <code>ints</code></dt>
<dd>Shape of the array.
</dd>
<dt><strong><code>strides</code></strong> : <code>tuple</code> of <code>ints</code></dt>
<dd>The step-size required to move from one element to the next in memory. For example, a contiguous <code>(3, 4)</code> array of type <code>int16</code> in C-order has strides <code>(8, 2)</code>. This implies that to move from element to element in memory requires jumps of 2 bytes. To move from row-to-row, one needs to jump 8 bytes at a time (<code>2 * 4</code>).
</dd>
<dt><strong><code>ctypes</code></strong> : <code>ctypes object</code></dt>
<dd>Class containing properties of the array needed for interaction with ctypes.
</dd>
<dt><strong><code>base</code></strong> : <code>ndarray</code></dt>
<dd>If the array is a view into another array, that array is its <code>base</code> (unless that array is also a view). The <code>base</code> array is where the array data is actually stored.
</dd>
</dl>
<h2 id="see-also">See Also</h2>
<dl>
<dt><code>array</code></dt>
<dd>Construct an array.
</dd>
<dt><code>zeros</code></dt>
<dd>Create an array, each element of which is zero.
</dd>
<dt><code>empty</code></dt>
<dd>Create an array, but leave its allocated memory unchanged (i.e., it contains “garbage”).
</dd>
<dt><code>dtype</code></dt>
<dd>Create a data-type.
</dd>
</dl>
<h2 id="notes">Notes</h2>
<p>There are two modes of creating an array using <code>__new__</code>:</p>
<ol type="1">
<li>If <code>buffer</code> is None, then only <code>shape</code>, <code>dtype</code>, and <code>order</code> are used.</li>
<li>If <code>buffer</code> is an object exposing the buffer interface, then all keywords are interpreted.</li>
</ol>
<p>No <code>__init__</code> method is needed because the array is fully initialized after the <code>__new__</code> method.</p>
<h2 id="examples">Examples</h2>
<p>These examples illustrate the low-level <code>ndarray</code> constructor. Refer to the <code>See Also</code> section above for easier ways of constructing an ndarray.</p>
<p>First mode, <code>buffer</code> is None:</p>
<pre class="python-repl"><code>&gt;&gt;&gt; np.ndarray(shape=(2,2), dtype=float, order=&#39;F&#39;)
array([[0.0e+000, 0.0e+000], # random
       [     nan, 2.5e-323]])</code></pre>
<p>Second mode:</p>
<pre class="python-repl"><code>&gt;&gt;&gt; np.ndarray((2,), buffer=np.array([1,2,3]),
...            offset=np.int_().itemsize,
...            dtype=int) # offset = 1*itemsize, i.e. skip first element
array([2, 3])</code></pre>
</div>
<h3>Ancestors</h3>
<ul class="hlist">
<li><a title="anabel.matrices.Structural_Vector" href="#anabel.matrices.Structural_Vector">Structural_Vector</a></li>
<li>numpy.ndarray</li>
</ul>
<h3>Subclasses</h3>
<ul class="hlist">
<li><a title="anabel.matrices.Displacement_vector" href="#anabel.matrices.Displacement_vector">Displacement_vector</a></li>
</ul>
</dd>
<dt id="anabel.matrices.iForce_vector"><code class="flex name class">
<span>class <span class="ident">iForce_vector</span></span>
<span>(</span><span>arry, model, row_data, Vector=None)</span>
</code></dt>
<dd>
<div class="desc"><p>ndarray(shape, dtype=float, buffer=None, offset=0, strides=None, order=None)</p>
<p>An array object represents a multidimensional, homogeneous array of fixed-size items. An associated data-type object describes the format of each element in the array (its byte-order, how many bytes it occupies in memory, whether it is an integer, a floating point number, or something else, etc.)</p>
<p>Arrays should be constructed using <code>array</code>, <code>zeros</code> or <code>empty</code> (refer to the See Also section below). The parameters given here refer to a low-level method (<code>ndarray(…)</code>) for instantiating an array.</p>
<p>For more information, refer to the <code>numpy</code> module and examine the methods and attributes of an array.</p>
<h2 id="parameters">Parameters</h2>
<p>(for the <strong>new</strong> method; see Notes below)</p>
<dl>
<dt><strong><code>shape</code></strong> : <code>tuple</code> of <code>ints</code></dt>
<dd>Shape of created array.
</dd>
<dt><strong><code>dtype</code></strong> : <code>data-type</code>, optional</dt>
<dd>Any object that can be interpreted as a numpy data type.
</dd>
<dt><strong><code>buffer</code></strong> : <code>object exposing buffer interface</code>, optional</dt>
<dd>Used to fill the array with data.
</dd>
<dt><strong><code>offset</code></strong> : <code>int</code>, optional</dt>
<dd>Offset of array data in buffer.
</dd>
<dt><strong><code>strides</code></strong> : <code>tuple</code> of <code>ints</code>, optional</dt>
<dd>Strides of data in memory.
</dd>
<dt><strong><code>order</code></strong> : <code>{'C', 'F'}</code>, optional</dt>
<dd>Row-major (C-style) or column-major (Fortran-style) order.
</dd>
</dl>
<h2 id="attributes">Attributes</h2>
<dl>
<dt><strong><code>T</code></strong> : <code>ndarray</code></dt>
<dd>Transpose of the array.
</dd>
<dt><strong><code>data</code></strong> : <code>buffer</code></dt>
<dd>The array’s elements, in memory.
</dd>
<dt><strong><code>dtype</code></strong> : <code>dtype object</code></dt>
<dd>Describes the format of the elements in the array.
</dd>
<dt><strong><code>flags</code></strong> : <code>dict</code></dt>
<dd>Dictionary containing information related to memory use, e.g., ‘C_CONTIGUOUS,’ ‘OWNDATA,’ ‘WRITEABLE,’ etc.
</dd>
<dt><strong><code>flat</code></strong> : <code>numpy.flatiter object</code></dt>
<dd>Flattened version of the array as an iterator. The iterator allows assignments, e.g., <code>x.flat = 3</code> (See <code>ndarray.flat</code> for assignment examples; TODO).
</dd>
<dt><strong><code>imag</code></strong> : <code>ndarray</code></dt>
<dd>Imaginary part of the array.
</dd>
<dt><strong><code>real</code></strong> : <code>ndarray</code></dt>
<dd>Real part of the array.
</dd>
<dt><strong><code>size</code></strong> : <code>int</code></dt>
<dd>Number of elements in the array.
</dd>
<dt><strong><code>itemsize</code></strong> : <code>int</code></dt>
<dd>The memory use of each array element in bytes.
</dd>
<dt><strong><code>nbytes</code></strong> : <code>int</code></dt>
<dd>The total number of bytes required to store the array data, i.e., <code>itemsize * size</code>.
</dd>
<dt><strong><code>ndim</code></strong> : <code>int</code></dt>
<dd>The array’s number of dimensions.
</dd>
<dt><strong><code>shape</code></strong> : <code>tuple</code> of <code>ints</code></dt>
<dd>Shape of the array.
</dd>
<dt><strong><code>strides</code></strong> : <code>tuple</code> of <code>ints</code></dt>
<dd>The step-size required to move from one element to the next in memory. For example, a contiguous <code>(3, 4)</code> array of type <code>int16</code> in C-order has strides <code>(8, 2)</code>. This implies that to move from element to element in memory requires jumps of 2 bytes. To move from row-to-row, one needs to jump 8 bytes at a time (<code>2 * 4</code>).
</dd>
<dt><strong><code>ctypes</code></strong> : <code>ctypes object</code></dt>
<dd>Class containing properties of the array needed for interaction with ctypes.
</dd>
<dt><strong><code>base</code></strong> : <code>ndarray</code></dt>
<dd>If the array is a view into another array, that array is its <code>base</code> (unless that array is also a view). The <code>base</code> array is where the array data is actually stored.
</dd>
</dl>
<h2 id="see-also">See Also</h2>
<dl>
<dt><code>array</code></dt>
<dd>Construct an array.
</dd>
<dt><code>zeros</code></dt>
<dd>Create an array, each element of which is zero.
</dd>
<dt><code>empty</code></dt>
<dd>Create an array, but leave its allocated memory unchanged (i.e., it contains “garbage”).
</dd>
<dt><code>dtype</code></dt>
<dd>Create a data-type.
</dd>
</dl>
<h2 id="notes">Notes</h2>
<p>There are two modes of creating an array using <code>__new__</code>:</p>
<ol type="1">
<li>If <code>buffer</code> is None, then only <code>shape</code>, <code>dtype</code>, and <code>order</code> are used.</li>
<li>If <code>buffer</code> is an object exposing the buffer interface, then all keywords are interpreted.</li>
</ol>
<p>No <code>__init__</code> method is needed because the array is fully initialized after the <code>__new__</code> method.</p>
<h2 id="examples">Examples</h2>
<p>These examples illustrate the low-level <code>ndarray</code> constructor. Refer to the <code>See Also</code> section above for easier ways of constructing an ndarray.</p>
<p>First mode, <code>buffer</code> is None:</p>
<pre class="python-repl"><code>&gt;&gt;&gt; np.ndarray(shape=(2,2), dtype=float, order=&#39;F&#39;)
array([[0.0e+000, 0.0e+000], # random
       [     nan, 2.5e-323]])</code></pre>
<p>Second mode:</p>
<pre class="python-repl"><code>&gt;&gt;&gt; np.ndarray((2,), buffer=np.array([1,2,3]),
...            offset=np.int_().itemsize,
...            dtype=int) # offset = 1*itemsize, i.e. skip first element
array([2, 3])</code></pre>
</div>
<h3>Ancestors</h3>
<ul class="hlist">
<li><a title="anabel.matrices.Structural_Vector" href="#anabel.matrices.Structural_Vector">Structural_Vector</a></li>
<li>numpy.ndarray</li>
</ul>
<h3>Class variables</h3>
<dl>
<dt id="anabel.matrices.iForce_vector.tag"><code class="name">var <span class="ident">tag</span></code></dt>
<dd>
<div class="desc">
</div>
</dd>
</dl>
<h3>Instance variables</h3>
<dl>
<dt id="anabel.matrices.iForce_vector.c"><code class="name">var <span class="ident">c</span></code></dt>
<dd>
<div class="desc"><p>Remove rows corresponding to element hinges/releases</p>
</div>
</dd>
<dt id="anabel.matrices.iForce_vector.i"><code class="name">var <span class="ident">i</span></code></dt>
<dd>
<div class="desc"><p>Removes rows corresponding to redundant forces</p>
</div>
</dd>
<dt id="anabel.matrices.iForce_vector.x"><code class="name">var <span class="ident">x</span></code></dt>
<dd>
<div class="desc"><p>Remove rows of corresponding to primary forces</p>
</div>
</dd>
</dl>
</dd>
<dt id="anabel.matrices.nDisplacement_vector"><code class="flex name class">
<span>class <span class="ident">nDisplacement_vector</span></span>
<span>(</span><span>arry, model, row_data, Vector=None)</span>
</code></dt>
<dd>
<div class="desc"><p>ndarray(shape, dtype=float, buffer=None, offset=0, strides=None, order=None)</p>
<p>An array object represents a multidimensional, homogeneous array of fixed-size items. An associated data-type object describes the format of each element in the array (its byte-order, how many bytes it occupies in memory, whether it is an integer, a floating point number, or something else, etc.)</p>
<p>Arrays should be constructed using <code>array</code>, <code>zeros</code> or <code>empty</code> (refer to the See Also section below). The parameters given here refer to a low-level method (<code>ndarray(…)</code>) for instantiating an array.</p>
<p>For more information, refer to the <code>numpy</code> module and examine the methods and attributes of an array.</p>
<h2 id="parameters">Parameters</h2>
<p>(for the <strong>new</strong> method; see Notes below)</p>
<dl>
<dt><strong><code>shape</code></strong> : <code>tuple</code> of <code>ints</code></dt>
<dd>Shape of created array.
</dd>
<dt><strong><code>dtype</code></strong> : <code>data-type</code>, optional</dt>
<dd>Any object that can be interpreted as a numpy data type.
</dd>
<dt><strong><code>buffer</code></strong> : <code>object exposing buffer interface</code>, optional</dt>
<dd>Used to fill the array with data.
</dd>
<dt><strong><code>offset</code></strong> : <code>int</code>, optional</dt>
<dd>Offset of array data in buffer.
</dd>
<dt><strong><code>strides</code></strong> : <code>tuple</code> of <code>ints</code>, optional</dt>
<dd>Strides of data in memory.
</dd>
<dt><strong><code>order</code></strong> : <code>{'C', 'F'}</code>, optional</dt>
<dd>Row-major (C-style) or column-major (Fortran-style) order.
</dd>
</dl>
<h2 id="attributes">Attributes</h2>
<dl>
<dt><strong><code>T</code></strong> : <code>ndarray</code></dt>
<dd>Transpose of the array.
</dd>
<dt><strong><code>data</code></strong> : <code>buffer</code></dt>
<dd>The array’s elements, in memory.
</dd>
<dt><strong><code>dtype</code></strong> : <code>dtype object</code></dt>
<dd>Describes the format of the elements in the array.
</dd>
<dt><strong><code>flags</code></strong> : <code>dict</code></dt>
<dd>Dictionary containing information related to memory use, e.g., ‘C_CONTIGUOUS,’ ‘OWNDATA,’ ‘WRITEABLE,’ etc.
</dd>
<dt><strong><code>flat</code></strong> : <code>numpy.flatiter object</code></dt>
<dd>Flattened version of the array as an iterator. The iterator allows assignments, e.g., <code>x.flat = 3</code> (See <code>ndarray.flat</code> for assignment examples; TODO).
</dd>
<dt><strong><code>imag</code></strong> : <code>ndarray</code></dt>
<dd>Imaginary part of the array.
</dd>
<dt><strong><code>real</code></strong> : <code>ndarray</code></dt>
<dd>Real part of the array.
</dd>
<dt><strong><code>size</code></strong> : <code>int</code></dt>
<dd>Number of elements in the array.
</dd>
<dt><strong><code>itemsize</code></strong> : <code>int</code></dt>
<dd>The memory use of each array element in bytes.
</dd>
<dt><strong><code>nbytes</code></strong> : <code>int</code></dt>
<dd>The total number of bytes required to store the array data, i.e., <code>itemsize * size</code>.
</dd>
<dt><strong><code>ndim</code></strong> : <code>int</code></dt>
<dd>The array’s number of dimensions.
</dd>
<dt><strong><code>shape</code></strong> : <code>tuple</code> of <code>ints</code></dt>
<dd>Shape of the array.
</dd>
<dt><strong><code>strides</code></strong> : <code>tuple</code> of <code>ints</code></dt>
<dd>The step-size required to move from one element to the next in memory. For example, a contiguous <code>(3, 4)</code> array of type <code>int16</code> in C-order has strides <code>(8, 2)</code>. This implies that to move from element to element in memory requires jumps of 2 bytes. To move from row-to-row, one needs to jump 8 bytes at a time (<code>2 * 4</code>).
</dd>
<dt><strong><code>ctypes</code></strong> : <code>ctypes object</code></dt>
<dd>Class containing properties of the array needed for interaction with ctypes.
</dd>
<dt><strong><code>base</code></strong> : <code>ndarray</code></dt>
<dd>If the array is a view into another array, that array is its <code>base</code> (unless that array is also a view). The <code>base</code> array is where the array data is actually stored.
</dd>
</dl>
<h2 id="see-also">See Also</h2>
<dl>
<dt><code>array</code></dt>
<dd>Construct an array.
</dd>
<dt><code>zeros</code></dt>
<dd>Create an array, each element of which is zero.
</dd>
<dt><code>empty</code></dt>
<dd>Create an array, but leave its allocated memory unchanged (i.e., it contains “garbage”).
</dd>
<dt><code>dtype</code></dt>
<dd>Create a data-type.
</dd>
</dl>
<h2 id="notes">Notes</h2>
<p>There are two modes of creating an array using <code>__new__</code>:</p>
<ol type="1">
<li>If <code>buffer</code> is None, then only <code>shape</code>, <code>dtype</code>, and <code>order</code> are used.</li>
<li>If <code>buffer</code> is an object exposing the buffer interface, then all keywords are interpreted.</li>
</ol>
<p>No <code>__init__</code> method is needed because the array is fully initialized after the <code>__new__</code> method.</p>
<h2 id="examples">Examples</h2>
<p>These examples illustrate the low-level <code>ndarray</code> constructor. Refer to the <code>See Also</code> section above for easier ways of constructing an ndarray.</p>
<p>First mode, <code>buffer</code> is None:</p>
<pre class="python-repl"><code>&gt;&gt;&gt; np.ndarray(shape=(2,2), dtype=float, order=&#39;F&#39;)
array([[0.0e+000, 0.0e+000], # random
       [     nan, 2.5e-323]])</code></pre>
<p>Second mode:</p>
<pre class="python-repl"><code>&gt;&gt;&gt; np.ndarray((2,), buffer=np.array([1,2,3]),
...            offset=np.int_().itemsize,
...            dtype=int) # offset = 1*itemsize, i.e. skip first element
array([2, 3])</code></pre>
</div>
<h3>Ancestors</h3>
<ul class="hlist">
<li><a title="anabel.matrices.Structural_Vector" href="#anabel.matrices.Structural_Vector">Structural_Vector</a></li>
<li>numpy.ndarray</li>
</ul>
<h3>Class variables</h3>
<dl>
<dt id="anabel.matrices.nDisplacement_vector.tag"><code class="name">var <span class="ident">tag</span></code></dt>
<dd>
<div class="desc">
</div>
</dd>
</dl>
<h3>Instance variables</h3>
<dl>
<dt id="anabel.matrices.nDisplacement_vector.f"><code class="name">var <span class="ident">f</span></code></dt>
<dd>
<div class="desc"><p>Removes rows corresponding to fixed dofs</p>
</div>
</dd>
</dl>
</dd>
<dt id="anabel.matrices.nForce_vector"><code class="flex name class">
<span>class <span class="ident">nForce_vector</span></span>
<span>(</span><span>arry, model, row_data, Vector=None)</span>
</code></dt>
<dd>
<div class="desc"><p>ndarray(shape, dtype=float, buffer=None, offset=0, strides=None, order=None)</p>
<p>An array object represents a multidimensional, homogeneous array of fixed-size items. An associated data-type object describes the format of each element in the array (its byte-order, how many bytes it occupies in memory, whether it is an integer, a floating point number, or something else, etc.)</p>
<p>Arrays should be constructed using <code>array</code>, <code>zeros</code> or <code>empty</code> (refer to the See Also section below). The parameters given here refer to a low-level method (<code>ndarray(…)</code>) for instantiating an array.</p>
<p>For more information, refer to the <code>numpy</code> module and examine the methods and attributes of an array.</p>
<h2 id="parameters">Parameters</h2>
<p>(for the <strong>new</strong> method; see Notes below)</p>
<dl>
<dt><strong><code>shape</code></strong> : <code>tuple</code> of <code>ints</code></dt>
<dd>Shape of created array.
</dd>
<dt><strong><code>dtype</code></strong> : <code>data-type</code>, optional</dt>
<dd>Any object that can be interpreted as a numpy data type.
</dd>
<dt><strong><code>buffer</code></strong> : <code>object exposing buffer interface</code>, optional</dt>
<dd>Used to fill the array with data.
</dd>
<dt><strong><code>offset</code></strong> : <code>int</code>, optional</dt>
<dd>Offset of array data in buffer.
</dd>
<dt><strong><code>strides</code></strong> : <code>tuple</code> of <code>ints</code>, optional</dt>
<dd>Strides of data in memory.
</dd>
<dt><strong><code>order</code></strong> : <code>{'C', 'F'}</code>, optional</dt>
<dd>Row-major (C-style) or column-major (Fortran-style) order.
</dd>
</dl>
<h2 id="attributes">Attributes</h2>
<dl>
<dt><strong><code>T</code></strong> : <code>ndarray</code></dt>
<dd>Transpose of the array.
</dd>
<dt><strong><code>data</code></strong> : <code>buffer</code></dt>
<dd>The array’s elements, in memory.
</dd>
<dt><strong><code>dtype</code></strong> : <code>dtype object</code></dt>
<dd>Describes the format of the elements in the array.
</dd>
<dt><strong><code>flags</code></strong> : <code>dict</code></dt>
<dd>Dictionary containing information related to memory use, e.g., ‘C_CONTIGUOUS,’ ‘OWNDATA,’ ‘WRITEABLE,’ etc.
</dd>
<dt><strong><code>flat</code></strong> : <code>numpy.flatiter object</code></dt>
<dd>Flattened version of the array as an iterator. The iterator allows assignments, e.g., <code>x.flat = 3</code> (See <code>ndarray.flat</code> for assignment examples; TODO).
</dd>
<dt><strong><code>imag</code></strong> : <code>ndarray</code></dt>
<dd>Imaginary part of the array.
</dd>
<dt><strong><code>real</code></strong> : <code>ndarray</code></dt>
<dd>Real part of the array.
</dd>
<dt><strong><code>size</code></strong> : <code>int</code></dt>
<dd>Number of elements in the array.
</dd>
<dt><strong><code>itemsize</code></strong> : <code>int</code></dt>
<dd>The memory use of each array element in bytes.
</dd>
<dt><strong><code>nbytes</code></strong> : <code>int</code></dt>
<dd>The total number of bytes required to store the array data, i.e., <code>itemsize * size</code>.
</dd>
<dt><strong><code>ndim</code></strong> : <code>int</code></dt>
<dd>The array’s number of dimensions.
</dd>
<dt><strong><code>shape</code></strong> : <code>tuple</code> of <code>ints</code></dt>
<dd>Shape of the array.
</dd>
<dt><strong><code>strides</code></strong> : <code>tuple</code> of <code>ints</code></dt>
<dd>The step-size required to move from one element to the next in memory. For example, a contiguous <code>(3, 4)</code> array of type <code>int16</code> in C-order has strides <code>(8, 2)</code>. This implies that to move from element to element in memory requires jumps of 2 bytes. To move from row-to-row, one needs to jump 8 bytes at a time (<code>2 * 4</code>).
</dd>
<dt><strong><code>ctypes</code></strong> : <code>ctypes object</code></dt>
<dd>Class containing properties of the array needed for interaction with ctypes.
</dd>
<dt><strong><code>base</code></strong> : <code>ndarray</code></dt>
<dd>If the array is a view into another array, that array is its <code>base</code> (unless that array is also a view). The <code>base</code> array is where the array data is actually stored.
</dd>
</dl>
<h2 id="see-also">See Also</h2>
<dl>
<dt><code>array</code></dt>
<dd>Construct an array.
</dd>
<dt><code>zeros</code></dt>
<dd>Create an array, each element of which is zero.
</dd>
<dt><code>empty</code></dt>
<dd>Create an array, but leave its allocated memory unchanged (i.e., it contains “garbage”).
</dd>
<dt><code>dtype</code></dt>
<dd>Create a data-type.
</dd>
</dl>
<h2 id="notes">Notes</h2>
<p>There are two modes of creating an array using <code>__new__</code>:</p>
<ol type="1">
<li>If <code>buffer</code> is None, then only <code>shape</code>, <code>dtype</code>, and <code>order</code> are used.</li>
<li>If <code>buffer</code> is an object exposing the buffer interface, then all keywords are interpreted.</li>
</ol>
<p>No <code>__init__</code> method is needed because the array is fully initialized after the <code>__new__</code> method.</p>
<h2 id="examples">Examples</h2>
<p>These examples illustrate the low-level <code>ndarray</code> constructor. Refer to the <code>See Also</code> section above for easier ways of constructing an ndarray.</p>
<p>First mode, <code>buffer</code> is None:</p>
<pre class="python-repl"><code>&gt;&gt;&gt; np.ndarray(shape=(2,2), dtype=float, order=&#39;F&#39;)
array([[0.0e+000, 0.0e+000], # random
       [     nan, 2.5e-323]])</code></pre>
<p>Second mode:</p>
<pre class="python-repl"><code>&gt;&gt;&gt; np.ndarray((2,), buffer=np.array([1,2,3]),
...            offset=np.int_().itemsize,
...            dtype=int) # offset = 1*itemsize, i.e. skip first element
array([2, 3])</code></pre>
</div>
<h3>Ancestors</h3>
<ul class="hlist">
<li><a title="anabel.matrices.Structural_Vector" href="#anabel.matrices.Structural_Vector">Structural_Vector</a></li>
<li>numpy.ndarray</li>
</ul>
<h3>Class variables</h3>
<dl>
<dt id="anabel.matrices.nForce_vector.tag"><code class="name">var <span class="ident">tag</span></code></dt>
<dd>
<div class="desc">
</div>
</dd>
</dl>
<h3>Instance variables</h3>
<dl>
<dt id="anabel.matrices.nForce_vector.d"><code class="name">var <span class="ident">d</span></code></dt>
<dd>
<div class="desc"><p>Removes rows corresponding to free dofs</p>
</div>
</dd>
<dt id="anabel.matrices.nForce_vector.f"><code class="name">var <span class="ident">f</span></code></dt>
<dd>
<div class="desc">
</div>
</dd>
</dl>
</dd>
<dt id="anabel.matrices.nKinematic_matrix"><code class="flex name class">
<span>class <span class="ident">nKinematic_matrix</span></span>
<span>(</span><span>arry, model, rcdata)</span>
</code></dt>
<dd>
<div class="desc"><p>Class for the kinematic matrix of a structural model with 2d/3d truss and 2d frame elements the function forms the kinematic matrix A for all degrees of freedom and all element deformations of the structural model specified in data structure MODEL the function is currently limited to 2d/3d truss and 2d frame elements</p>
<h2 id="returns">Returns</h2>
<dl>
<dt><code>Kinematic matrix</code></dt>
<dd>
</dd>
</dl>
</div>
<h3>Ancestors</h3>
<ul class="hlist">
<li><a title="anabel.matrices.Structural_Matrix" href="#anabel.matrices.Structural_Matrix">Structural_Matrix</a></li>
<li>numpy.ndarray</li>
</ul>
<h3>Class variables</h3>
<dl>
<dt id="anabel.matrices.nKinematic_matrix.ranges"><code class="name">var <span class="ident">ranges</span></code></dt>
<dd>
<div class="desc">
</div>
</dd>
</dl>
<h3>Instance variables</h3>
<dl>
<dt id="anabel.matrices.nKinematic_matrix.c"><code class="name">var <span class="ident">c</span></code></dt>
<dd>
<div class="desc"><p>Removes rows corresponding to element hinges/releases</p>
</div>
</dd>
<dt id="anabel.matrices.nKinematic_matrix.c0"><code class="name">var <span class="ident">c0</span></code></dt>
<dd>
<div class="desc">
</div>
</dd>
<dt id="anabel.matrices.nKinematic_matrix.d"><code class="name">var <span class="ident">d</span></code></dt>
<dd>
<div class="desc"><p>Removes columns corresponding to free dofs</p>
</div>
</dd>
<dt id="anabel.matrices.nKinematic_matrix.e"><code class="name">var <span class="ident">e</span></code></dt>
<dd>
<div class="desc">
</div>
</dd>
<dt id="anabel.matrices.nKinematic_matrix.f"><code class="name">var <span class="ident">f</span></code></dt>
<dd>
<div class="desc"><p>Removes columns corresponding to fixed dofs</p>
</div>
</dd>
<dt id="anabel.matrices.nKinematic_matrix.i"><code class="name">var <span class="ident">i</span></code></dt>
<dd>
<div class="desc"><p>Removes rows corresponding to redundant forces</p>
</div>
</dd>
<dt id="anabel.matrices.nKinematic_matrix.o"><code class="name">var <span class="ident">o</span></code></dt>
<dd>
<div class="desc">
</div>
</dd>
</dl>
<h3>Methods</h3>
<dl>
<dt id="anabel.matrices.nKinematic_matrix.combine"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">combine</span></span>(<span>self, component)</span>
</code></dt>
<dd>
<div class="desc">
</div>
</dd>
</dl>
<h3>Inherited members</h3>
<ul class="hlist">
<li><code><b><a title="anabel.matrices.Structural_Matrix" href="#anabel.matrices.Structural_Matrix">Structural_Matrix</a></b></code>:
<ul class="hlist">
<li><code><a title="anabel.matrices.Structural_Matrix.del_zeros" href="#anabel.matrices.Structural_Matrix.del_zeros">del_zeros</a></code></li>
<li><code><a title="anabel.matrices.Structural_Matrix.ker" href="#anabel.matrices.Structural_Matrix.ker">ker</a></code></li>
<li><code><a title="anabel.matrices.Structural_Matrix.lns" href="#anabel.matrices.Structural_Matrix.lns">lns</a></code></li>
<li><code><a title="anabel.matrices.Structural_Matrix.nls" href="#anabel.matrices.Structural_Matrix.nls">nls</a></code></li>
<li><code><a title="anabel.matrices.Structural_Matrix.rank" href="#anabel.matrices.Structural_Matrix.rank">rank</a></code></li>
<li><code><a title="anabel.matrices.Structural_Matrix.remove" href="#anabel.matrices.Structural_Matrix.remove">remove</a></code></li>
<li><code><a title="anabel.matrices.Structural_Matrix.round" href="#anabel.matrices.Structural_Matrix.round">round</a></code></li>
</ul>
</li>
</ul>
</dd>
<dt id="anabel.matrices.nStatic_matrix"><code class="flex name class">
<span>class <span class="ident">nStatic_matrix</span></span>
<span>(</span><span>arry, model, rcdata)</span>
</code></dt>
<dd>
<div class="desc"><p>ndarray(shape, dtype=float, buffer=None, offset=0, strides=None, order=None)</p>
<p>An array object represents a multidimensional, homogeneous array of fixed-size items. An associated data-type object describes the format of each element in the array (its byte-order, how many bytes it occupies in memory, whether it is an integer, a floating point number, or something else, etc.)</p>
<p>Arrays should be constructed using <code>array</code>, <code>zeros</code> or <code>empty</code> (refer to the See Also section below). The parameters given here refer to a low-level method (<code>ndarray(…)</code>) for instantiating an array.</p>
<p>For more information, refer to the <code>numpy</code> module and examine the methods and attributes of an array.</p>
<h2 id="parameters">Parameters</h2>
<p>(for the <strong>new</strong> method; see Notes below)</p>
<dl>
<dt><strong><code>shape</code></strong> : <code>tuple</code> of <code>ints</code></dt>
<dd>Shape of created array.
</dd>
<dt><strong><code>dtype</code></strong> : <code>data-type</code>, optional</dt>
<dd>Any object that can be interpreted as a numpy data type.
</dd>
<dt><strong><code>buffer</code></strong> : <code>object exposing buffer interface</code>, optional</dt>
<dd>Used to fill the array with data.
</dd>
<dt><strong><code>offset</code></strong> : <code>int</code>, optional</dt>
<dd>Offset of array data in buffer.
</dd>
<dt><strong><code>strides</code></strong> : <code>tuple</code> of <code>ints</code>, optional</dt>
<dd>Strides of data in memory.
</dd>
<dt><strong><code>order</code></strong> : <code>{'C', 'F'}</code>, optional</dt>
<dd>Row-major (C-style) or column-major (Fortran-style) order.
</dd>
</dl>
<h2 id="attributes">Attributes</h2>
<dl>
<dt><strong><code>T</code></strong> : <code>ndarray</code></dt>
<dd>Transpose of the array.
</dd>
<dt><strong><code>data</code></strong> : <code>buffer</code></dt>
<dd>The array’s elements, in memory.
</dd>
<dt><strong><code>dtype</code></strong> : <code>dtype object</code></dt>
<dd>Describes the format of the elements in the array.
</dd>
<dt><strong><code>flags</code></strong> : <code>dict</code></dt>
<dd>Dictionary containing information related to memory use, e.g., ‘C_CONTIGUOUS,’ ‘OWNDATA,’ ‘WRITEABLE,’ etc.
</dd>
<dt><strong><code>flat</code></strong> : <code>numpy.flatiter object</code></dt>
<dd>Flattened version of the array as an iterator. The iterator allows assignments, e.g., <code>x.flat = 3</code> (See <code>ndarray.flat</code> for assignment examples; TODO).
</dd>
<dt><strong><code>imag</code></strong> : <code>ndarray</code></dt>
<dd>Imaginary part of the array.
</dd>
<dt><strong><code>real</code></strong> : <code>ndarray</code></dt>
<dd>Real part of the array.
</dd>
<dt><strong><code>size</code></strong> : <code>int</code></dt>
<dd>Number of elements in the array.
</dd>
<dt><strong><code>itemsize</code></strong> : <code>int</code></dt>
<dd>The memory use of each array element in bytes.
</dd>
<dt><strong><code>nbytes</code></strong> : <code>int</code></dt>
<dd>The total number of bytes required to store the array data, i.e., <code>itemsize * size</code>.
</dd>
<dt><strong><code>ndim</code></strong> : <code>int</code></dt>
<dd>The array’s number of dimensions.
</dd>
<dt><strong><code>shape</code></strong> : <code>tuple</code> of <code>ints</code></dt>
<dd>Shape of the array.
</dd>
<dt><strong><code>strides</code></strong> : <code>tuple</code> of <code>ints</code></dt>
<dd>The step-size required to move from one element to the next in memory. For example, a contiguous <code>(3, 4)</code> array of type <code>int16</code> in C-order has strides <code>(8, 2)</code>. This implies that to move from element to element in memory requires jumps of 2 bytes. To move from row-to-row, one needs to jump 8 bytes at a time (<code>2 * 4</code>).
</dd>
<dt><strong><code>ctypes</code></strong> : <code>ctypes object</code></dt>
<dd>Class containing properties of the array needed for interaction with ctypes.
</dd>
<dt><strong><code>base</code></strong> : <code>ndarray</code></dt>
<dd>If the array is a view into another array, that array is its <code>base</code> (unless that array is also a view). The <code>base</code> array is where the array data is actually stored.
</dd>
</dl>
<h2 id="see-also">See Also</h2>
<dl>
<dt><code>array</code></dt>
<dd>Construct an array.
</dd>
<dt><code>zeros</code></dt>
<dd>Create an array, each element of which is zero.
</dd>
<dt><code>empty</code></dt>
<dd>Create an array, but leave its allocated memory unchanged (i.e., it contains “garbage”).
</dd>
<dt><code>dtype</code></dt>
<dd>Create a data-type.
</dd>
</dl>
<h2 id="notes">Notes</h2>
<p>There are two modes of creating an array using <code>__new__</code>:</p>
<ol type="1">
<li>If <code>buffer</code> is None, then only <code>shape</code>, <code>dtype</code>, and <code>order</code> are used.</li>
<li>If <code>buffer</code> is an object exposing the buffer interface, then all keywords are interpreted.</li>
</ol>
<p>No <code>__init__</code> method is needed because the array is fully initialized after the <code>__new__</code> method.</p>
<h2 id="examples">Examples</h2>
<p>These examples illustrate the low-level <code>ndarray</code> constructor. Refer to the <code>See Also</code> section above for easier ways of constructing an ndarray.</p>
<p>First mode, <code>buffer</code> is None:</p>
<pre class="python-repl"><code>&gt;&gt;&gt; np.ndarray(shape=(2,2), dtype=float, order=&#39;F&#39;)
array([[0.0e+000, 0.0e+000], # random
       [     nan, 2.5e-323]])</code></pre>
<p>Second mode:</p>
<pre class="python-repl"><code>&gt;&gt;&gt; np.ndarray((2,), buffer=np.array([1,2,3]),
...            offset=np.int_().itemsize,
...            dtype=int) # offset = 1*itemsize, i.e. skip first element
array([2, 3])</code></pre>
</div>
<h3>Ancestors</h3>
<ul class="hlist">
<li><a title="anabel.matrices.Structural_Matrix" href="#anabel.matrices.Structural_Matrix">Structural_Matrix</a></li>
<li>numpy.ndarray</li>
</ul>
<h3>Class variables</h3>
<dl>
<dt id="anabel.matrices.nStatic_matrix.ranges"><code class="name">var <span class="ident">ranges</span></code></dt>
<dd>
<div class="desc">
</div>
</dd>
</dl>
<h3>Instance variables</h3>
<dl>
<dt id="anabel.matrices.nStatic_matrix.bari"><code class="name">var <span class="ident">bari</span></code></dt>
<dd>
<div class="desc">
</div>
</dd>
<dt id="anabel.matrices.nStatic_matrix.barx"><code class="name">var <span class="ident">barx</span></code></dt>
<dd>
<div class="desc">
</div>
</dd>
<dt id="anabel.matrices.nStatic_matrix.barxi"><code class="name">var <span class="ident">barxi</span></code></dt>
<dd>
<div class="desc">
</div>
</dd>
<dt id="anabel.matrices.nStatic_matrix.c"><code class="name">var <span class="ident">c</span></code></dt>
<dd>
<div class="desc"><p>Removes columns corresponding to element hinges/releases</p>
</div>
</dd>
<dt id="anabel.matrices.nStatic_matrix.c0"><code class="name">var <span class="ident">c0</span></code></dt>
<dd>
<div class="desc">
</div>
</dd>
<dt id="anabel.matrices.nStatic_matrix.d"><code class="name">var <span class="ident">d</span></code></dt>
<dd>
<div class="desc"><p>Removes rows corresponding to free dofs</p>
</div>
</dd>
<dt id="anabel.matrices.nStatic_matrix.f"><code class="name">var <span class="ident">f</span></code></dt>
<dd>
<div class="desc">
</div>
</dd>
<dt id="anabel.matrices.nStatic_matrix.fc"><code class="name">var <span class="ident">fc</span></code></dt>
<dd>
<div class="desc">
</div>
</dd>
<dt id="anabel.matrices.nStatic_matrix.i"><code class="name">var <span class="ident">i</span></code></dt>
<dd>
<div class="desc"><p>Removes rows of B_matrix corresponding to redundant forces</p>
</div>
</dd>
<dt id="anabel.matrices.nStatic_matrix.o"><code class="name">var <span class="ident">o</span></code></dt>
<dd>
<div class="desc"><p>Remove columns corresponding to element force releases, then delete zeros</p>
</div>
</dd>
<dt id="anabel.matrices.nStatic_matrix.x"><code class="name">var <span class="ident">x</span></code></dt>
<dd>
<div class="desc"><p>Removes rows of B_matrix corresponding to primary (non-redundant) forces</p>
</div>
</dd>
</dl>
<h3>Inherited members</h3>
<ul class="hlist">
<li><code><b><a title="anabel.matrices.Structural_Matrix" href="#anabel.matrices.Structural_Matrix">Structural_Matrix</a></b></code>:
<ul class="hlist">
<li><code><a title="anabel.matrices.Structural_Matrix.del_zeros" href="#anabel.matrices.Structural_Matrix.del_zeros">del_zeros</a></code></li>
<li><code><a title="anabel.matrices.Structural_Matrix.ker" href="#anabel.matrices.Structural_Matrix.ker">ker</a></code></li>
<li><code><a title="anabel.matrices.Structural_Matrix.lns" href="#anabel.matrices.Structural_Matrix.lns">lns</a></code></li>
<li><code><a title="anabel.matrices.Structural_Matrix.nls" href="#anabel.matrices.Structural_Matrix.nls">nls</a></code></li>
<li><code><a title="anabel.matrices.Structural_Matrix.rank" href="#anabel.matrices.Structural_Matrix.rank">rank</a></code></li>
<li><code><a title="anabel.matrices.Structural_Matrix.remove" href="#anabel.matrices.Structural_Matrix.remove">remove</a></code></li>
<li><code><a title="anabel.matrices.Structural_Matrix.round" href="#anabel.matrices.Structural_Matrix.round">round</a></code></li>
</ul>
</li>
</ul>
</dd>
<dt id="anabel.matrices.row_vector"><code class="flex name class">
<span>class <span class="ident">row_vector</span></span>
<span>(</span><span>Matrix)</span>
</code></dt>
<dd>
<div class="desc"><p>ndarray(shape, dtype=float, buffer=None, offset=0, strides=None, order=None)</p>
<p>An array object represents a multidimensional, homogeneous array of fixed-size items. An associated data-type object describes the format of each element in the array (its byte-order, how many bytes it occupies in memory, whether it is an integer, a floating point number, or something else, etc.)</p>
<p>Arrays should be constructed using <code>array</code>, <code>zeros</code> or <code>empty</code> (refer to the See Also section below). The parameters given here refer to a low-level method (<code>ndarray(…)</code>) for instantiating an array.</p>
<p>For more information, refer to the <code>numpy</code> module and examine the methods and attributes of an array.</p>
<h2 id="parameters">Parameters</h2>
<p>(for the <strong>new</strong> method; see Notes below)</p>
<dl>
<dt><strong><code>shape</code></strong> : <code>tuple</code> of <code>ints</code></dt>
<dd>Shape of created array.
</dd>
<dt><strong><code>dtype</code></strong> : <code>data-type</code>, optional</dt>
<dd>Any object that can be interpreted as a numpy data type.
</dd>
<dt><strong><code>buffer</code></strong> : <code>object exposing buffer interface</code>, optional</dt>
<dd>Used to fill the array with data.
</dd>
<dt><strong><code>offset</code></strong> : <code>int</code>, optional</dt>
<dd>Offset of array data in buffer.
</dd>
<dt><strong><code>strides</code></strong> : <code>tuple</code> of <code>ints</code>, optional</dt>
<dd>Strides of data in memory.
</dd>
<dt><strong><code>order</code></strong> : <code>{'C', 'F'}</code>, optional</dt>
<dd>Row-major (C-style) or column-major (Fortran-style) order.
</dd>
</dl>
<h2 id="attributes">Attributes</h2>
<dl>
<dt><strong><code>T</code></strong> : <code>ndarray</code></dt>
<dd>Transpose of the array.
</dd>
<dt><strong><code>data</code></strong> : <code>buffer</code></dt>
<dd>The array’s elements, in memory.
</dd>
<dt><strong><code>dtype</code></strong> : <code>dtype object</code></dt>
<dd>Describes the format of the elements in the array.
</dd>
<dt><strong><code>flags</code></strong> : <code>dict</code></dt>
<dd>Dictionary containing information related to memory use, e.g., ‘C_CONTIGUOUS,’ ‘OWNDATA,’ ‘WRITEABLE,’ etc.
</dd>
<dt><strong><code>flat</code></strong> : <code>numpy.flatiter object</code></dt>
<dd>Flattened version of the array as an iterator. The iterator allows assignments, e.g., <code>x.flat = 3</code> (See <code>ndarray.flat</code> for assignment examples; TODO).
</dd>
<dt><strong><code>imag</code></strong> : <code>ndarray</code></dt>
<dd>Imaginary part of the array.
</dd>
<dt><strong><code>real</code></strong> : <code>ndarray</code></dt>
<dd>Real part of the array.
</dd>
<dt><strong><code>size</code></strong> : <code>int</code></dt>
<dd>Number of elements in the array.
</dd>
<dt><strong><code>itemsize</code></strong> : <code>int</code></dt>
<dd>The memory use of each array element in bytes.
</dd>
<dt><strong><code>nbytes</code></strong> : <code>int</code></dt>
<dd>The total number of bytes required to store the array data, i.e., <code>itemsize * size</code>.
</dd>
<dt><strong><code>ndim</code></strong> : <code>int</code></dt>
<dd>The array’s number of dimensions.
</dd>
<dt><strong><code>shape</code></strong> : <code>tuple</code> of <code>ints</code></dt>
<dd>Shape of the array.
</dd>
<dt><strong><code>strides</code></strong> : <code>tuple</code> of <code>ints</code></dt>
<dd>The step-size required to move from one element to the next in memory. For example, a contiguous <code>(3, 4)</code> array of type <code>int16</code> in C-order has strides <code>(8, 2)</code>. This implies that to move from element to element in memory requires jumps of 2 bytes. To move from row-to-row, one needs to jump 8 bytes at a time (<code>2 * 4</code>).
</dd>
<dt><strong><code>ctypes</code></strong> : <code>ctypes object</code></dt>
<dd>Class containing properties of the array needed for interaction with ctypes.
</dd>
<dt><strong><code>base</code></strong> : <code>ndarray</code></dt>
<dd>If the array is a view into another array, that array is its <code>base</code> (unless that array is also a view). The <code>base</code> array is where the array data is actually stored.
</dd>
</dl>
<h2 id="see-also">See Also</h2>
<dl>
<dt><code>array</code></dt>
<dd>Construct an array.
</dd>
<dt><code>zeros</code></dt>
<dd>Create an array, each element of which is zero.
</dd>
<dt><code>empty</code></dt>
<dd>Create an array, but leave its allocated memory unchanged (i.e., it contains “garbage”).
</dd>
<dt><code>dtype</code></dt>
<dd>Create a data-type.
</dd>
</dl>
<h2 id="notes">Notes</h2>
<p>There are two modes of creating an array using <code>__new__</code>:</p>
<ol type="1">
<li>If <code>buffer</code> is None, then only <code>shape</code>, <code>dtype</code>, and <code>order</code> are used.</li>
<li>If <code>buffer</code> is an object exposing the buffer interface, then all keywords are interpreted.</li>
</ol>
<p>No <code>__init__</code> method is needed because the array is fully initialized after the <code>__new__</code> method.</p>
<h2 id="examples">Examples</h2>
<p>These examples illustrate the low-level <code>ndarray</code> constructor. Refer to the <code>See Also</code> section above for easier ways of constructing an ndarray.</p>
<p>First mode, <code>buffer</code> is None:</p>
<pre class="python-repl"><code>&gt;&gt;&gt; np.ndarray(shape=(2,2), dtype=float, order=&#39;F&#39;)
array([[0.0e+000, 0.0e+000], # random
       [     nan, 2.5e-323]])</code></pre>
<p>Second mode:</p>
<pre class="python-repl"><code>&gt;&gt;&gt; np.ndarray((2,), buffer=np.array([1,2,3]),
...            offset=np.int_().itemsize,
...            dtype=int) # offset = 1*itemsize, i.e. skip first element
array([2, 3])</code></pre>
</div>
<h3>Ancestors</h3>
<ul class="hlist">
<li><a title="anabel.matrices.Structural_Vector" href="#anabel.matrices.Structural_Vector">Structural_Vector</a></li>
<li>numpy.ndarray</li>
</ul>
</dd>
</dl>
</section>
</main>