```{=html}
<!--
Download `hw7.zip`. It will create a directory called \emph{hw7} with 5
quadrutre scheme files and 3 matlab routines (\emph{get\_mesh.m},
  \emph{plot\_errors.m} and \emph{plot\_soln.m}).  There is also a
directory called \emph{circles\_iso} that contains 5 mesh files for
isoparametric elements, and another 5 with the same nodes but
connected together as linear triangular elements. The latter are for
plotting your solution.  (See the \emph{plot\_soln.m} file for an
 example of how to use the \emph{mesh?lin} files.)  There is a
\emph{notes} file in \emph{circles\_iso} that explains the data layout
of each mesh file.
-->
```
# Problem 1.

> (12 points) Solve the Dirichlet problem
>
> $$
>  \begin{aligned}
>    -\Delta u &= 4, & \quad &\text{in $\Omega$} \\
>            u &= 0, & &\text{on $\partial\Omega$}
>  \end{aligned}
> $$
>
> on the unit disk $\Omega=\{(x,y)\;:\; x^2+y^2\le 1\}$ using quadratic
> isoparametric elements.

A function implementing quadratic Lagrange interpolation over a
reference triangle is implemented in the file `interpolate.py` which is
used by the function `poisson2` from `poisson.py` to create a finite
element that locally evaluates the following variational Poisson problem

$$
\sum_{j=1}^{n} \mathbf{u}_{j} \int_{\Omega} \nabla \phi_{j} \cdot \nabla \phi_{i}=\int_{\Omega} \phi_{i} f+\int_{\partial \Omega_{N}} \phi_{i} g_{N}-\sum_{j=n+1}^{n+n_{\partial}} \mathbf{u}_{j} \int_{\Omega} \nabla \phi_{j} \cdot \nabla \phi_{i}
$$

This is then integrated over the domain using a self-implemented system
optimization package called `anabel` which leverages the JAX library to
vectorize element state determination in a manner that can be
accelerated on specialized hardware.

```{=html}
<!--
Element stiffness matrix:

$$
\begin{aligned}
a_{i j}^{(k)}=& \int_{\Delta *}\left(b_{2} \frac{\partial \psi_{*, i}}{\partial \xi}+b_{3} \frac{\partial \psi_{*, i}}{\partial \eta}\right)\left(b_{2} \frac{\partial \psi_{*, j}}{\partial \xi}+b_{3} \frac{\partial \psi_{*, j}}{\partial \eta}\right) \frac{1}{\left|J_{k}\right|} \mathrm{d} \xi \mathrm{d} \eta \\
&+\int_{\triangle *}\left(c_{2} \frac{\partial \psi_{*, i}}{\partial \xi}+c_{3} \frac{\partial \psi_{*, i}}{\partial \eta}\right)\left(c_{2} \frac{\partial \psi_{*, j}}{\partial \xi}+c_{3} \frac{\partial \psi_{*, j}}{\partial \eta}\right) \frac{1}{\left|J_{k}\right|} \mathrm{d} \xi \mathrm{d} \eta
\end{aligned}
$$

$$
\begin{aligned}
a_{i j}^{(k)} &=\int_{\Delta_{k}} \frac{\partial \psi_{k, i}}{\partial x} \frac{\partial \psi_{k, j}}{\partial x}+\frac{\partial \psi_{k, i}}{\partial y} \frac{\partial \psi_{k, j}}{\partial y} \mathrm{~d} x \mathrm{~d} y \quad i, j=1, \ldots, n_{k} \\
&=\int_{\Delta *}\left\{\frac{\partial \psi_{*, i}}{\partial x} \frac{\partial \psi_{*, j}}{\partial x}+\frac{\partial \psi_{*, i}}{\partial y} \frac{\partial \psi_{*, j}}{\partial y}\right\}\left|J_{k}\right| \mathrm{d} \xi \mathrm{d} \eta
\end{aligned}
$$
-->
```
![Finite element solution using order-2 Gaussian
quadrature](../img/mesh5-gauss02.png){width="50%"
style="margin:auto; display: block; max-width: 75%"}

> What is the exact solution?

The exact solution is

$$
\boxed{u = 1 - x^2 - y^2}
$$

![Closed-form solution to the stated Poisson
problem.](../img/analytic-a.png){width="50%"
style="margin:auto; display: block; max-width: 75%"}

> Compute the $H^1$ seminorm and $L^2$ norm of the error for each of the
> meshes. Ignore the fringe error due to the piecewise parabolic mesh
> boundary not quite aligning with the circular domain.

![](../img/mesh5-gauss02-H1.png){width="50%"
style="margin:auto; display: block; max-width: 75%"}
![](../img/mesh5-gauss02-L2.png){width="50%"
style="margin:auto; display: block; max-width: 75%"}



> Turn in a table of your errors and $\log$-$\log$ plots of the error
> vs.\~the mesh parameter, $h$.

