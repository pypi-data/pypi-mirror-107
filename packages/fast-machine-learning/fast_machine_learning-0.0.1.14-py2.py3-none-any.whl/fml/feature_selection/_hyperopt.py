from hyperopt import hp
if __name__ == "__main__":
    import sys
    sys.path.append("..")
    from utils import BaseHyperOpt
    from validates import Validate
else:
    from ..validates import Validate
    from ..utils import BaseHyperOpt
import numpy as np

class SingleFeatureHyperOpt(BaseHyperOpt):
    
    def __init__(self, flen=5, max_evals=100, verbose=0):
        super(SingleFeatureHyperOpt, self).__init__(None, None, max_evals, verbose)
        self.flen = flen
    
    def fit(self, flag, algo, X, Y, **model_p):
        self.is_regressor = self._is_regressor(Y.tolist())
        featurespace = {}
        for fl in range(self.flen):
            featurespace.update({str(fl): hp.randint(str(fl), X.shape[1])})
        self.space = featurespace
        def f(params):
            result = Validate(algo, X[:, np.array(list(params.values()))], Y, **model_p).validate_switch(flag)
            if self.is_regressor:
                loss = result["rmse"]
            else:
                loss = 1 / (result["accuracy_score"] + 0.0000001)
            return loss, result, 
        best = self._fit()
        return np.array(list(best.values())), f(best)
# class AutoFeatureHyperOpt(BaseHyperOpt):
#     def __init__(self, min_flen=3, max_flen=10, max_evals=100, verbose=0):
#         super(SingleFeatureHyperOpt, self).__init__(None, None, max_evals, verbose)
#         self.min_flen = min_flen
#         self.max_flen = max_flen
    
#     def fit(self, flag, algo, X, Y, **model_p):
#         self.is_regressor = self._is_regressor(Y.tolist())
#         if self.min_flen <= 0:
#             self.min_flen = 3
#         if self.max_flen > X.shape[1]:
#             self.max_flen = X.shape[1]
        
        
        
    
if __name__ == "__main__":
    from sklearn.datasets import load_boston
    import xgboost; algo = xgboost.XGBRegressor
    import copy
    dataset = load_boston()
    X = dataset.data
    Y = dataset.target
    
    best, loss = SingleFeatureHyperOpt().fit(10, algo, X, Y)
    # frange = list(range(100))
    # a = dict()
    # depth = 0
    
    # def create_tree(frange, depth=0):
        
    #     if depth >= 5:
    #         return frange
    #     my_tree = {}
    #     for i in frange:
    #         b = copy.deepcopy(frange)
    #         b.pop(frange.index(i))
    #         my_tree[i] = create_tree(b, depth+1)
        
    #     return my_tree
    
    # c = create_tree(frange)
    
# =============================================================================
# def single_hyperopt(X, Y, algo, flen, loo=10):
#     
#     featurespace = {}
#     for fl in range(flen):
#         featurespace.update({str(fl): hp.randint(str(fl), X.shape[1])})
#     
#     trials = Trials()
#     
#     def f(params):
#         print(params)
#         result = validate_switch(loo, algo, X[:, np.array(list(params.values()))], Y)
#         if len(set(Y)) > 8:
#             loss = result["rmse"]
#         else:
#             loss = 1 / result["accuracy_score"] + 0.0000001
#         return {'loss': loss, 'status': STATUS_OK}
# 
#     best = fmin(fn=f, space=featurespace, algo=tpe.suggest, max_evals=100, trials=trials)
# 
#     return best, f(best)["loss"]
# 
# def auto_hyperopt(X, Y, algo, loo=10):
#     
#     maxflen = X.shape[1]
#     
#     # try:
#     #     pyll.scope.getattr(pyll.scope, "foo")
#     #     pyll.scope.undefine("foo")
#     # except:
#     #     pass
#     
#     # @pyll.scope.define
#     # def foo():
#     #     flen = np.random.randint(maxflen)
#     #     return np.random.choice(np.arange(flen))
#     
#     # featurespace = pyll.scope.foo()
#     
#     featurespace = {}
#     featurespace.update(dict(rs=hp.randint("rs", 0, 999999)))
#     featurespace.update(dict(maxf=hp.randint("maxf", 2, maxflen)))
#     
#     trials = Trials()
#     
#     def f(params):
#         print(params)
#         
#         from sklearn.utils import check_random_state
#         rng = check_random_state(params["rs"])
#         perm = rng.permutation(maxflen)
#         fi = perm[:params["maxf"]]
#         
#         result = validate_switch(loo, algo, X[:, fi], Y)
#         if len(set(Y)) > 8:
#             loss = result["rmse"]
#         else:
#             loss = 1 / result["accuracy_score"] + 0.0000001
#         return {'loss': loss, 'status': STATUS_OK, "fi":fi}
# 
#     best = fmin(fn=f, space=featurespace, algo=tpe.suggest, max_evals=100, trials=trials)
# 
#     return best, f(best)
# =============================================================================

# if __name__ == "__main__":
    # from sklearn.datasets import load_boston
    # import xgboost; algo = xgboost.XGBRegressor
    # dataset = load_boston()
    # X = dataset.data
    # Y = dataset.target
    
    # best, loss = single_hyperopt(X, Y, algo, 12, False)
    # best, loss = auto_hyperopt(X, Y, algo, False)