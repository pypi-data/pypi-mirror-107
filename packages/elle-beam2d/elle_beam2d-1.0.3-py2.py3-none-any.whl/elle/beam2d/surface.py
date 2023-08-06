"""Limit surface wrappers for 2D beam elements.
"""
import jax
# import anabel as ana
import anon
import anon.atom as anp
# import anabel.ops as anp

from anon.dual import generator


@generator(3,statevar="initial_state")
def surf_no1(local, Mp, Hi=None, Hk=None, HngOff=None,
        w=None, tol=1e-12, **kwds):
    """Basic elastoplastic frame limit surface [@ngoc2017damage, chp. 3.1].

    > Note: The formulation of this element is not endorsed.

    Forked from `elle.beam2dseries.no_7`. Uses general element response function,
    `resp` instead of constant elastic stiffness matrix,`ke`.

    Parameters
    ----------
    local: Callable
        Local element response function, generally of type $f: v \\rightarrow q$.
    Mp: list/float
        Plastic moment capacity

    Effect of `HngOff` parameter (see study [stdy-0007](/stdy/stdy-0007)):

    <div style="display:flex;flex:1 1 auto;">
    <iframe 
    scrolling="no"
    seamless="seamless"
    src="/stdy/stdy-0007/src/main.html" 
    style="border:none;display:block;flex-direction:column;" 
    height="500" width="90%"></iframe>
    </div>

    References
    ----------
    :::{#refs}
    :::
    
    -------------------
    Claudio Perez

    2020-12-30
    """
    initial_state = dict(
        vp=anp.zeros((3,1)),
        alpha=anp.zeros((2,1)),
        qbk=anp.zeros((2,1))
    )
    initial_state.update({...: local.origin.state})

    if Hi is None: Hi = anp.zeros((2,1))
    if Hk is None:
        Hk = anp.zeros((2,2))
    elif len(Hk) < 4:
        Hk = anp.diag(Hk.flatten())
    if w  is None: w  = anp.zeros((2,1))

    if HngOff is None:
        HngOff = anp.zeros(2)

    bh = anp.array([[  HngOff[0]-1,     HngOff[0] ],
                    [ -HngOff[1]  ,   1-HngOff[1] ]])


    _ke_ = anon.diff.jacx(local)
    vb0 = anp.zeros((2,1))
    Mhw = anp.zeros((2,1))

    def scalar_beta(kb,i,N,Y):
        i = i.flatten()
        nha = bh.T@N[:,i]
        kpDen = nha.T@(kb + Hk)@nha + Hi[i]
        Dgam = (Y[i]*Mp[i]) / kpDen[i,i]
        return Dgam

    @jax.jit
    def scalar_update(kb,nha:float,Dgam:float,qtr,vp,alpha,qbk):
        qb_n = qtr - kb@nha*Dgam
        vp_n = vp + nha*Dgam
        alpha_n = alpha + Dgam
        qbk_n = qbk + Hk@nha*Dgam
        return qb_n,vp_n,alpha_n,qbk_n

    @jax.jit
    def vector_beta(kb,N,Y):
        Nha   = bh.T@N                                 # account for hinge offset
        kpDen = Nha.T@(kb+Hk)@Nha + anp.diag(Hi.flatten())   # plastic modulus denominator
        Dgam  = anp.linalg.solve(kpDen,Y*Mp)   # plastic flow
        return Dgam

    @jax.jit
    def vector_update(kb,N,Dgam,qtr,vp,alpha,qbk):
        Nha = bh.T@N
        qb_n = qtr - kb@Nha@Dgam
        vp_n = vp + Nha@Dgam
        alpha_n = alpha + Dgam
        qbk_n = qbk + Hk@Nha@Dgam
        return qb_n,vp_n,alpha_n,qbk_n
    
    def main(v, q=anp.zeros((3,1)), state=initial_state,
          Hi=Hi, Hk=Hk, w=anp.zeros((2,1)), params={}, **env):
        """
        element state determination: determine resisting force for v
        """
        # print(f"inel: {state}\n")
        vp, alpha, qbk = (state[k] for k in ["vp", "alpha", "qbk"])

        vb =  v[1:]
        vp = vp[1:]
        ke = _ke_(v, q, state[...], **params, **env)
        kb = ke[1:,1:]
        qa = ke[0,0] * v[0]
        ve = vb - vb0 - vp
        # trial elastic step
        qtr  = kb@ve    
        # trial flexural basic forces
        Mtr  = bh@qtr + Mhw
        xi_trial = Mtr - bh@qbk
        n = anp.sign(xi_trial)
        N = anp.diag(n.flatten())
        YFtr = (N.T@xi_trial)/Mp - ( 1 + anp.diag((Hi/Mp).flatten())@alpha)    # trial value of yield function
        j_act = YFtr > tol

        # check location of trial force relative to yield surface
        if not anp.any(j_act):
            # trial state is admissible (falls inside the yield surface)
            vp_n = anp.concatenate((anp.zeros((1,1)),vp))
            q_n  = anp.concatenate((qa[:,None],qtr))
            state = {"vp":vp_n, "alpha":alpha, "qbk":qbk, ...: state[...]}
            return v, q_n, state

        elif anp.all(j_act):
            Dgam = vector_beta(kb,N,YFtr)
            # check number of active yield surfaces
            if  anp.product(Dgam.flatten()) < 0.:
                i = Dgam > 0.
                Dgam = scalar_beta(kb,i,N,YFtr)
                nha = bh.T@N[:,i.flatten()]
                qb,vp_n,alpha_n,qbk_n = scalar_update(kb,nha,Dgam,qtr,vp,alpha,qbk)
            else:
                qb,vp_n,alpha_n,qbk_n = vector_update(kb,N,Dgam,qtr,vp,alpha,qbk)
        else:
            Dgam = scalar_beta(kb,j_act,N,YFtr)
            nha = bh.T@N[:,j_act.flatten()]
            qb,vp_n,alpha_n,qbk_n = scalar_update(kb,nha,Dgam,qtr,vp,alpha,qbk)

        ## check for Region C
        Mh  = bh@qb + Mhw
        Mbk = bh@qbk_n
        xi  = Mh - Mbk

        Nn = anp.diag(anp.sign(xi).flatten())
        yfn = (Nn.T@(Mh-Mbk))/Mp - (1 + anp.diag((Hi/Mp).flatten())@alpha)    # trial value of yield function
        if anp.any(yfn > tol):
            print("BRANCH UNTESTED")
            # last state falls in region C and needs to be revised
            Nh    = bh.T@N                                    # hinge offset effect
            kpDen = Nh.T@(kb+Hk)@Nh + anp.diag(Hi.flatten())  # plastic modulus denominator
            Dgam  = anp.linalg.solve(kpDen,YFtr*Mp)           # plastic flow
            qb    = qtr - kb@Nh@Dgam
            # update plastic deformation, hardening variable and back force vectors
            vp_n    = vp + Nh@Dgam
            alpha_n = alpha + Dgam
            qbk_n   = qbk   + Hk@Nh@Dgam

        ## set up element stiffness and basic forces
        vp_n = anp.concatenate((anp.zeros((1,1)),vp_n))
        q_n  = anp.concatenate((qa[:,None],qb))

        state = {"vp":vp_n, "alpha":alpha_n, "qbk":qbk_n, ...: state[...]}
        # print(f"\n\nend inel: {state}\n")
        return v, q_n, state

    return locals()