![](../img/conv-3.png){style="margin:auto; display: block; max-width: 75%"}

Table of errors in the L2 norm for problem 1

  $h$       2               5               13              19
  --------- --------------- --------------- --------------- ---------------
  0.5       0.0024764578    0.0030141854    0.0029849953    0.0029849953
  0.25      0.0002258162    0.00027375659   0.00027090969   0.00027090969
  0.125     2.1527457e-05   2.5708536e-05   2.5448945e-05   2.5448945e-05
  0.0625    1.9830323e-06   2.3460163e-06   2.3228069e-06   2.3228069e-06
  0.03125   1.7587735e-07   2.0760524e-07   2.0555351e-07   2.0555351e-07

Table of errors in the L2 norm for problem 2

  $h$       2               5               13              19
  --------- --------------- --------------- --------------- ---------------
  0.5       0.0099611923    0.0064076596    0.0071412137    0.0071412137
  0.25      0.0013051996    0.00083984741   0.0009471105    0.0009471105
  0.125     0.00016874334   0.00010830203   0.00012249798   0.00012249798
  0.0625    2.1626624e-05   1.3882073e-05   1.5691434e-05   1.5691434e-05
  0.03125   2.7380054e-06   1.756023e-06    1.9850051e-06   1.9850051e-06

Table of errors in the H1 norm for problem 1

  $h$       2               5               13              19
  --------- --------------- --------------- --------------- ---------------
  0.5       0.033040555     0.05344312      0.053451002     0.053451002
  0.25      0.0057268302    0.0091748492    0.0091751946    0.0091751946
  0.125     0.0010299012    0.0016399388    0.0016399544    0.0016399544
  0.0625    0.00018443725   0.00029237375   0.00029237444   0.00029237444
  0.03125   3.254096e-05    5.152993e-05    5.1529961e-05   5.1529961e-05

Table of errors in the H1 norm for problem 2

  $h$       2               5               13              19
  --------- --------------- --------------- --------------- ---------------
  0.5       0.050321736     0.087419539     0.087364004     0.087364004
  0.25      0.013576873     0.024424342     0.024421502     0.024421502
  0.125     0.0036081315    0.0065157661    0.006515551     0.006515551
  0.0625    0.00093741811   0.0016853971    0.0016853811    0.0016853811
  0.03125   0.00023986093   0.00042915864   0.00042915753   0.00042915753

```{=html}
<!--
Find $u$ such that

$$
\begin{array}{c}
-\nabla^{2} u=f \quad \text { in } \Omega \\
u=g_{D} \text { on } \partial \Omega_{D} \quad \text { and } \quad \frac{\partial u}{\partial n}=g_{N} \text { on } \partial \Omega_{N},
\end{array}
$$
where $\partial \Omega_{D} \cup \partial \Omega_{N}=\partial \Omega$ and $\partial \Omega_{D}$ and $\partial \Omega_{N}$ are distinct.
-->
```
```{=html}
<!-- Weak form
Find $u \in \mathcal{H}_{E}^{1}$ such that

$$
\int_{\Omega} \nabla u \cdot \nabla v=\int_{\Omega} v f+\int_{\partial \Omega_{N}} v g_{N} \quad \text { for all } v \in \mathcal{H}_{E_{0}}^{1}
$$
-->
```


# Problem 2

> Repeat (1) for the problem
>
> $$
>  \begin{aligned}
>    -\Delta u &= \frac{\pi^2}{4}\left(\cos\frac{\pi r}{2} +
>    \operatorname{sinc} \frac{\pi r}{2}\right), & \quad &\text{in $\Omega$} \\
>            u &= 0, & &\text{on $\partial\Omega$}
>  \end{aligned}
> $$
>
> where $\Omega$ is again the unit disk. The exact solution is
> $u(x,y)=\cos \frac{\pi r}{2}$, where $r=\sqrt{x^2+y^2}$.

![Plot of the given closed-form
solution.](../img/analytic-b.png){width="50%"
style="margin:auto; display: block; max-width: 75%"}



# Problem 3

> (6 points) Explain why the convergence rate for problem (1) is half an
> order higher than for problem (2). To understand what's going on, it
> may be helpful to plot the contribution to the $H^1$ and $L^2$ errors
> element by element. (see the sample file `plot_errors.m`). For
> example, in problem 2, I got the following values when I integrated
>
> $$
> \iint_T \nabla(u_{FE} - u_{exact}) \cdot
> \nabla(u_{FE} - u_{exact})\,dx \, dy, \qquad
> (T\in\mathcal{T})
> $$
>
> over the triangles in `circle_iso/mesh3`:

> The $H^1$ semi-norm error in the finite element solution is the square
> root of the sum of all the errors shown here. (I got $0.00400512$ for
> the $H^1$ error and $7.5355\times10^{-5}$ for the $L^2$ error on this
> mesh).

