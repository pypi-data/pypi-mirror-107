# Problem 1 ($\mathbf{u}_t + A \mathbf{u}_x = \mathbf{0}$)

> Consider the Riemann problem
>
> $$
> \begin{gathered}
> \begin{pmatrix} p \\ u \end{pmatrix}_t +
> \begin{pmatrix} 0 & c_0^2\rho_0 \\ 1/\rho_0 & 0 \end{pmatrix}
> \begin{pmatrix} p \\ u \end{pmatrix}_x =
> \begin{pmatrix} 0 \\ 0 \end{pmatrix}, \qquad (x\in\mathbb R\;,\; t>0) \\[5pt]
> p(x,0)=\left\{ \begin{array}{cc} p_L & x<0 \\ p_R & x>0 \end{array}\right\}, \quad
> u(x,0)=\left\{ \begin{array}{cc} u_L & x<0 \\ u_R & x>0 \end{array}\right\}
> \end{gathered}
> $$
>
> describing linear acoustics. Compute the exact solution $p(x,t)$ and
> $u(x,t)$ for $x\in\mathbb R$, $t>0$. Here $c_0$ and $\rho_0$ are
> positive constants while $u_L$, $u_R$, $p_L$ and $p_R$ are arbitrary
> real constants.

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

```{=html}
<!-- jump conditions -->
```
```{=html}
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
```
Decomposing $Q$ into column vectors $\mathbf{q}_j$, and summing on
$j=1,2$:

$$
\mathbf{u}(x,t)= 
  \left\{\begin{array}{cc} 
   \mathbf{q}_jw_j^L & x^0_i(x,t)<0\\
   \mathbf{q}_jw_j^R & x^0_i(x,t)>0
  \end{array} \right.
$$

```{=html}
<!-- For eigen values -->
```
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

The region $x_1^0 > 0 > x_2^0$ is not valid for the eigenvalues
$\lambda = (c_0, -c_0)^T$ so that the only intermediate state is

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



# Problem 2.

> Consider the nonlinear isothermal equations of gas dynamics,
>
> $$
> \begin{pmatrix} \rho \\ m \end{pmatrix}_t +
> \begin{pmatrix} m \\ \frac{m^2}\rho + a^2\rho \end{pmatrix}_x =
> \begin{pmatrix} 0 \\ 0 \end{pmatrix}.
> $$
>
> Here $m$ is the momentum and the velocity of the gas is $v=m/\rho$.
> Let $a=1$ and consider the Reimann problem
> $\rho(x,0)=\left\{\begin{array}{cc} \rho_0 & x<0 \\ \rho_2 & x>0 \end{array}\right\}$,
> $m(x,0)=\left\{\begin{array}{cc} m_0 & x<0 \\ m_2 & x>0 \end{array}\right\}$,
> where
>
> $$
> q_0 = \begin{pmatrix} \rho_0 \\ m_0 \end{pmatrix} = \begin{pmatrix} 1 \\ 3 \end{pmatrix}, \qquad
> q_2 = \begin{pmatrix} \rho_2 \\ m_2 \end{pmatrix} = \begin{pmatrix} 1 \\ 0 \end{pmatrix}.
> $$
>
> Find an intermediate state
> $q_1=\begin{pmatrix} \rho_1 \\ m_1 \end{pmatrix}$ and shock speeds
> $\dot s_1$ and $\dot s_2$ such that
>
> $$
> F(q_i)-F(q_{i-1}) = \dot s_i(q_i-q_{i-1}), \qquad (i=1,2), \qquad \dot s_2>\dot s_1.
> $$

```{=html}
<!-- ## Shock -->
```
Following @leveque1992numerical and beginning at the Rankine-Hugoniot
condition, the following system of equations is obtained:

$$
\begin{aligned}
\tilde{m}-\hat{m} &=s(\tilde{\rho}-\hat{\rho}) \\
\left(\tilde{m}^{2} / \tilde{\rho}+a^{2} \tilde{\rho}\right)-\left(\hat{m}^{2} / \hat{\rho}+a^{2} \hat{\rho}\right) &=s(\tilde{m}-\hat{m})
\end{aligned}
$$

![Graphical solution of the isothermal Riemann
problem](../img/p1-locus.png)

$$
\rho_{1} m_{0} / \rho_{0}-a \sqrt{\rho_{1} / \rho_{0}}\left(\rho_{1}-\rho_{0}\right)=\rho_{1} m_{2} / \rho_{2}+a \sqrt{\rho_{1} / \rho_{2}}\left(\rho_{1}-\rho_{2}\right)
$$

$$
\left(\frac{a}{\sqrt{\rho_{2}}}+\frac{a}{\sqrt{\rho_{0}}}\right) z^{2}+\left(\frac{m_{2}}{\rho_{2}}-\frac{m_{0}}{\rho_{0}}\right) z-a\left(\sqrt{\rho_{2}}+\sqrt{\rho_{0}}\right)=0
$$

Plugging in the specified values for $q_0$ and $q_2$ yields the
following coefficients:

$$
\begin{aligned}
\frac{a}{\sqrt{\rho_{2}}}+\frac{a}{\sqrt{\rho_{0}}} = 2\\
\frac{m_{2}}{\rho_{2}}-\frac{m_{0}}{\rho_{0}} = -3\\
a\left(\sqrt{\rho_{2}}+\sqrt{\rho_{0}}\right) = -2
\end{aligned}
$$

This yields the following roots:

$$
\rho_1 = \left\{\frac{1}{4}, 4\right\} \\
$$

$$
m_1 =\rho_{m} m_{r} / \rho_{r}+a \sqrt{\rho_{m} / \rho_{r}}\left(\rho_{m}-\rho_{r}\right) \\
$$

`<!-- = \left\{\frac{9}{8}, 6\right\} -->`{=html}

$$
\boxed{q_1 = \begin{pmatrix}4 \\ 6\end{pmatrix}}
$$

> In each region $i=0,1,2$, compute the characteristic speeds, which are
> the eigenvalues $\lambda_{i1}$ and $\lambda_{i2}$ of the Jacobian
> $J_i=DF(q_i)$. Also compute the fluid velocities $v_i$.

$$
DF(q_i)=\begin{pmatrix}
0 & 1 \\
a^{2}-m_i^{2} / \rho_i^{2} & 2 m_i / \rho_i
\end{pmatrix}
$$

### State $i=0$

$$
DF(q_0) = \begin{pmatrix}0 & 1\\ -8 & 6\end{pmatrix}
$$

$$
\lambda = \{2,4\}
$$

$$
\mathbf{Q} = \begin{pmatrix}
-0.4472136 & -0.24253563\\
-0.89442719 & -0.9701425 
\end{pmatrix}
$$

$$
v_0 = 3
$$

### State $i=1$

$$
\lambda_1 = \{1/2, 5/2\}
$$

$$
\mathbf{Q} = \begin{pmatrix}
-0.89442719& -0.37139068 \\
-0.4472136 & -0.92847669
\end{pmatrix}
$$

$$
v_1 = 3/2
$$

$$
\dot s_1 = 1
$$

### State $i=2$

$$
DF(q_2) = \begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix}
$$

