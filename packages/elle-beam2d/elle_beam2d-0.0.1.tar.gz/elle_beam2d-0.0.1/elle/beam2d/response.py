r"""Displacement-based beam element models

($f: v \rightarrow q$)

#### Common Parameters

$E$ (`E`): `float`
:   Elastic modulus.

$A$ (`A`): `float`
:   Cross-sectional area.

$I$ (`I`): `float`
:   Cross-sectional moment of inertia.

"""


import warnings
from functools import partial

import anon
import anon.atom as anp
from anabel.template import template
#from anon.dual import template
from anon.quad import quad_points

template = template
# import anabel.ops as anp
import elle.numeric
array = anp.array

__all__ = ["resp_no1", "resp_no2", "resp_no3", "resp_no4", "resp_no6"]

# Configure warnings so that convergence 
# messages are always thrown.
warnings.simplefilter('always', UserWarning)

def fix(f, state=None, tol=1e-9, maxiter: int =20, norm=anp.linalg.norm):
    state = {...: state}
    def g(x, y, state=state, **params):
        _, yi, localstate = f(x, y, state[...], **params)
        for i in range(maxiter):
            _, y, localstate = f(x, yi, localstate, **params)

            if norm(y - yi) < tol:
                return x, y, {...: localstate}
            yi = y
        warnings.warn("Iterations failed to converge.")
        return x, y, state
    return g, state

#------------------------------------------------------------------------------------
def fixed_point_no2(f,state, maxiter=10, tol=1e-8, norm=anp.linalg.norm):
    """
    created 2020-12-31
    """
    @jax.jit
    def cond_fun(carry):
        y_prev, y = carry
        return norm(y_prev - y) > tol
    

    # @partial(jax.custom_vjp, nondiff_argnums=(2,))
    # @jax.custom_vjp
    def fixpnt(x, y_guess, state=state, **params):
        _, y_initial, localstate = f(x,y_guess,state[...],**params)
        def body_fun(carry):
            _, y = carry
            return y, f(x,y,localstate,**params)[1]

        _, y_star = jax.lax.while_loop(cond_fun, body_fun, (y_guess, y_initial))
        return x, y_star, state


    def fixed_point_fwd(f, a, x_init):
        x_star = fixpnt(f, a, x_init)
        return x_star, (a, x_star)

    def fixed_point_rev(f, res, x_star_bar):
        a, x_star = res
        _, vjp_a = jax.vjp(lambda a: f(a, x_star), a)
        a_bar, = vjp_a(fixpnt(partial(rev_iter, f),
                                    (a, x_star, x_star_bar),
                                    x_star_bar))
        return a_bar, jnp.zeros_like(x_star)
    
    def rev_iter(f, packed, u):
        a, x_star, x_star_bar = packed
        _, vjp_x = jax.vjp(lambda x: f(a, x), x_star)
        return x_star_bar + vjp_x(u)[0]

    # fixed_point.defvjp(fixed_point_fwd, fixed_point_rev)
    return fixpnt, state
#------------------------------------------------------------------------------------


@template(3)
def resp_no1(
    q0: array = None,
    E:  float = None,
    A:  float = None,
    I:  float = None,
    L:  float = None, **kwds):
    r"""Construct a 1st order beam element.

    $$
    v \mapsto \mathbf{k}v


    \mathbf{k}=\frac{E}{L}\left[
        \begin{array}{lll}
        A &  0 &  0 \\\\
        0 & 4I & 2I \\\\
        0 & 2I & 4I
        \end{array}\right]
    $$

    created: 2020-12-23
    """
    if q0 is None: q0 = anp.zeros((3,1))
    v0 = anp.zeros((3,1))
    # state = {"y": q0, "x": v0}
    state = {}
    def jacx(v, q=q0,state=state,E=E,A=A,I=I,L=L,**env):
        C0 = E*I/L
        C1 = 4.0*C0
        C2 = 2.0*C0
        k = anp.array([[E*A/L,0.0,0.0],[0.0,C1,C2],[0.0,C2,C1]])
        return k

    def main(v, q=q0,state=state,E=E,A=A,I=I,L=L,**env):
        C0 = E*I/L
        C1 = 4.0*C0
        C2 = 2.0*C0
        k = anp.array([[E*A/L,0.0,0.0],[0.0,C1,C2],[0.0,C2,C1]])
        return v, k@v, state
    return locals()

@template(3,"state")
def resp_no2(
    q0=None,
    E:   float = None,
    A:   float = None,
    I:   float = None,
    L:   float = None,
    tol: float = 1e-6,
    jit: bool  = False,
    **kwds):
    """
    2nd order beam element.

    created: 2020-12-23
    """
    if q0 is None: q0 = anp.zeros((3,1))
    state = {"q": q0}

    def jac_x(v, q=q0, state=state, L:float=L, E:float=E, A:float=A, I:float=I):
        EI = E*I
        c = q.squeeze()[0].astype(float)*L**2/(EI)
        C1 = EI/L*(4.0+2/15*c)
        C2 = EI/L*(2.0-1/30*c)
        #C3 = E*I/L*(3.0+1/5*c)
        k = anp.array([[E*A/L,0.0,0.0], [0.0,C1,C2], [0.0,C2,C1]])
        return v, k, state
    
    def beam_no2(v, q=q0, state=state, L:float=L, E:float=E, A:float=A, I:float=I):
        EI = E*I
        c = q.squeeze()[0].astype(float)*L**2/(EI)
        C1 = EI/L*(4.0+2/15*c)
        C2 = EI/L*(2.0-1/30*c)
        #C3 = E*I/L*(3.0+1/5*c)
        k = anp.array([[E*A/L,0.0,0.0], [0.0,C1,C2], [0.0,C2,C1]])
        return v, k@v, state

    main, state = fix(beam_no2,state)
    return locals()