![](../img/mesh5-gauss02-b-H1.png){width="50%"
style="margin:auto; display: block; max-width: 75%"}
![](../img/mesh5-gauss02-H1.png){width="50%"
style="margin:auto; display: block; max-width: 75%"}



# Appendix

## Solution plots

### Plots of Finite Element Solutions

![Finite element solution for problem 1 over mesh number 1 and order-2
numerical integration.](../img/mesh1-gauss02.png){width="50%"}

![Finite element solution for problem 1 over mesh number 1 and order-5
numerical integration.](../img/mesh1-gauss05.png){width="50%"}

![Finite element solution for problem 1 over mesh number 1 and order-8
numerical integration.](../img/mesh1-gauss08.png){width="50%"}

![Finite element solution for problem 1 over mesh number 1 and order-13
numerical integration.](../img/mesh1-gauss13.png){width="50%"}

![Finite element solution for problem 1 over mesh number 1 and order-19
numerical integration.](../img/mesh1-gauss19.png){width="50%"}

![Finite element solution for problem 1 over mesh number 2 and order-2
numerical integration.](../img/mesh2-gauss02.png){width="50%"}

![Finite element solution for problem 1 over mesh number 2 and order-5
numerical integration.](../img/mesh2-gauss05.png){width="50%"}

![Finite element solution for problem 1 over mesh number 2 and order-8
numerical integration.](../img/mesh2-gauss08.png){width="50%"}

![Finite element solution for problem 1 over mesh number 2 and order-13
numerical integration.](../img/mesh2-gauss13.png){width="50%"}

![Finite element solution for problem 1 over mesh number 2 and order-19
numerical integration.](../img/mesh2-gauss19.png){width="50%"}

![Finite element solution for problem 1 over mesh number 3 and order-2
numerical integration.](../img/mesh3-gauss02.png){width="50%"}

![Finite element solution for problem 1 over mesh number 3 and order-5
numerical integration.](../img/mesh3-gauss05.png){width="50%"}

![Finite element solution for problem 1 over mesh number 3 and order-8
numerical integration.](../img/mesh3-gauss08.png){width="50%"}

![Finite element solution for problem 1 over mesh number 3 and order-13
numerical integration.](../img/mesh3-gauss13.png){width="50%"}

![Finite element solution for problem 1 over mesh number 3 and order-19
numerical integration.](../img/mesh3-gauss19.png){width="50%"}

![Finite element solution for problem 1 over mesh number 4 and order-2
numerical integration.](../img/mesh4-gauss02.png){width="50%"}

![Finite element solution for problem 1 over mesh number 4 and order-5
numerical integration.](../img/mesh4-gauss05.png){width="50%"}

![Finite element solution for problem 1 over mesh number 4 and order-8
numerical integration.](../img/mesh4-gauss08.png){width="50%"}

![Finite element solution for problem 1 over mesh number 4 and order-13
numerical integration.](../img/mesh4-gauss13.png){width="50%"}

![Finite element solution for problem 1 over mesh number 4 and order-19
numerical integration.](../img/mesh4-gauss19.png){width="50%"}

![Finite element solution for problem 1 over mesh number 5 and order-2
numerical integration.](../img/mesh5-gauss02.png){width="50%"}

![Finite element solution for problem 1 over mesh number 5 and order-5
numerical integration.](../img/mesh5-gauss05.png){width="50%"}

![Finite element solution for problem 1 over mesh number 5 and order-8
numerical integration.](../img/mesh5-gauss08.png){width="50%"}

![Finite element solution for problem 1 over mesh number 5 and order-13
numerical integration.](../img/mesh5-gauss13.png){width="50%"}

![Finite element solution for problem 1 over mesh number 5 and order-19
numerical integration.](../img/mesh5-gauss19.png){width="50%"}

![Finite element solution for problem 1 over mesh number 1 and order-2
numerical integration.](../img/mesh1-gauss02-b.png){width="50%"}

![Finite element solution for problem 1 over mesh number 1 and order-5
numerical integration.](../img/mesh1-gauss05-b.png){width="50%"}

![Finite element solution for problem 1 over mesh number 1 and order-8
numerical integration.](../img/mesh1-gauss08-b.png){width="50%"}

![Finite element solution for problem 1 over mesh number 1 and order-13
numerical integration.](../img/mesh1-gauss13-b.png){width="50%"}

![Finite element solution for problem 1 over mesh number 1 and order-19
numerical integration.](../img/mesh1-gauss19-b.png){width="50%"}

![Finite element solution for problem 1 over mesh number 2 and order-2
numerical integration.](../img/mesh2-gauss02-b.png){width="50%"}

![Finite element solution for problem 1 over mesh number 2 and order-5
numerical integration.](../img/mesh2-gauss05-b.png){width="50%"}

![Finite element solution for problem 1 over mesh number 2 and order-8
numerical integration.](../img/mesh2-gauss08-b.png){width="50%"}

![Finite element solution for problem 1 over mesh number 2 and order-13
numerical integration.](../img/mesh2-gauss13-b.png){width="50%"}