$$
\lambda_2 = (1,-1)
$$

$$
\mathbf{Q} = \frac{1}{\sqrt{2}}\begin{pmatrix}1 & -1 \\ 1 & 1\end{pmatrix}
$$

$$
v_2 = 0
$$

$$
\dot s_2 = 2
$$

```{=html}
<!-- ## Rarefaction -->
```
```{=html}
<!-- (8.22) -->
```
```{=html}
<!--
$$
\rho_{m}=\sqrt{\rho_{l} \rho_{r}} \exp \left(\frac{1}{2 a}\left(\frac{m_{l}}{\rho_{l}}-\frac{m_{r}}{\rho_{r}}\right)\right) .
$$

$$
=\rho_{m} m_{r} / \rho_{r}+a \sqrt{\rho_{m} / \rho_{r}}\left(\rho_{m}-\rho_{r}\right)
$$

-->
```
> Confirm that $\lambda_{01}>\dot s_1>\lambda_{11}$ and
> $\lambda_{12}>\dot s_2>\lambda_{22}$, which are Lax's entropy
> conditions for this system. Also confirm that $v_0>\dot s_1$,
> $v_1>\dot s_1$, $\dot s_2>v_1$ and $\dot s_2>v_2$, which means fluid
> particles move from the original states $q_0$ and $q_2$ to the
> auxiliary state $q_1$ as the shocks propagate through space and time.



# Problem 3 ($-\alpha u_{xx} + Au = f$)

> Write a 1d finite element code to solve the modified Poisson equation
> $$
> -\alpha u_{xx} + Au = f, \quad (0\le x\le 1), \qquad u(0)=0,\; u(1)=0,
> $$ where $\alpha>0$ and $A\ge0$. Use 4th order finite elments on a
> uniformly spaced grid,
>
> $$
> x_j = j/M, \qquad\quad 0\le j\le M
> $$
>
> where $M$ is divisible by 4 and the $r$th element includes nodes
> $x_{4r+i}$ for $0\le r<M/4$ and $0\le i\le 4$.

## Part A

Multiplying by a test function $v$ and integrating over the domain
(applying integration by parts) yields:

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

A fourth order isoparametric 1D element is developed by applying
Lagrange interpolation over 5 equally spaced sampling points.

![Shape
functions](../img/lagrange.png){style="margin:auto; display: block; max-width: 75%"}

### Convergence

