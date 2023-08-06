from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score, \
    confusion_matrix, accuracy_score, f1_score, recall_score, precision_score
import numpy as np

class SelfMatrics:
    
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
    def _is_regressor(self, X):
        if len(set(X)) > 8:
            return True