![Finite element solution for problem 1 over mesh number 2 and order-19
numerical integration.](../img/mesh2-gauss19-b.png){width="50%"}

![Finite element solution for problem 1 over mesh number 3 and order-2
numerical integration.](../img/mesh3-gauss02-b.png){width="50%"}

![Finite element solution for problem 1 over mesh number 3 and order-5
numerical integration.](../img/mesh3-gauss05-b.png){width="50%"}

![Finite element solution for problem 1 over mesh number 3 and order-8
numerical integration.](../img/mesh3-gauss08-b.png){width="50%"}

![Finite element solution for problem 1 over mesh number 3 and order-13
numerical integration.](../img/mesh3-gauss13-b.png){width="50%"}

![Finite element solution for problem 1 over mesh number 3 and order-19
numerical integration.](../img/mesh3-gauss19-b.png){width="50%"}

![Finite element solution for problem 1 over mesh number 4 and order-2
numerical integration.](../img/mesh4-gauss02-b.png){width="50%"}

![Finite element solution for problem 1 over mesh number 4 and order-5
numerical integration.](../img/mesh4-gauss05-b.png){width="50%"}

![Finite element solution for problem 1 over mesh number 4 and order-8
numerical integration.](../img/mesh4-gauss08-b.png){width="50%"}

![Finite element solution for problem 1 over mesh number 4 and order-13
numerical integration.](../img/mesh4-gauss13-b.png){width="50%"}

![Finite element solution for problem 1 over mesh number 4 and order-19
numerical integration.](../img/mesh4-gauss19-b.png){width="50%"}

![Finite element solution for problem 1 over mesh number 5 and order-2
numerical integration.](../img/mesh5-gauss02-b.png){width="50%"}

![Finite element solution for problem 1 over mesh number 5 and order-5
numerical integration.](../img/mesh5-gauss05-b.png){width="50%"}

![Finite element solution for problem 1 over mesh number 5 and order-8
numerical integration.](../img/mesh5-gauss08-b.png){width="50%"}

![Finite element solution for problem 1 over mesh number 5 and order-13
numerical integration.](../img/mesh5-gauss13-b.png){width="50%"}

![Finite element solution for problem 1 over mesh number 5 and order-19
numerical integration.](../img/mesh5-gauss19-b.png){width="50%"}

### Errors in the $H^1$ and $L2$ norms

