# Copyright 2020 Claudio Perez
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     https://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Geometric transformations of 2D beam elements.
"""
try:
    import jax
except:
    pass
from anon.dual import generator
import anon
import anon.atom as anp

def transform(base_transf,_jit=True):
    @generator(6,_jit=_jit)
    def geom(local,  xyz=None):
        state = {...: local.origin.state, "q": anp.zeros((3,1))}
        transf = base_transf(xyz)
        transf_grad = anon.diff.jacfwd(transf, 1, 0)

        if xyz is None:
            def main(u, p, state=state, xyz=xyz, params={}, **env):
                _, v, L = transf(u, None, xyz)
                v, q, localstate = local(v, state["q"], state[...], **env, L=L,  **params)
                p = transf_grad(u, None, xyz).T @ q
                state = {"q": q, ...: localstate}
                return u, p, state
        else:
            def main(u, p, state=state, params={}, **env):
                _, v, L = transf(u, None)
                _, q, localstate = local(v, state["q"], state[...], **env, L=L,  **params)
                p = transf_grad(u, None).T @ q
                state = {"q": q, ...: localstate}
                return u, p, state
        return locals()
    return geom

def transform_no2(base_transf,_jit=True):
    """
    Claudio Perez 2021-04-01
    """
    @generator(6,_jit=_jit)
    def geom(local,  xyz=None):
        params = anon.dual.get_unspecified_parameters(local,recurse=False)
        if "L" in params: params.pop("L")
        #params = { "iargs": anon.dual.get_unspecified_parameters(local,recurse=False) }
        #params["iargs"].pop("L")
        state = {"state": local.origin.state, "q": anp.zeros((3,1))}
        transf = base_transf(xyz)
        transf_grad = anon.diff.jacfwd(transf, 1, 0)
        _p0 = anp.zeros((6,1))
        I = anp.eye(2)
        o = anp.zeros((1,2))
        O = anp.zeros((6,1))
        II = anp.block([[I,-I],[-I,I]])

        _k_ = anon.diff.jacx(local)
        if xyz is None:
            def truss_geometric_stiffness(L,i_d):
                idid = (I-i_d@i_d.T)
                kga = anp.concatenate([idid,o,-idid,o])
                return anp.concatenate([kga,O,-kga,O],axis=-1)

            def beam_geometric_stiffness(L,i_d,n_d):
                idnd = ( i_d@n_d.T + n_d@i_d.T )
                kgb = anp.concatenate([idnd,o,-idnd,o])
                return anp.concatenate([kgb,O,-kgb,O],axis=-1)/(L**2)

            def jacx(u, p, state=state, xyz=xyz, params=params):
                q = state["q"].flatten()
                _, ag, L = transf(u, None, xyz)
                i_d = ag[0,3:5][:,None]
                n_d = L*ag[1,:2][:,None]
                kga = q[0]/L*truss_geometric_stiffness(L,i_d)
                kgb = sum(q[1:])*beam_geometric_stiffness(L,i_d,n_d)
                k = _k_(ag@u, state["q"], state["state"], L=L, **params)
                return ag.T @ k @ ag + kga + kgb


            def main(u, p=_p0, state=state, xyz=xyz, params=params):
                _, ag, L = transf(u, None, xyz)
                #print(f"u: {u}, \nag: {ag}, \nv: {ag@u}")
                v, q, localstate = local(ag@u, state["q"], state["state"], L=L, **params)
                p = ag.T @ q
                state = {"q": q, "state": localstate}
                return u, p, state
        else:
            def main(u, p=_p0, state=state, params=params, **env):
                _, ag, L = transf(u, None)
                _, q, localstate = local(ag@u, state["q"], state["state"], **env, L=L,  **params)
                p = ag.T @ q
                state = {"q": q, "state": localstate}
                return u, p, state
        return locals()
    return geom


def geom_no1(xyz=None):

    def _ag(DX,DY,Ln):
        return anp.array([
            [- DX ,    -DY,  0.0,  DX,    DY,   0.0],
            [-DY/Ln,  DX/Ln, Ln,  DY/Ln,-DX/Ln, 0.0],
            [-DY/Ln,  DX/Ln, 0.0, DY/Ln,-DX/Ln,  Ln]])/Ln

    if xyz is None:
        def f(u, v, xyz):
            DX = xyz[1,0] - xyz[0,0]
            DY = xyz[1,1] - xyz[0,1]
            Ln = anp.linalg.norm([DX,DY])
            ag = _ag(DX,DY,Ln)
            return u, ag, Ln

    else:
        DX = xyz[1,0] - xyz[0,0]
        DY = xyz[1,1] - xyz[0,1]
        Ln = anp.linalg.norm([DX,DY])
        ag = _ag(DX,DY,Ln)
        def f(u, v=None):
            return u, ag, Ln

    return f


# @geometric_transform
def geom_no2(xyz=None):
    """
    Corotational beam transformation
    """
    if xyz is None:
        def f(u, v, xyz):
            DX = xyz[1,0] - xyz[0,0]
            DY = xyz[1,1] - xyz[0,1]
            L = anp.linalg.norm([DX,DY])
            transf = anp.array([
                [ DX , DY ],
                [-DY , DX ]])/L

            du = u[:3] - u[3:]
            dux, duy = du[:2].flatten()
            #dux, duy = map(float, du[:2].squeeze())
            dw = (transf @ du[:2]).flatten()
            Ln = anp.sqrt((L + dw[0])**2 + dw[1]**2)
            #i_d = anp.array([[(DX+dux)/Ln, (DY+duy)/Ln]])
            #n_d = anp.array([[(-DY+duy)/Ln], [(DX+dux)/Ln)]])
            ag = anp.array([
                [- DX-dux,       -DY-duy,    0.0,  DX+dux,    DY + duy, 0.0],
                [-(DY-duy)/Ln,  (DX+dux)/Ln, Ln, (DY+duy)/Ln, -(DX+dux)/Ln, 0.0],
                [-(DY-duy)/Ln,  (DX+dux)/Ln, 0.0, (DY+duy)/Ln, -(DX+dux)/Ln, Ln],
            ])/Ln
            return u, ag, Ln

    else:
        DX = xyz[1,0] - xyz[0,0]
        DY = xyz[1,1] - xyz[0,1]
        L = anp.linalg.norm([DX,DY])
        transf = anp.array([
            [ DX , DY ],
            [-DY , DX ]])/L
        # print(DX)
        def f(u, v):
            du = u[:3] - u[3:]
            dux, duy = du[:2].flatten()
            dw = transf @ du[:2]
            Ln = anp.sqrt((L + dw[0])**2 + dw[1]**2).squeeze()#.astype(float)
            ag = anp.array([
                [- DX-dux,       -DY-duy,    0.0,  DX+dux,         DY + duy, 0.0],
                [-(DY-duy)/Ln,  (DX+dux)/Ln,  Ln, (DY+duy)/Ln, -(DX+dux)/Ln, 0.0],
                [-(DY-duy)/Ln,  (DX+dux)/Ln, 0.0, (DY+duy)/Ln, -(DX+dux)/Ln,  Ln],
            ])/Ln
            return u, ag, Ln
    return f




