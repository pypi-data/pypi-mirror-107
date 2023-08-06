
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score, \
    confusion_matrix, accuracy_score, f1_score, recall_score, precision_score
from sklearn.model_selection import LeaveOneOut, KFold
import numpy as np
if __name__ == "__main__":
    import sys
    sys.path.append("../utils")
    from check import is_regressor, ensure_ndarray, ensure_1d
else:
    from ..utils import is_regressor, ensure_ndarray, ensure_1d

class Validate:
    
    def __init__(self, algo, X, Y, X_test=None, Y_test=None, **modelparams):
        
        self.X = ensure_ndarray(X)
        self.Y = ensure_ndarray(Y)
        self.Y = ensure_1d(self.Y)
        self.X_test = ensure_ndarray(X_test)
        self.Y_test = ensure_ndarray(Y_test)
        self.Y_test = ensure_1d(self.Y_test)
        self.modelparams = modelparams
        self.algo = algo
        
        if X_test or Y_test is None:
            self.test_f = False
        
        self.is_regressor = is_regressor(Y.tolist())
        
        self.train_result = None
        self.test_result = None
        self.loo_result = None
        self.cv10_result = None
        self.cv5_result = None
        
        self.additional_results = dict()
        
    def validate_train(self):
        model = self.algo(**self.modelparams).fit(self.X, self.Y)
        preds = ensure_1d(model.predict(self.X))
        self.train_result = self.metrics(self.Y, preds)
        self.train_result.update(dict(model=model))
        return self
    
    def validate_loo(self):
        loo = LeaveOneOut()
        loo.get_n_splits(self.X)
        preds = []
        obs = []
        for itrain, itest in loo.split(self.X):
            xtrain, xtest = self.X[itrain], self.X[itest]
            ytrain, ytest = self.Y[itrain], self.Y[itest]
            preds += self.algo(**self.modelparams).fit(xtrain, ytrain).predict(xtest).tolist()
            obs += ytest.tolist()
        preds = np.array(preds)
        obs = np.array(obs)
        self.loo_result = self.metrics(obs, preds)
        return self
    
    def validate_test(self, X_test=None, Y_test=None):
        self.update_data(X_test, Y_test)
        if self.X_test is None or self.Y_test is None:
            print("X_test or Y_test is None, validate nothing")
            return self
        if self.train_result is None:
            self.validate_train()
        preds = self.train_result["model"].predict(X_test)
        self.test_result = self.metrics(self.X_test, preds)
        return self
    
    def cv10(self, shuffle=True):
        self.validate_cv(10, shuffle)
        return self
    
    def cv5(self, shuffle=True):
        self.validate_cv(5, shuffle)
        return self
    
    def validate_cv(self, cv, shuffle=True):
        kf = KFold(n_splits=cv, shuffle=shuffle)
        kf.get_n_splits(self.X)
        preds = []
        obs = []
        for itrain, itest in kf.split(self.X):
            xtrain, xtest = self.X[itrain], self.X[itest]
            ytrain, ytest = self.Y[itrain], self.Y[itest]
            preds += self.algo(**self.modelparams).fit(xtrain, ytrain).predict(xtest).tolist()
            obs += ytest.tolist()
        preds = np.array(preds)
        obs = np.array(obs)
        result = self.metrics(obs, preds)
        self.__dict__.update({
            f"cv{cv}_result": result
            })
        if cv not in [5, 10]:
            self.additional_results.update({
                f"cv{cv}_result": result
                })
        return self
    
    def validate_all(self, additional_cv=[], shuffle=True):
        for index, validate in [
                self.validate_train, 
                self.validate_test,
                self.validate_cv10,
                self.validate_cv5,
                self.validate_loo
                  ] + additional_cv:
            if index >= 5:
                if isinstance(validate, int):
                    self.validate_cv(validate, shuffle)
            else:
                validate()
        return self
    
    def update_data(self, X=None, Y=None, X_test=None, Y_test=None, **modelparams):
        if X is not None:
            self.X = ensure_ndarray(X)
        if Y is not None:
            self.Y = ensure_ndarray(Y)
            self.Y = ensure_1d(self.Y)
        if X_test is not None:
            self.X_test = ensure_ndarray(X_test)
        if Y_test is not None:
            self.Y_test = ensure_ndarray(Y_test)
            self.Y_test = ensure_1d(self.Y_test)
        if modelparams is not None:
            self.modelparams = modelparams
        return self
    
    def metrics(self, obs, preds):
        if self.is_regressor:
            return dict(
                r2_score = r2_score(obs, preds),
                mse = mean_squared_error(obs, preds),
                mae = mean_absolute_error(obs, preds),
                rmse = np.sqrt(mean_squared_error(obs, preds)),
                preds = preds,
                true_value = obs,
                R = self.R(obs, preds)
            )
        else:
            return dict(
                confusion_matrix = confusion_matrix(obs, preds),
                accuracy_score = accuracy_score(obs, preds),
                preds = preds,
                true_value = obs,
                precision_score = precision_score(obs, preds),
                f1_score = f1_score(obs, preds),
                recall_score = recall_score(obs, preds)
            )
    
    def R(self, obs, preds):
        return np.corrcoef(obs, preds)[0][1]
    
    @property
    def results(self):
        return dict(
            train=self.train_result,
            test=self.test_result,
            loo=self.loo_result,
            cv5=self.cv5_result,
            cv10=self.cv10_result
            ).update(self.additional_results)