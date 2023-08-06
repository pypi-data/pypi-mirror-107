
import sys
from sklearn.feature_selection import RFE as SKRFE
if __name__ == "__main__":
    sys.path.append("..")
    from validates import validate_switch, Validate
else:
    from ..validates import validate_switch, Validate

class RFE:
    
    def __init__(self, number_feature=None, verbose=0):
        self.number_feature = number_feature
        self.verbose = verbose
        
        self.feature_order = None
        self.feature_importance = None
    
    def fit(self, algo, X, Y, **model_p):
        rfe = SKRFE(algo(**model_p), n_features_to_select=self.number_feature, verbose=self.verbose).fit(X, Y)
        original_index = np.arange(X.shape[1])
        self.feature_importance = np.array(sorted(zip(original_index, rfe.ranking_), key=lambda x: x[1], reverse=False))
        self.feature_order = self.feature_importance[:, 0]
        return self


if __name__ == "__main__":
    
    from sklearn.svm import SVR, SVC
    from sklearn.datasets import load_boston, load_breast_cancer
    import numpy as np
    from xgboost import XGBRegressor, XGBClassifier
    X, Y = load_boston(return_X_y=True)
    
    rfe = RFE().fit(XGBRegressor, X, Y)
    feature_order = rfe.feature_order