![](../img/mesh1-gauss02-L2.png){width="50%"}
![](../img/mesh1-gauss02-H1.png){width="50%"}
```{=tex}
\begin{figure}
\caption{Finite element error in the L2 and H1 norms/seminorms, respectively for problem 1 over mesh number 1 using order 2 quadrature.}
\end{figure}
```
![](../img/mesh1-gauss05-L2.png){width="50%"}
![](../img/mesh1-gauss05-H1.png){width="50%"}
```{=tex}
\begin{figure}
\caption{Finite element error in the L2 and H1 norms/seminorms, respectively for problem 1 over mesh number 1 using order 5 quadrature.}
\end{figure}
```
![](../img/mesh1-gauss08-L2.png){width="50%"}
![](../img/mesh1-gauss08-H1.png){width="50%"}
```{=tex}
\begin{figure}
\caption{Finite element error in the L2 and H1 norms/seminorms, respectively for problem 1 over mesh number 1 using order 8 quadrature.}
\end{figure}
```
![](../img/mesh1-gauss13-L2.png){width="50%"}
![](../img/mesh1-gauss13-H1.png){width="50%"}
```{=tex}
\begin{figure}
\caption{Finite element error in the L2 and H1 norms/seminorms, respectively for problem 1 over mesh number 1 using order 13 quadrature.}
\end{figure}
```
![](../img/mesh1-gauss19-L2.png){width="50%"}
![](../img/mesh1-gauss19-H1.png){width="50%"}
```{=tex}
\begin{figure}
\caption{Finite element error in the L2 and H1 norms/seminorms, respectively for problem 1 over mesh number 1 using order 19 quadrature.}
\end{figure}
```
![](../img/mesh2-gauss02-L2.png){width="50%"}
![](../img/mesh2-gauss02-H1.png){width="50%"}
```{=tex}
\begin{figure}
\caption{Finite element error in the L2 and H1 norms/seminorms, respectively for problem 1 over mesh number 2 using order 2 quadrature.}
\end{figure}
```
![](../img/mesh2-gauss05-L2.png){width="50%"}
![](../img/mesh2-gauss05-H1.png){width="50%"}
```{=tex}
\begin{figure}
\caption{Finite element error in the L2 and H1 norms/seminorms, respectively for problem 1 over mesh number 2 using order 5 quadrature.}
\end{figure}
```
![](../img/mesh2-gauss08-L2.png){width="50%"}
![](../img/mesh2-gauss08-H1.png){width="50%"}
```{=tex}
\begin{figure}
\caption{Finite element error in the L2 and H1 norms/seminorms, respectively for problem 1 over mesh number 2 using order 8 quadrature.}
\end{figure}
```
![](../img/mesh2-gauss13-L2.png){width="50%"}
![](../img/mesh2-gauss13-H1.png){width="50%"}
```{=tex}
\begin{figure}
\caption{Finite element error in the L2 and H1 norms/seminorms, respectively for problem 1 over mesh number 2 using order 13 quadrature.}
\end{figure}
```
![](../img/mesh2-gauss19-L2.png){width="50%"}
![](../img/mesh2-gauss19-H1.png){width="50%"}
```{=tex}
\begin{figure}
\caption{Finite element error in the L2 and H1 norms/seminorms, respectively for problem 1 over mesh number 2 using order 19 quadrature.}
\end{figure}
```
![](../img/mesh3-gauss02-L2.png){width="50%"}
![](../img/mesh3-gauss02-H1.png){width="50%"}
```{=tex}
\begin{figure}
\caption{Finite element error in the L2 and H1 norms/seminorms, respectively for problem 1 over mesh number 3 using order 2 quadrature.}
\end{figure}
```
![](../img/mesh3-gauss05-L2.png){width="50%"}
![](../img/mesh3-gauss05-H1.png){width="50%"}
```{=tex}
\begin{figure}
\caption{Finite element error in the L2 and H1 norms/seminorms, respectively for problem 1 over mesh number 3 using order 5 quadrature.}
\end{figure}
```
![](../img/mesh3-gauss08-L2.png){width="50%"}
![](../img/mesh3-gauss08-H1.png){width="50%"}
```{=tex}
\begin{figure}
\caption{Finite element error in the L2 and H1 norms/seminorms, respectively for problem 1 over mesh number 3 using order 8 quadrature.}
\end{figure}
```
![](../img/mesh3-gauss13-L2.png){width="50%"}
![](../img/mesh3-gauss13-H1.png){width="50%"}
```{=tex}
\begin{figure}
\caption{Finite element error in the L2 and H1 norms/seminorms, respectively for problem 1 over mesh number 3 using order 13 quadrature.}
\end{figure}
```
![](../img/mesh3-gauss19-L2.png){width="50%"}
![](../img/mesh3-gauss19-H1.png){width="50%"}
```{=tex}
\begin{figure}
\caption{Finite element error in the L2 and H1 norms/seminorms, respectively for problem 1 over mesh number 3 using order 19 quadrature.}
\end{figure}
```
![](../img/mesh4-gauss02-L2.png){width="50%"}
![](../img/mesh4-gauss02-H1.png){width="50%"}
```{=tex}
\begin{figure}
\caption{Finite element error in the L2 and H1 norms/seminorms, respectively for problem 1 over mesh number 4 using order 2 quadrature.}
\end{figure}
```
![](../img/mesh4-gauss05-L2.png){width="50%"}
![](../img/mesh4-gauss05-H1.png){width="50%"}
```{=tex}
\begin{figure}
\caption{Finite element error in the L2 and H1 norms/seminorms, respectively for problem 1 over mesh number 4 using order 5 quadrature.}
\end{figure}
```
![](../img/mesh4-gauss08-L2.png){width="50%"}
![](../img/mesh4-gauss08-H1.png){width="50%"}
```{=tex}
\begin{figure}
\caption{Finite element error in the L2 and H1 norms/seminorms, respectively for problem 1 over mesh number 4 using order 8 quadrature.}
\end{figure}
```
![](../img/mesh4-gauss13-L2.png){width="50%"}
![](../img/mesh4-gauss13-H1.png){width="50%"}
```{=tex}
\begin{figure}
\caption{Finite element error in the L2 and H1 norms/seminorms, respectively for problem 1 over mesh number 4 using order 13 quadrature.}
\end{figure}
```
![](../img/mesh4-gauss19-L2.png){width="50%"}
![](../img/mesh4-gauss19-H1.png){width="50%"}
```{=tex}
\begin{figure}
\caption{Finite element error in the L2 and H1 norms/seminorms, respectively for problem 1 over mesh number 4 using order 19 quadrature.}
\end{figure}
```
![](../img/mesh5-gauss02-L2.png){width="50%"}
![](../img/mesh5-gauss02-H1.png){width="50%"}
```{=tex}
\begin{figure}
\caption{Finite element error in the L2 and H1 norms/seminorms, respectively for problem 1 over mesh number 5 using order 2 quadrature.}
\end{figure}
```
![](../img/mesh5-gauss05-L2.png){width="50%"}
![](../img/mesh5-gauss05-H1.png){width="50%"}
```{=tex}
\begin{figure}
\caption{Finite element error in the L2 and H1 norms/seminorms, respectively for problem 1 over mesh number 5 using order 5 quadrature.}
\end{figure}
```
![](../img/mesh5-gauss08-L2.png){width="50%"}
![](../img/mesh5-gauss08-H1.png){width="50%"}
```{=tex}
\begin{figure}
\caption{Finite element error in the L2 and H1 norms/seminorms, respectively for problem 1 over mesh number 5 using order 8 quadrature.}
\end{figure}
```
![](../img/mesh5-gauss13-L2.png){width="50%"}
![](../img/mesh5-gauss13-H1.png){width="50%"}
```{=tex}
\begin{figure}
\caption{Finite element error in the L2 and H1 norms/seminorms, respectively for problem 1 over mesh number 5 using order 13 quadrature.}
\end{figure}
```
![](../img/mesh5-gauss19-L2.png){width="50%"}
![](../img/mesh5-gauss19-H1.png){width="50%"}
```{=tex}
\begin{figure}
\caption{Finite element error in the L2 and H1 norms/seminorms, respectively for problem 1 over mesh number 5 using order 19 quadrature.}
\end{figure}
```
![](../img/mesh1-gauss02-b-L2.png){width="50%"}
![](../img/mesh1-gauss02-b-H1.png){width="50%"}
```{=tex}
\begin{figure}
\caption{Finite element error in the L2 and H1 norms/seminorms, respectively for problem 1 over mesh number 1 using order 2 quadrature.}
\end{figure}
```
![](../img/mesh1-gauss05-b-L2.png){width="50%"}
![](../img/mesh1-gauss05-b-H1.png){width="50%"}
```{=tex}
\begin{figure}
\caption{Finite element error in the L2 and H1 norms/seminorms, respectively for problem 1 over mesh number 1 using order 5 quadrature.}
\end{figure}
```
![](../img/mesh1-gauss08-b-L2.png){width="50%"}
![](../img/mesh1-gauss08-b-H1.png){width="50%"}
```{=tex}
\begin{figure}
\caption{Finite element error in the L2 and H1 norms/seminorms, respectively for problem 1 over mesh number 1 using order 8 quadrature.}
\end{figure}
```
![](../img/mesh1-gauss13-b-L2.png){width="50%"}
![](../img/mesh1-gauss13-b-H1.png){width="50%"}
```{=tex}
\begin{figure}
\caption{Finite element error in the L2 and H1 norms/seminorms, respectively for problem 1 over mesh number 1 using order 13 quadrature.}
\end{figure}
```
![](../img/mesh1-gauss19-b-L2.png){width="50%"}
![](../img/mesh1-gauss19-b-H1.png){width="50%"}
```{=tex}
\begin{figure}
\caption{Finite element error in the L2 and H1 norms/seminorms, respectively for problem 1 over mesh number 1 using order 19 quadrature.}
\end{figure}
```
![](../img/mesh2-gauss02-b-L2.png){width="50%"}
![](../img/mesh2-gauss02-b-H1.png){width="50%"}
```{=tex}
\begin{figure}
\caption{Finite element error in the L2 and H1 norms/seminorms, respectively for problem 1 over mesh number 2 using order 2 quadrature.}
\end{figure}
```
![](../img/mesh2-gauss05-b-L2.png){width="50%"}
![](../img/mesh2-gauss05-b-H1.png){width="50%"}
```{=tex}
\begin{figure}
\caption{Finite element error in the L2 and H1 norms/seminorms, respectively for problem 1 over mesh number 2 using order 5 quadrature.}
\end{figure}
```
![](../img/mesh2-gauss08-b-L2.png){width="50%"}
![](../img/mesh2-gauss08-b-H1.png){width="50%"}
```{=tex}
\begin{figure}
\caption{Finite element error in the L2 and H1 norms/seminorms, respectively for problem 1 over mesh number 2 using order 8 quadrature.}
\end{figure}
```
![](../img/mesh2-gauss13-b-L2.png){width="50%"}
![](../img/mesh2-gauss13-b-H1.png){width="50%"}
```{=tex}
\begin{figure}
\caption{Finite element error in the L2 and H1 norms/seminorms, respectively for problem 1 over mesh number 2 using order 13 quadrature.}
\end{figure}
```
![](../img/mesh2-gauss19-b-L2.png){width="50%"}
![](../img/mesh2-gauss19-b-H1.png){width="50%"}
```{=tex}
\begin{figure}
\caption{Finite element error in the L2 and H1 norms/seminorms, respectively for problem 1 over mesh number 2 using order 19 quadrature.}
\end{figure}
```
![](../img/mesh3-gauss02-b-L2.png){width="50%"}
![](../img/mesh3-gauss02-b-H1.png){width="50%"}
```{=tex}
\begin{figure}
\caption{Finite element error in the L2 and H1 norms/seminorms, respectively for problem 1 over mesh number 3 using order 2 quadrature.}
\end{figure}
```
![](../img/mesh3-gauss05-b-L2.png){width="50%"}
![](../img/mesh3-gauss05-b-H1.png){width="50%"}
```{=tex}
\begin{figure}
\caption{Finite element error in the L2 and H1 norms/seminorms, respectively for problem 1 over mesh number 3 using order 5 quadrature.}
\end{figure}
```
![](../img/mesh3-gauss08-b-L2.png){width="50%"}
![](../img/mesh3-gauss08-b-H1.png){width="50%"}
```{=tex}
\begin{figure}
\caption{Finite element error in the L2 and H1 norms/seminorms, respectively for problem 1 over mesh number 3 using order 8 quadrature.}
\end{figure}
```
![](../img/mesh3-gauss13-b-L2.png){width="50%"}
![](../img/mesh3-gauss13-b-H1.png){width="50%"}
```{=tex}
\begin{figure}
\caption{Finite element error in the L2 and H1 norms/seminorms, respectively for problem 1 over mesh number 3 using order 13 quadrature.}
\end{figure}
```
![](../img/mesh3-gauss19-b-L2.png){width="50%"}
![](../img/mesh3-gauss19-b-H1.png){width="50%"}
```{=tex}
\begin{figure}
\caption{Finite element error in the L2 and H1 norms/seminorms, respectively for problem 1 over mesh number 3 using order 19 quadrature.}
\end{figure}
```
![](../img/mesh4-gauss02-b-L2.png){width="50%"}
![](../img/mesh4-gauss02-b-H1.png){width="50%"}
```{=tex}
\begin{figure}
\caption{Finite element error in the L2 and H1 norms/seminorms, respectively for problem 1 over mesh number 4 using order 2 quadrature.}
\end{figure}
```
![](../img/mesh4-gauss05-b-L2.png){width="50%"}
![](../img/mesh4-gauss05-b-H1.png){width="50%"}
```{=tex}
\begin{figure}
\caption{Finite element error in the L2 and H1 norms/seminorms, respectively for problem 1 over mesh number 4 using order 5 quadrature.}
\end{figure}
```
![](../img/mesh4-gauss08-b-L2.png){width="50%"}
![](../img/mesh4-gauss08-b-H1.png){width="50%"}
```{=tex}
\begin{figure}
\caption{Finite element error in the L2 and H1 norms/seminorms, respectively for problem 1 over mesh number 4 using order 8 quadrature.}
\end{figure}
```
![](../img/mesh4-gauss13-b-L2.png){width="50%"}
![](../img/mesh4-gauss13-b-H1.png){width="50%"}
```{=tex}
\begin{figure}
\caption{Finite element error in the L2 and H1 norms/seminorms, respectively for problem 1 over mesh number 4 using order 13 quadrature.}
\end{figure}
```
![](../img/mesh4-gauss19-b-L2.png){width="50%"}
![](../img/mesh4-gauss19-b-H1.png){width="50%"}
```{=tex}
\begin{figure}
\caption{Finite element error in the L2 and H1 norms/seminorms, respectively for problem 1 over mesh number 4 using order 19 quadrature.}
\end{figure}
```
![](../img/mesh5-gauss02-b-L2.png){width="50%"}
![](../img/mesh5-gauss02-b-H1.png){width="50%"}
```{=tex}
\begin{figure}
\caption{Finite element error in the L2 and H1 norms/seminorms, respectively for problem 1 over mesh number 5 using order 2 quadrature.}
\end{figure}
```
![](../img/mesh5-gauss05-b-L2.png){width="50%"}
![](../img/mesh5-gauss05-b-H1.png){width="50%"}
```{=tex}
\begin{figure}
\caption{Finite element error in the L2 and H1 norms/seminorms, respectively for problem 1 over mesh number 5 using order 5 quadrature.}
\end{figure}
```
![](../img/mesh5-gauss08-b-L2.png){width="50%"}
![](../img/mesh5-gauss08-b-H1.png){width="50%"}
```{=tex}
\begin{figure}
\caption{Finite element error in the L2 and H1 norms/seminorms, respectively for problem 1 over mesh number 5 using order 8 quadrature.}
\end{figure}
```
![](../img/mesh5-gauss13-b-L2.png){width="50%"}
![](../img/mesh5-gauss13-b-H1.png){width="50%"}
```{=tex}
\begin{figure}
\caption{Finite element error in the L2 and H1 norms/seminorms, respectively for problem 1 over mesh number 5 using order 13 quadrature.}
\end{figure}
```
![](../img/mesh5-gauss19-b-L2.png){width="50%"}
![](../img/mesh5-gauss19-b-H1.png){width="50%"}
```{=tex}
\begin{figure}
\caption{Finite element error in the L2 and H1 norms/seminorms, respectively for problem 1 over mesh number 5 using order 19 quadrature.}
\end{figure}
```