def resp_no3(q0=None, 
    E=None, A=None, I=None, L=None, 
    tol=1e-2, maxiter=10, **kwds):
    """Exact beam element.
    
    created: 2020-12-23
    """
    state = {...: None}
    if q0 is None: q0 = anp.zeros((3,1))
    def f(v, q=q0, state=state, E:float=E, A:float=A, I:float=I, L:float=L, **env):
        psi = anp.sqrt(abs(q[0].squeeze().astype(float)-0.001)/E*I)*L
        C1 = E*I/L*psi*(anp.sin(psi)-psi*anp.cos(psi))/(2-2*anp.cos(psi)-psi*anp.sin(psi))
        C2 = E*I/L*psi*(1-anp.sin(psi))/(2-2*anp.cos(psi)-psi*anp.sin(psi))
        #C3 = psi**2*anp.sin(psi)/(anp.sin(psi)-psi*anp.cos(psi))
        k = anp.array([[E*A/L,0.0,0.0], [0.0,C1,C2], [0.0,C2,C1]])
        return v, k@v, state

    return fix(f, maxiter=maxiter, tol=tol), state

try:
    import elle.solvers
except:
    pass

@template(3)
def resp_no4(v0=None, E:float=None, A:float=None, I:float=None, L:float=None,
    wx=0.0, wy=0.0, k0=0.0, e0=0.0, DL=0.0,tol=1e-9,maxiter=10,**kwds):
    """Linear flexibility element.

    Parameters
    ----------
    v0: array_like
        initial deformation vector


    created 2020-12-27
    """
    state = {...:None}
    if v0 is None: v0 = anp.zeros((3,1))

    # @anabel.jit
    def resp(q, v=v0, state=state, 
             wy=wy, wx=wx, e0=e0, k0=k0, DL=DL, E=E, A=A, I=I, L=L, **env):
        v0 = anp.array([
            [   e0*L + DL   ],
            [-k0/2*L - wy*L**3/(24*E*I)],
            [ k0/2*L + wy*L**3/(24*E*I)]
        ])
        EI = E*I
        f = anp.array([
            [L/(E*A),      0.0,        0.0],
            [   0.0, L/(3*EI), -L/(6*EI)],
            [   0.0,-L/(6*EI),  L/(3*EI)]])
        return q, f@q + v0, state

    return elle.solvers.inverse(resp,maxiter=maxiter,tol=tol), state


@template(3,"state")
def resp_no5(
    q0 = None, 
    E: float = None, 
    A: float = None, 
    I: float = None, 
    L: float = None, 
    hinge:int = 0,
**kwds):
    r"""Construct a 1st order beam element with a hinge release.
    $$
    f: q \rightarrow v \\\\
       q \mapsto \mathbf{k}q
    $$
    
    $$
    \mathbf{k}=\frac{E}{L}\left[
        \begin{array}{lll}
        A &  0 &  0 \\\\
        0 & 3I &  0 \\\\
        0 &  0 &  0
        \end{array}\right] 
    $$

    created: 2020-12-23
    """
    if q0 is None: q0 = anp.zeros((3,1))
    v0 = anp.zeros((3,1))
    # state = {"y": q0, "x": v0}
    offsets = 3.0*anp.array([float(hinge), float(not hinge)])
    state = {}
    # @anabel.jit
    def main(v, q=q0,state=state,E=E,A=A,I=I,L=L,**env):
        C1, C2 = I*offsets
        k = E/L*anp.array([[A,0.0,0.0],[0.0,C1,0.0],[0.0,0.0,C2]])
        return v, k@v, state
    return locals()

@template(3)
def resp_no6(
    *sections,
    q0: array = None,
    E:  float = None,
    L:  float = None,
    quad = None,
    **kwds):
    r"""Displacement-based fiber beam.

    Parameters
    ----------
    quad: 


    created: 2021-03-30
    """
    if q0 is None: q0 = anp.zeros((3,1))
    v0 = anp.zeros((3,1))
    state = [s.origin[2] for s in sections]
    params = {...: [anon.dual.get_unspecified_parameters(s) for s in sections]}
    locs, weights = quad_points(**quad)
    def _B(xi,L):
        x = L/2.0*(1.0+xi)
        return anp.array([[1/L,0.,0.],[0.0,(6*x/L-4)/L, (6*x/L-2)/L]])

    def main(v, q=q0,state=state,E=E,L=L,params=params):
        B = [_B(xi,L) for xi in locs]
        S = [s(b@v,None,state=state[i],**params[...][i]) for i,(b,s) in enumerate(zip(B,sections))]
        q = sum(
            L/2.0*w*b.T @ s[1] for b,w,s in zip(B,weights,S)
        )
        state = [s[2] for s in S]
        return v, q, state

    return locals()



@template(3)
def resp_nox(
    q0: array = None,
    E:  float = None,
    A:  float = None,
    I:  float = None,
    L:  float = None,
    **kwds
):
    if q0 is None: q0 = anp.zeros((3,1))
    v0 = anp.zeros((3,1))
    state = {}

    def main(v, q=q0,state=state,E=E,A=A,I=I,L=L,**env):
        C0 = E*I/L
        C1 = 4.0*C0
        C2 = 2.0*C0
        k = anp.array([[E*A/L,0.0,0.0],[0.0,C1,C2],[0.0,C2,C1]])
        return v, k@v, state

    return locals()

