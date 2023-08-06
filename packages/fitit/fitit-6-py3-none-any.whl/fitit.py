# fitit.py
#
#
# changelog:
#   5: added support for simultaneous fits
#   6: added bounds support with least_squares
VERSION = 6

from scipy import optimize

import numpy as np
from numpy import ravel, asarray, asanyarray

from scipy.linalg import svd


# utility class to keep track of fitting parameters.  Can both accept a ndarray 
# and convert to named parameters and generate a ndarray for use with leastsq.
class Params(object):
    def __init__(self, params="", like=None, vals=[], fitvals=[], fiterrs=[], fitinfo=None):
        self.errors = {}
        self.fitinfo = fitinfo
        if like is not None:
            # copy params from reference Params object
            self.params = like.params[:]
            self.tofit  = like.tofit[:]
            for p in self.params:
                self.__setattr__(p, like.__getattribute__(p))
        else:
            # parse params string for parameters
            ps = params.split()
            self.params = [p.replace('*', '') for p in ps]
            self.tofit = [p.find('*') == -1 for p in ps]
            for p in self.params:
                self.__setattr__(p, 1)

        if len(vals) > 0:
            self.set_vals(vals)
        if len(fitvals) > 0:
            self.set_fitvals(fitvals)
        if len(fiterrs) > 0:
            self.set_fiterrs(fiterrs)
        else:
            self.has_errors = False

    
    def keys(self):
        return " ".join(self.params)

    def fitparams(self):
        return [p for p, t in zip(self.params, self.tofit) if t]
            
    def fitvals(self):
        return [self.__getattribute__(p) for p in self.fitparams()]

    def set_fitvals(self, vals):
        for p, v in zip(self.fitparams(), vals):
            self.__setattr__(p, v)

    def set_fiterrs(self, vals):
        for p, v in zip(self.fitparams(), vals):
            self.errors[p] = v
            # self.__setattr__(p + 'e', v)

    def set_vals(self, args):
        for p, v in zip(self.params, args):
            self.__setattr__(p, v)
        self.has_errors = True

    def __repr__(self):
        padding = max([len(p) for p in self.params]) + 1
        instr = "%" + str(padding) + "s: %g"
        return "\n".join(
            [instr % (p, self.__getattribute__(p)) for p in self.params])


    def with_const(self, **kwargs):
        # create a copy of the params with each keyword to with set as constants.
        p = Params(like=self)
        for k, v in kwargs.items():
            p.tofit[p.params.index(k)] = False
            p.__setattr__(k, v)
        return p

    def with_(self, **kwargs):
        # create a copy with keywards changed. Don't modify whats constant.
        p = Params(like=self)
        for k, v in kwargs.items():
            p.__setattr__(k, v)
        return p


def fit(func, x, y, p0, sigma=1., bounds=None, method=None, fitinfo=False, fillbaderrs=None, **kwargs):
    if not isinstance(p0, Params):
        msg = "expected p0 to be a Params object"
        raise TypeError(msg)

    # convert x and y in case they are lists / tuples
    y = asanyarray(y)
    x = asanyarray(x)

    def residual(params):
        p = Params(like=p0, fitvals=params)
        f = func(x, p)
        if isinstance(f, (list, tuple)):
            # `func` should return same shape as y.
            # convert from list for convenience.
            f = asarray(f)

        # flatten residuals so simultaneus fits work
        return ravel(abs(f - y) / sigma)

    if method is None:
        if bounds is None:
            method = 'lm'
        else:
            method = 'trf'

    if bounds:
        lb = bounds[0].fitvals()
        ub = bounds[1].fitvals()
        bounds = (lb, ub)
        



    if method == 'lm':
        # use leastsq for fitting
        # taken from scipy's curve_fit
        r = optimize.leastsq(residual, p0.fitvals(), full_output=True)
        popt, pcov, info, errmsg, ier = r

        if ier not in [1, 2, 3, 4]:
            print("Warning, optimal parameters not found: " + errmsg)
            #raise RuntimeError(msg)
    else:
        # user least_squares for fitting
        # taken from scipy's curve_fit (Oct 2018)

        if 'max_nfev' not in kwargs:
            kwargs['max_nfev'] = kwargs.pop('maxfev', None)

        if bounds is None:
            bounds = (-np.inf, np.inf)

        r = res = optimize.least_squares(residual, p0.fitvals(), bounds=bounds, 
                method=method, **kwargs)
        
        if not res.success:
            raise RuntimeError("Optimal parameters not found: " + res.message)

        popt = res.x
        errmsg = res.message

        _, s, VT = svd(res.jac, full_matrices=False)
        threshold = np.finfo(float).eps * max(res.jac.shape) * s[0]
        s = s[s > threshold]
        VT = VT[:s.size]
        pcov = np.dot(VT.T / s**2, VT)

        if fitinfo:
            print("fitinfo unsupported with this method")
            fitinfo = False

    # count x, not y (like curve_fit) so simultaneus fits work.
    if (len(x) > len(p0.fitparams())) and pcov is not None:
        s_sq = (residual(popt)**2).sum()/(len(x)-len(p0.fitparams()))
        pcov = pcov * s_sq
        # diagonal should be variance
        errs = pcov.diagonal()**0.5
    else:
        print("could not determine fit errors:\n%s" % errmsg)
        if fillbaderrs is None:
            errs = []
        else:
            errs = [fillbaderrs] * len(p0.fitparams())

    if fitinfo:
        return Params(like=p0, fitvals=popt, fiterrs=errs, fitinfo=r), r
    else:
        return Params(like=p0, fitvals=popt, fiterrs=errs, fitinfo=r)

