
# Problem 1 ($\mathbf{u}_t + A \mathbf{u}_x = \mathbf{0}$)

>Consider the Riemann problem
>
>$$
\begin{gathered}
  \begin{pmatrix} p \\ u \end{pmatrix}_t +
  \begin{pmatrix} 0 & c_0^2\rho_0 \\ 1/\rho_0 & 0 \end{pmatrix}
  \begin{pmatrix} p \\ u \end{pmatrix}_x =
  \begin{pmatrix} 0 \\ 0 \end{pmatrix}, \qquad (x\in\mathbb R\;,\; t>0) \\[5pt]
  p(x,0)=\left\{ \begin{array}{cc} p_L & x<0 \\ p_R & x>0 \end{array}\right\}, \quad
  u(x,0)=\left\{ \begin{array}{cc} u_L & x<0 \\ u_R & x>0 \end{array}\right\}
\end{gathered}
>$$
>
>describing linear acoustics.  Compute the exact solution
$p(x,t)$ and $u(x,t)$ for $x\in\mathbb R$, $t>0$. Here $c_0$ and $\rho_0$ are
positive constants while $u_L$, $u_R$, $p_L$ and $p_R$ are arbitrary real
constants.


$$
A = Q\Lambda Q^{-1} = 
\begin{pmatrix} 1 & -c_0 \rho_0 \\ \frac{1}{c_0 \rho_0} & 1 \end{pmatrix}
\begin{pmatrix}c_0 & 0 \\ 0 & -c_0\end{pmatrix}
\begin{pmatrix}1/2 & c_0 \rho_0 /2 \\ \frac{-1}{2 c_0 \rho_0 } & 1/2\end{pmatrix}
$$


