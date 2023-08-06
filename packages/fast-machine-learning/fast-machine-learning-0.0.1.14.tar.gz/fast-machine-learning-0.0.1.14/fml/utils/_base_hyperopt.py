
import sys
if __name__ == "__main__":
    sys.path.append(".")
    from validates import validate_switch, Validate
    from _base import SelfMatrics
else:
    try:
        from ..validates import validate_switch, Validate
        from _base import SelfMatrics
    except:
        sys.path.append("..")
        sys.path.append(".")
        from validates import validate_switch, Validate
        from _base import SelfMatrics
from hyperopt import fmin, tpe, hp, STATUS_OK, Trials

class BaseHyperOpt(SelfMatrics):
    
    def __init__(self, f, space, max_evals=100, verbose=0):
        self.f = f
        self.space = space
        self.max_evals = max_evals
        self.verbose = verbose
        self.trials = None
    
    def _fit(self):
        self.trials = Trials()
        def min_f(params):
            loss = self.f(params)[0]
            return {"loss": loss, "status": STATUS_OK}
        result = fmin(fn=min_f, space=self.space, algo=tpe.suggest, 
                      max_evals=self.max_evals, trials=self.trials)
        return result
    
    
    