> (a) Do a convergence study for $\alpha=1/100$, $A=0$ and
>     $f(x)=\frac{\pi^2}{100}\sum_{k=0}^4 \sin\big((2k+1)\pi x \big)$.

The exact integral for this problem is as follows:

$$
\frac{1}{\alpha 100} \sum{\frac{1}{(2k+1)^2}\sin{\left((2k+1)\pi x\right)} }
$$

![Source curve $f$ and exact solution
$u$](../img/p3a-exact.png){style="margin:auto; display: block; max-width: 75%"}

![Convergence study for finite element solution of steady-state
problem.](../img/p3a-conv.png){style="margin:auto; display: block; max-width: 75%"}



## Part B: Transient Analysis

> (b) Solve $u_t=\frac1{100}u_{xx}+f(x)\sin(\pi t)$ from $t=0$ to $t=1$
>     with initial condition $u(x,0)=0$ and the same $f$ as in part (a).
>     Use the 4th order implicit SDIRK timestepper with Butcher array
>     given in problem 2 of HW 2. Use your finite element code above to
>     solve the implicit equation for each stage of the timestepper.
>     (I'll explain this in class). Make a convergence plot for several
>     values of $M$ and one choice of $\nu=k/h$ that you find works
>     well.

The exact solution of the transient problem was derrived using the
`sympy` CAS library. A plot is shown below for various times.

![Analytic solution
curves](../img/p3b-exact.png){style="margin:auto; display: block; max-width: 75%"}

![FEM
solution](../img/p3b-fem-iso.png){style="margin:auto; display: block; max-width: 75%"}

### SDIRK Implementation

In HW2 a Runge-Kutta algorithm was implemented for problems with the
following form:

$$
\mathbf{u}_t + B\mathbf{u} = \mathbf{d}(t)
$$

Where $B$ is a linear operator . At stage $i$ of a diagonal Runge-Kutta
method one has

$$
\ell_{i}=F\left(t_{n}+c_{i} k, \vec{u}_{n}+k \sum_{j=1}^{i-1} a_{i j} \ell_{j}+k a_{i j} \ell_{i}\right)
$$

where $k=\Delta t$. For problems of the aforementioned form, this
simplifies to

$$
\left(I - k a_{i i} B\right) \ell_{i} = B \left(\vec{u}_{n}+k \sum_{j=1}^{i-1} a_{i j} \ell_{j}\right) + d(t_n+c_i k) 
$$

The following data is required to set up a particular scheme for
$\mathbf{u}\in \mathbb{R}^n$ with $s\in\mathbf{Z^+}$ stages:

$\mathcal{T}$
:   A Butcher tableau with zero entries above the diagonal.

$B, \mathbb{R}^n \rightarrow \mathbb{R}^n$: Discrete space operator

$\mathbf{d}, \mathbb{R} \rightarrow \mathbb{R}^n$
:   Source term.

The problem at hand is manipulated to fit the following form:

$$\vec{u}_{t}=-\frac{1}{100} {M}^{-1} A \vec{u}+\vec{f} \sin \pi t$$

so that

$$
\begin{gathered}
B=\frac{-1}{100}M^{-1}A \\
\mathbf{d}=M^{-1}b\sin{\pi t}
\end{gathered}
$$

where $A$, $M$, and $b$ are the stiffness, mass and load vectors as
readily produced by the implementation for Part B.

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

------------------------------------------------------------------------

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

```{=html}
<!-- where $M^{-1}A$ is a FE approximation to $-\Delta()$. -->
```
### Convergence

Convergence studies are presented below for time discretizations using
both the SDIRK scheme provided and the Crank-Nicolson scheme.

![Convergence
study.](../img/p3b-conv.png){style="margin:auto; display: block; max-width: 75%"}

![Convergence study for Crank-Nicolson
tableau.](../img/p3b-conv-cn.png){style="margin:auto; display: block; max-width: 75%"}



# Appendix

Key source code excerpts are provided below. The Python libraries
`elle`, `emme`, `anon` and `m228` which have been used throughout are
self written and available either from [PyPi.org](PyPi.org) via `pip` or
on Github.

## Source Code

### Fourth-order Lagrange element

``` {.python}
# external imports
import jax
# internal imports
import anon
import anon.atom as anp
from anon import quad

@anon.dual.generator(5)
def elem_0001(f=None,a1=1.0, a2=0.0,order=4):
    """
    Fourth order 1D Lagrange finite element with uniformly spaced nodes.
    
    Parameters
    ----------
    f: Callable
        element loading.
    a1: float
        Stiffness coefficient
    a2: float
        Mass coefficient
    """
    state = {}
    if f is None: f = lambda x: 0.0

    def transf(xi: float,x_nodes)->float:
        return ( x_nodes[0]*( + xi/6) 
               + x_nodes[1]*( - 4*xi/3) 
               + x_nodes[2]*( + 1) 
               + x_nodes[3]*( + 4*xi/3) 
               + x_nodes[4]*( - xi/6)
        )
    def grad_transf(xi,x_nodes):
        return abs(x_nodes[-1] - x_nodes[0])/2
    
    quad_points = quad.quad_points(n=order+1,rule="gauss-legendre")

    @jax.jit
    def jacx(u=None,y=None,state=None,xyz=None, a1=a1, a2=a2):
        x_nodes = anp.linspace(xyz[0][0],xyz[-1][0],5)
        grad = grad_transf(0,x_nodes)
        return a1*anp.array([
            [985/378, -3424/945, 508/315, -736/945, 347/1890],
            [-3424/945, 1664/189, -2368/315, 2944/945, -736/945],
            [508/315, -2368/315, 248/21, -2368/315, 508/315],
            [-736/945, 2944/945, -2368/315, 1664/189, -3424/945],
            [347/1890, -736/945, 508/315, -3424/945, 985/378],
        ]) / grad + a2*anp.array([
            [292/2835, 296/2835, -58/945, 8/405, -29/2835],
            [296/2835, 256/405, -128/945, 256/2835, 8/405],
            [-58/945, -128/945, 208/315, -128/945, -58/945],
            [8/405, 256/2835, -128/945, 256/405, 296/2835],
            [-29/2835, 8/405, -58/945, 296/2835, 292/2835],
        ])*grad


    @jax.jit
    def main(u,_,state,xyz,a1=a1,a2=a2):
        x_nodes = anp.linspace(xyz[0][0],xyz[-1][0],5)
        external_term = sum(
              anp.array([
                [f(transf(xi,x_nodes))*(2*xi**4/3 - 2*xi**3/3 - xi**2/6 + xi/6)],
                [f(transf(xi,x_nodes))*(-8*xi**4/3 + 4*xi**3/3 + 8*xi**2/3 - 4*xi/3)],
                [f(transf(xi,x_nodes))*(4*xi**4 - 5*xi**2 + 1)],
                [f(transf(xi,x_nodes))*(-8*xi**4/3 - 4*xi**3/3 + 8*xi**2/3 + 4*xi/3)],
                [f(transf(xi,x_nodes))*(2*xi**4/3 + 2*xi**3/3 - xi**2/6 - xi/6)],
              ]
            )*weight * grad_transf(xi,x_nodes) for xi, weight in zip(*quad_points)
        )
        resp = jacx(u,_,state,xyz,a1=a1,a2=a2)@u + external_term
        return u, resp, state
    return locals()
```



### Analytic Transient Solution

``` {.python}
pi = anp.pi
sin = anp.sin
cos = anp.cos
exp = anp.exp
def cn(t):
    return [
        pi**2*(pi*alpha*sin(pi*t)/(pi**3*alpha**2 + pi) 
            - cos(pi*t)/(pi**3*alpha**2 + pi))/100 
            + pi**2/(100*(pi**3*alpha**2*exp(pi**2*alpha*t) 
            + pi*exp(pi**2*alpha*t))), 
        pi**2*(9*pi*alpha*sin(pi*t)/(81*pi**3*alpha**2 + pi) 
            - cos(pi*t)/(81*pi**3*alpha**2 + pi))/100
            + pi**2/(100*(81*pi**3*alpha**2*exp(9*pi**2*alpha*t) 
            + pi*exp(9*pi**2*alpha*t))), 
        pi**2*(25*pi*alpha*sin(pi*t)/(625*pi**3*alpha**2 + pi) 
            - cos(pi*t)/(625*pi**3*alpha**2 + pi))/100 
            + pi**2/(100*(625*pi**3*alpha**2*exp(25*pi**2*alpha*t) 
            + pi*exp(25*pi**2*alpha*t))), 
        pi**2*(49*pi*alpha*sin(pi*t)/(2401*pi**3*alpha**2 + pi) 
            - cos(pi*t)/(2401*pi**3*alpha**2 + pi))/100 
            + pi**2/(100*(2401*pi**3*alpha**2*exp(49*pi**2*alpha*t) 
            + pi*exp(49*pi**2*alpha*t))), 
        pi**2*(81*pi*alpha*sin(pi*t)/(6561*pi**3*alpha**2 + pi) 
            - cos(pi*t)/(6561*pi**3*alpha**2 + pi))/100 
            + pi**2/(100*(6561*pi**3*alpha**2*exp(81*pi**2*alpha*t) 
            + pi*exp(81*pi**2*alpha*t)))
     ]

def u(x,t):
    c = cn(t)
    return sum( 
        c[n] * anp.sin(xi*x)
            for n,xi in enumerate([(2*k+1)*anp.pi for k in range(5)])
    ) 
```