## Source Code of Interest

``` {.python}
# Claudio Perez
# May 2021
import jax
import anon.diff as diff
from anabel.template import template
import anabel.backend as anp


@template(6)
def poisson2(transf, test, trial, f=lambda x: 0.0, ndim=2, points=None, weights=None, thickness=1.0, **kwds):
    """
    Parameters
    ----------
    test, trial : Callable
        test and trial interpolants over the reference element.
    thickness : float
    
    http://people.inf.ethz.ch/arbenz/FEM17/pdfs/0-19-852868-X.pdf
    """
    state = {}
    
    det = anp.linalg.det
    slv = anp.linalg.solve
    
    jacn_test = diff.jacx(test)
    jacn_trial = diff.jacx(trial)
    
    def transf(xi, xyz):
        return test(xi)@xyz
    
    def jacn_transf(xi,xyz):
        return jacn_test(xi)@xyz
    
    def jacx_test(xi,xyz): 
        return slv(jacn_transf(xi,xyz), jacn_test(xi))
    
    def dvol(xi, xyz): 
        return 0.5*thickness*(abs(det(jacn_transf(xi,xyz))))
    
    def stif(u,xyz,xi,wght,**kwds):
        dNdx = jacx_test(xi,xyz)
        return (dNdx.T@dNdx)*dvol(xi,xyz)*wght
    
    fj = jax.vmap(f,0)
    
    def resp(u,xyz,xi,wght,**kwds):
        dNdx = jacx_test(xi,xyz)
        N = test(xi)[:,None]
        p = (dNdx.T@dNdx)@u*dvol(xi,xyz)*wght - (N@N.T)@fj(xyz)[:,None]*dvol(xi,xyz)*wght
        return p
    
    integral = jax.vmap(resp,(None,None,0,0))
    jac_integral = jax.vmap(stif,(None, None, 0, 0))
    
    def jacx(u,__,___,xyz,points,weights):
        return sum(jac_integral(u,xyz,points,weights))

    def main(u,__,___,xyz,points,weights):
        return sum(integral(u,xyz,points,weights))
    return locals()

@template(1)
def L2(transf,test,trial,u,quad_point=None, thickness=1.0):
    state = None
    det = anp.linalg.det
    slv = anp.linalg.solve
    du = lambda x: diff.jacfwd(u)(x)[:,None]
    jacn_test = diff.jacx(test)
    jacn_trial = diff.jacx(trial)

    def transf(xi, xyz):
        return test(xi)@xyz
    
    def jacn_transf(xi,xyz):
        return jacn_test(xi)@xyz

    dvol = lambda xi, xyz: 0.5*thickness*abs(det(jacn_transf(xi,xyz)))
     
    def resp(U,xyz,xi, wght):
        N = test(xi)[:,None]
        tmp = u(transf(xi,xyz)) - N.T@U
        q =  tmp.T@tmp * dvol(xi,xyz) * wght
        return q
    
    integral = jax.vmap(resp,(None,None,0,0))

    def main(u,__,___,xyz,points,weights):
        return sum(integral(u,xyz,points,weights))
    
    return locals()


@template(1)
def H1_v1(transf,test,trial,u,quad_point=None, thickness=1.0):
    state = None
    det = anp.linalg.det
    slv = anp.linalg.solve
    du = lambda x: diff.jacfwd(u)(x)[:,None]
    jacn_test = diff.jacx(test)
    jacn_trial = diff.jacx(trial)

    def transf(xi, xyz):
        return test(xi)@xyz
    
    def jacn_transf(xi,xyz):
        return jacn_test(xi)@xyz

    jacx_test = lambda xi,xyz: slv(jacn_transf(xi,xyz), jacn_test(xi))
    dvol = lambda xi, xyz: 0.5*thickness*abs(det(jacn_transf(xi,xyz)))
    
    
    def resp(U,xyz,xi, wght):
        tmp = du(transf(xi,xyz)) - jacx_test(xi,xyz)@U
        q = tmp.T@tmp * dvol(xi,xyz) * wght
        return q

    integral = jax.vmap(resp,(None,None,0,0))

    def main(u,__,___,xyz,points,weights):
        return sum(integral(u,xyz,points,weights))
    
    return locals()

@template(1)
def H1(transf,test,trial,u,quad_point=None, thickness=1.0):
    state = None
    det = anp.linalg.det
    slv = anp.linalg.solve
    du = lambda x: diff.jacfwd(u)(x)[:,None]
    jacn_test = diff.jacx(test)
    jacn_trial = diff.jacx(trial)

    def transf(xi, xyz):
        return test(xi)@xyz
    
    def jacn_transf(xi,xyz):
        return jacn_test(xi)@xyz

    jacx_test = lambda xi,xyz: slv(jacn_transf(xi,xyz), jacn_test(xi))
    dvol = lambda xi, xyz: 0.5*thickness*abs(det(jacn_transf(xi,xyz)))

    def resp(U,xyz,xi, wght):
        tmp = jacx_test(xi,xyz)@(U - u(transf(xi,xyz)))
        q = tmp.T@tmp * dvol(xi,xyz) * wght
        return q

    integral = jax.vmap(resp,(None,None,0,0))

    def main(u,__,___,xyz,points,weights):
        return sum(integral(u,xyz,points,weights))
    
    return locals()


```
