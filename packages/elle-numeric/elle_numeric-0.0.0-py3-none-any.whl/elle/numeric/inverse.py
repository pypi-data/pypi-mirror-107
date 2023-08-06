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
"""Numerical function inversion
"""


import warnings
from collections import defaultdict
from functools import partial
from typing import Callable

from anon import dual
import anon
# import anabel.ops as anp
import anon.atom as anp

warnings.simplefilter('always', UserWarning)

@dual.generator(dim="shape",main="accumulate_main")
def accumulate(f):
    import jax
    origin = f.origin

    state = {...: origin.state}
    shape = f.shape

    def accumulate_main(x, y=origin[1], state=state, params={}, **env):
        localstate = state[...]
        Y = anp.zeros(x.shape)
        localstates = []
        n = len(x)
        for i,p in enumerate(x):
            print(f"{i}/{n}")
            _x, y, localstate = f(p, y,  localstate, **env, **params)
            Y = jax.ops.index_update(Y,jax.ops.index[i,...],y)
            localstates.append(localstate)
        return _x, Y, {...:localstates}

    return locals()


@dual.generator(dim="shape",main="walk_main")
def walk(f):
    origin = f.origin

    state = {...: origin.state}
    shape = f.shape

    def walk_main(x, y=origin[1], state=state, params={}, **env):
        localstate = state[...]
        for i,p in enumerate(x):
            _x, y, localstate = f(p, y,  localstate, **env, **params)
        return _x, y, {...:localstate}

    return locals()


    
@dual.generator(dim="shape")
def inv_no1(f,df=None, nr=None, norm=anp.linalg.norm,
    jacx=None,
    origin=None,shape=None,
    maxiter=10,tol=1e-10, jit=False
)->Callable:
    """
    Parameters
    ----------
    f: Callable
        Function to invert.
        `f(x, y0, state=f.state,params={},**kwds)->(x, y, state)`{.python .hljs}

    nr: int, default=None
        Defines indices of fixed function outputs

    norm: Callable, default = `anon.atom.linalg.norm`
        Function defining norm.

    Returns
    -------
    f_inv: Callable
        `f_inv(y, x0, state=f.state, params={}, **kwds)->(y, x, state)`{.python .hljs}

    Studies
    -------
    elle-0007

    ---------------------------------
    Claudio Perez
    2020-12-30
    """
    if origin is None:
        origin = f.origin

    state = {...: origin.state}

    if df is None and jacx is None:
        df = anon.diff.jacfwd(f, 1, 0)
    else:
        df = jacx
    if nr is not None:
        nr = -nr

        def main(x, y, state=state, params={},**env):
            """y is taken as initial guess"""
            y , xn, localstate = f(y, x, state[...], **env, **params)
            dx = x - xn
            for _ in range(maxiter):
                if norm(dx) < tol:
                    return x, y, state
                df_i = df(y, x, localstate, **env, **params)[:nr,:nr]
                dy = anp.linalg.solve(df_i, dx[:nr])
                dy = anp.pad(dy, ((0,-nr), (0, 0)), 'constant')
                y  = y + dy
                y , xn, localstate =   f(y, x, localstate, **env, **params)
                dx = x - xn

            warnings.warn(f"Failed to converge on function {f} inversion.")

            return x, y, {...:localstate}
    else:

        def main(x, y, state=state, params={}, **env):
            """
            Used by: elle-0007, w/ beam2d.resp_no4
            y is initial guess
            """
            y , xi, localstate = f(y, x, state[...], **env,**params)
            dx = x - xi
            for i in range(maxiter):
                if norm(dx) < tol:
                    return x, y, {...:localstate}
                df_i = df(y, x, localstate, **env, **params)
                dy = anp.linalg.solve(df_i, dx)
                y  = y + dy
                y, xi, localstate = f(y, x, state[...], **env, **params)
                dx = x - xi

            warnings.warn("Function inversion failed to converge.")
            
            return x, y, {...:localstate}

    if shape is None: shape = reversed(f.shape)
    return locals()