$$
\mathbf{w}(x,0)=\left\{ \begin{array}{cc} \mathbf{w}_L & x<0 \\ \mathbf{w}_R & x>0 \end{array}\right.
$$

Characteristics:

$$
x_i^0 = x - \lambda_i t \quad i=1,2
$$

$$
w_i(x,t)=\left\{\begin{array}{cc} w_i^L & x_0(x,t)<0 \\ w_i^R & x_0(x,t)>0 \end{array}\right.
$$

Using $\mathbf{w} = Q^{-1}\mathbf{u}$

$$
w_1 = \frac{p + c_0 \rho_0 u}{2} \\
$$

$$
w_2 = \frac{u}{2} - \frac{1}{ 2 c_0 \rho_0 }p
$$

where the superscript 

<!-- jump conditions -->

<!--
$$
\mathbf{u}(x,t)=\left\{\begin{array}{cc} 
  \left\{\begin{array}{cc} 
    \mathbf{q}_iw_i^L & x_0(x,t)<0\\
    a
  \end{array} \right. & x^0
   \\ w_i^R & x_0(x,t)>0 \end{array}\right.
$$
-->

Decomposing $Q$ into column vectors $\mathbf{q}_j$, and summing on $j=1,2$:

$$
\mathbf{u}(x,t)= 
  \left\{\begin{array}{cc} 
   \mathbf{q}_jw_j^L & x^0_i(x,t)<0\\
   \mathbf{q}_jw_j^R & x^0_i(x,t)>0
  \end{array} \right.
$$

<!-- For eigen values -->

Expanding for all regions yields

$$
\mathbf{u}(x,t)= 
 \left\{\begin{array}{cc} 
  \mathbf{q}_1w_1^L + \mathbf{q}_2w_2^L& x^0_2(x,t)<0\\
  \mathbf{q}_1w_1^L + \mathbf{q}_2w_2^R& x^0_1(x,t)> 0 > x^0_2(x,t)\\
  \mathbf{q}_1w_1^R + \mathbf{q}_2w_2^L& x^0_1(x,t)< 0 < x^0_2(x,t)\\
  \mathbf{q}_1w_1^R + \mathbf{q}_2w_2^R& x^0_1(x,t)>0
 \end{array} \right.
$$

The region $x_1^0 > 0 > x_2^0$ is not valid for the eigenvalues $\lambda = (c_0, -c_0)^T$ so that the only intermediate state is

$$
\mathbf{u}^M = \mathbf{q}_1w_1^R + \mathbf{q}_2 w_2^L , \quad x^0_1(x,t)< 0 < x^0_2(x,t)
$$

$$
\boxed{
\begin{gathered}
p^M =  \frac{1}{2}\left(p^R+c_0 \rho_0 u^R\right) -\frac{1}{2} \left(c_0\rho_0 u^L - p^L\right) \\
u^M = \frac{1}{2\rho_0 c_0} \left(p^R + \rho_0 c_0 u^R\right) + \frac{u^R}{2} - \frac{p^L}{2 \rho_0 c_0}  \\
\mathbf{u}^M = \begin{pmatrix} p^M \\ u^M\end{pmatrix} \\
\mathbf{u}(x,t)= 
 \left\{\begin{array}{cc} 
 \mathbf{u}^L & x^0_2(x,t)<0\\
 \mathbf{u}^M & x^0_1(x,t)< 0 < x^0_2(x,t)\\
 \mathbf{u}^R & x^0_1(x,t)>0\\
 \end{array} \right.\\
\end{gathered}}
$$



\pagebreak

# Problem 2. 

>Consider the nonlinear isothermal equations of gas dynamics,
>
>$$
  \begin{pmatrix} \rho \\ m \end{pmatrix}_t +
  \begin{pmatrix} m \\ \frac{m^2}\rho + a^2\rho \end{pmatrix}_x =
  \begin{pmatrix} 0 \\ 0 \end{pmatrix}.
>$$
>
>Here $m$ is the momentum and the velocity of the gas is $v=m/\rho$.
Let $a=1$ and consider the Reimann problem
$\rho(x,0)=\left\{\begin{array}{cc} \rho_0 & x<0 \\ \rho_2 & x>0 \end{array}\right\}$, $m(x,0)=\left\{\begin{array}{cc} m_0 & x<0 \\ m_2 & x>0 \end{array}\right\}$, where
>
>$$
  q_0 = \begin{pmatrix} \rho_0 \\ m_0 \end{pmatrix} = \begin{pmatrix} 1 \\ 3 \end{pmatrix}, \qquad
  q_2 = \begin{pmatrix} \rho_2 \\ m_2 \end{pmatrix} = \begin{pmatrix} 1 \\ 0 \end{pmatrix}.
>$$
>
>Find an intermediate state $q_1=\begin{pmatrix} \rho_1 \\ m_1 \end{pmatrix}$ and shock speeds
$\dot s_1$ and $\dot s_2$ such that
>
>$$
 F(q_i)-F(q_{i-1}) = \dot s_i(q_i-q_{i-1}), \qquad (i=1,2), \qquad \dot s_2>\dot s_1.
>$$
>

```{.include}
5/p2.md
```


>Confirm that $\lambda_{01}>\dot s_1>\lambda_{11}$ and
$\lambda_{12}>\dot s_2>\lambda_{22}$, which are Lax's entropy conditions for this system.
Also confirm that $v_0>\dot s_1$, $v_1>\dot s_1$, $\dot s_2>v_1$ and $\dot s_2>v_2$,
which means fluid particles move from the original states $q_0$ and $q_2$ to the
auxiliary state $q_1$ as the shocks propagate through space and time.



\pagebreak

# Problem 3 ($-\alpha u_{xx} + Au = f$)

>Write a 1d finite element code to solve the modified Poisson equation
>$$
  -\alpha u_{xx} + Au = f, \quad (0\le x\le 1), \qquad u(0)=0,\; u(1)=0,
>$$
>where $\alpha>0$ and $A\ge0$. Use 4th order finite elments on a uniformly spaced grid,
>
>$$
  x_j = j/M, \qquad\quad 0\le j\le M
>$$
>
>where $M$ is divisible by 4 and the $r$th element includes nodes $x_{4r+i}$ for
$0\le r<M/4$ and $0\le i\le 4$. 

## Part A

Multiplying by a test function $v$ and integrating over the domain (applying integration by parts) yields:

$$
\int_\Omega -\alpha u_{xx} v + \gamma u v = \int_\Omega f v
$$

$$
\int \alpha u_x v_x dx - \left. \alpha u_x v \right| + \gamma \int u v dx = \int f v dx
$$

For test functions which vanish on the boundary one obtains:

$$
\int_\Omega \alpha u_x v_x + \gamma u v = \int_\Omega f v
$$

$$
a(\alpha u,v) + \langle Au,v \rangle = \langle f,v\rangle
$$

### Fourth-order element

A fourth order isoparametric 1D element is developed by applying Lagrange interpolation over 5 equally spaced sampling points.

![Shape functions](../img/lagrange.png)


### Convergence

>(a) Do a convergence study for $\alpha=1/100$, $A=0$ and $f(x)=\frac{\pi^2}{100}\sum_{k=0}^4 \sin\big((2k+1)\pi x \big)$.

The exact integral for this problem is as follows:

$$
\frac{1}{\alpha 100} \sum{\frac{1}{(2k+1)^2}\sin{\left((2k+1)\pi x\right)} }
$$

![Source curve $f$ and exact solution $u$](../img/p3a-exact.png)

![Convergence study for finite element solution of steady-state problem.](../img/p3a-conv.png)

\pagebreak

## Part B: Transient Analysis

>(b) Solve $u_t=\frac1{100}u_{xx}+f(x)\sin(\pi t)$ from $t=0$ to
$t=1$ with initial condition $u(x,0)=0$ and the same $f$ as in part (a).  Use the 4th order implicit SDIRK timestepper with Butcher array given in problem 2 of HW 2. Use your finite element code above to solve the implicit equation for each stage of the
timestepper. (I'll explain this in class). Make a convergence plot for several values of $M$ and one choice of $\nu=k/h$ that you find works well.

The exact solution of the transient problem was derrived using the `sympy` CAS library. A plot is shown below for various times.

![Analytic solution curves](../img/p3b-exact.png)

![FEM solution](../img/p3b-fem-iso.png)

### SDIRK Implementation

In HW2 a Runge-Kutta algorithm was implemented for problems with the following form:

$$
\mathbf{u}_t + B\mathbf{u} = \mathbf{d}(t)
$$

Where $B$ is a linear operator . At stage $i$ of a diagonal Runge-Kutta method one has

$$
\ell_{i}=F\left(t_{n}+c_{i} k, \vec{u}_{n}+k \sum_{j=1}^{i-1} a_{i j} \ell_{j}+k a_{i j} \ell_{i}\right)
$$

where $k=\Delta t$. For problems of the aforementioned form, this simplifies to

$$
\left(I - k a_{i i} B\right) \ell_{i} = B \left(\vec{u}_{n}+k \sum_{j=1}^{i-1} a_{i j} \ell_{j}\right) + d(t_n+c_i k) 
$$

The following data is required to set up a particular scheme for $\mathbf{u}\in \mathbb{R}^n$ with $s\in\mathbf{Z^+}$ stages:

$\mathcal{T}$
: A Butcher tableau with zero entries above the diagonal.

$B, \mathbb{R}^n \rightarrow \mathbb{R}^n$: Discrete space operator

$\mathbf{d}, \mathbb{R} \rightarrow \mathbb{R}^n$
: Source term.

The problem at hand is manipulated to fit the following form:

$$\vec{u}_{t}=-\frac{1}{100} {M}^{-1} A \vec{u}+\vec{f} \sin \pi t$$

so that 

$$
\begin{gathered}
B=\frac{-1}{100}M^{-1}A \\
\mathbf{d}=M^{-1}b\sin{\pi t}
\end{gathered}
$$


where $A$, $M$, and $b$ are the stiffness, mass and load vectors as readily produced by the implementation for Part B.

$$
\left(M+\frac{k a_{i i}}{100} A\right) l_{i} = -\frac{1}{100} A\left(\vec{u}_{n}+k \sum_{j=1}^{i-1} a_{i j} \ell_{j}\right) + M \vec{f} \sin \pi\left(t_{n}+c_{i} k\right)
$$


The tableau $\mathcal{T}$ is given as 

$$
\begin{array}{c|ccccc}
  1/4 & 1/4 \\
  3/4 & 1/2 & 1/4 \\
  11/20 & 17/50 & -1/25 & 1/4 \\
  1/2 & 371/1360 & -137/2720 & 15/544 & 1/4 \\
  1 & 25/24 & -49/48 & 125/16 & -85/12 & 1/4 \\
  \hline
  & 25/24 & -49/48 & 125/16 & -85/12 & 1/4
\end{array}
$$


---------------

$u(x,t) = \sum_j u_j(t)\phi_j(x)$

$$u_{t}=\frac{1}{100} u_{x x}+f(x) \sin \pi t$$

let $u_t = \sum_ju_{j,t}\phi_j$, and $v=\phi_i$

$$
\langle u_{t}, v\rangle = -\frac{1}{100} a(u, v)+\langle f, v\rangle \sin \pi t
$$


$$
M \vec{u}_{t}=-\frac{1}{100} A \vec{u} + M \vec{f} \sin \pi t
$$


$$
\vec{u}_{t}=-\frac{1}{100} {M}^{-1} A \vec{u}+\vec{f} \sin \pi t
$$

<!-- where $M^{-1}A$ is a FE approximation to $-\Delta()$. -->


### Convergence

Convergence studies are presented below for time discretizations using both the SDIRK scheme provided and the Crank-Nicolson scheme.

![Convergence study.](../img/p3b-conv.png)

![Convergence study for Crank-Nicolson tableau.](../img/p3b-conv-cn.png)

\pagebreak

# Appendix

Key source code excerpts are provided below. The Python libraries `elle`, `emme`, `anon` and `m228` which have been used throughout are self written and available either from [PyPi.org](PyPi.org) via `pip` or on Github.

## Source Code

### Fourth-order Lagrange element

```{include=5/elle_0001.py .python}
```

\pagebreak

### Analytic Transient Solution

```{include=5/p3b.py .python}
```

