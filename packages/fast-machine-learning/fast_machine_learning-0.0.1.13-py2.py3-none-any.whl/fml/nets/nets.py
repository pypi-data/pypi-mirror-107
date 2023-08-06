if __name__ == "__main__":
    import sys
    sys.path.append("..")
    from utils import is_regressor
else:
    from ..utils import is_regressor

import torch 
import torch.nn as nn
import torch.utils.data as Data
import numpy as np, copy
import sklearn.preprocessing as skpp
from itertools import zip_longest
from sklearn.metrics import mean_squared_error as mse, mean_absolute_error as mae, r2_score as r2, accuracy_score as accuracy, precision_score as precision, f1_score as f1, recall_score as recall, confusion_matrix as cm
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

def rmse(X, Y):
    return mse(X, Y) ** 0.5
def R(X, Y):
    return np.corrcoef(X, Y)[0][1]

class CommonLayer(nn.Module):
    def __init__(self, X_train, Y_train, X_test=None, Y_test=None, silent=True, scaler=skpp.StandardScaler, dimension=2, batch=64, gpu=True, defined_layers=None):
        """
        X_train, Y_train, X_test, Y_test: ndarray
        scaler: sklearn.preprocessing.class
        defined_layers: iterable that will pass to nn.Sequential
        """
        super(CommonLayer, self).__init__()
        
        self.dimension = dimension
        if X_train.shape[0] <= batch:
            self.batch = X_train.shape
        else:
            self.batch = batch
        self.gpu = gpu
        if not torch.cuda.is_available():
            self.gpu = False
        
        self.X_train = X_train
        self.Y_train = Y_train
        self.X_test = X_test
        self.Y_test = Y_test
        self.test_f = True
        self.reg = False
        self.silent = silent
        if X_test is None and Y_test is None:
            self.test_f = False
        if is_regressor(Y_train):
            self.reg = True
        
        if scaler.__name__ in dir(skpp):
            scaler = scaler
        else:
            if not self.silent:
                print("scaler not in sklearn.preprocessing, using preprocessing.StandardScaler.")
            scaler = skpp.StandardScaler
        scaler = scaler().fit(X_train, Y_train)
        self.X_train = scaler.transform(self.X_train)
        if self.test_f:
            self.X_test = scaler.transform(self.X_test)
        self.scaler = scaler
        
        self.X_train = torch.from_numpy(X_train.astype(np.float32))
        if self.reg:
            self.Y_train = torch.from_numpy(Y_train.astype(np.float32).reshape(-1, ))
        else:
            self.Y_train = torch.from_numpy(Y_train.astype(np.int64).reshape(-1, ))
        train_data = Data.TensorDataset(self.X_train, self.Y_train)
        if self.test_f:
            self.X_test = torch.from_numpy(X_test.astype(np.float32))
            if self.reg:
                self.Y_test = torch.from_numpy(Y_test.astype(np.float32).reshape(-1, ))
            else:
                self.Y_test = torch.from_numpy(Y_test.astype(np.int64).reshape(-1, ))
            test_data = Data.TensorDataset(self.X_test, self.Y_test)
        
        self.train_loader = Data.DataLoader(
                dataset=train_data,
                batch_size=self.batch,
                shuffle=True,
                num_workers=0
                )
        if self.test_f:
            self.test_loader = Data.DataLoader(
                    dataset=test_data,
                    batch_size=self.batch,
                    shuffle=False,
                    num_workers=0
                    )
        
        if not defined_layers or not isinstance(defined_layers, (list, tuple, nn.Sequential,)):
            if not self.silent:
                print("defined_layers is not one of list, tuple, nn.Sequential. The default net will be applied. ")
            self.dense_layers = self.default_layers()
        elif isinstance(defined_layers, nn.Sequential):
            self.dense_layers = defined_layers
        elif isinstance(defined_layers, (list, tuple,)):
            if isinstance(defined_layers[0], (float, int, )):
                in_lens = [self.X_train.shape[1]] + defined_layers
                out_lens = defined_layers + [1]
                defined_layers = []
                for in_len, out_len in zip_longest(in_lens, out_lens, fillvalue=1):
                    defined_layers.append(nn.Linear(in_len, out_len))
                    if out_len != 1:
                        defined_layers.append(nn.ReLU())
            elif defined_layers[0] in dir(nn):
                pass
            else:
                if not self.silent:
                    print("defined_layers is not numbers or nn.modules. The default net will be applied. ")
                defined_layers = self.default_layers()
            self.dense_layers = nn.Sequential(*defined_layers)
        if self.gpu:
            self.to(device)
        pass
    
    def forward(self, X):
        current_batch = X.size()[0]
        if self.dimension == 2:
            return self.dense_layers(X)
        else:
            X = self.dense_layers[0](X)
            s = int(X.size()[1]**0.5)
            X = X.view(current_batch, 1, s, s)
            X = self.dense_layers[1](X)
            s = int(X.flatten().size()[0] / current_batch)
            X = X.view(-1, s)
            X = self.dense_layers[2](X)
            return X
    
    def fit(self, epoches=2000, validate_per=0.15, lr=0.01, optimizer=torch.optim.Adam, criterion="auto"):
        optimizer = optimizer(self.parameters(), lr=lr)
        if criterion == "auto":
            if self.reg:
                criterion = nn.MSELoss
            else:
                # if len(self.Y_train.tolist()) >= 2:
                criterion = nn.CrossEntropyLoss
        criterion=criterion()
        training_per = 1 - 0.15
        if training_per < 0 or training_per >= 1: training_per = 0.85
        
        if self.reg:
            metric_criterion = ["r2_score", "rmse", "mse", "mae", "R"]
            metric_criterion_ = [r2, rmse, mse, mae, R]
        else:
            metric_criterion = ["accuracy_score", "precision_score", "f1_score", "recall_score", "confusion_matrix"]
            metric_criterion_ = [accuracy, precision, f1, recall, cm]
        metrics = dict()
        for i in ["train", "val", "best_train", "best_val","test"]:
            metrics.update({i:{}})
            for j in metric_criterion:
                if i in ["best_train", "best_val"]:
                    metrics[i].update({j:[0]})
                else:
                    metrics[i].update({j:[]})
        
        batch_number = len(self.train_loader) # 多少个batch
        train_batch_number = round(batch_number * training_per) # 训练集有多少个batch
        
        train_loss_all = []
        val_loss_all = []
        
        best_model_wts = copy.deepcopy(self.state_dict()) # 最佳模型参数
        best_epoch = 0
        
        ## 训练部分，分为两个阶段，第一阶段为训练阶段，第二阶段为验证阶段
        for epoch in range(epoches):
            if not self.silent:
                print(f"epoch - {epoch}")
            train_numbers = 0 # 训练集累计样本数
            val_numbers = 0 # 验证集的累计样本数
            train_loss = 0
            val_loss = 0
            train_preds = []
            train_obs = []
            val_preds = []
            val_obs = []
            
            for step, (batch_x, batch_y) in enumerate(self.train_loader):
                if self.dimension == 3:
                    batch_x = batch_x.unsqueeze(-1)
                if self.gpu:
                    batch_x, batch_y = batch_x.to(device), batch_y.to(device)
                ## 第一阶段，训练阶段
                if step < train_batch_number:
                    ## 常规的网络计算、误差反馈
                    output = self(batch_x).squeeze() # 计算得到output 
                    loss = criterion(output, batch_y) # 计算损失
                    optimizer.zero_grad() # 梯度清零
                    loss.backward() # 梯度反向传播
                    optimizer.step() # 参数更新
                    ## 累加损失
                    train_loss += loss.item() * batch_x.size(0) # 累加batch的训练损失
                    if not self.reg:
                        output = torch.argmax(output, axis=1)
                    train_preds.append(output) # 累计存放batch的训练预测值
                    train_obs.append(batch_y.data) # 累计存放batch的训练观测值
                    train_numbers += batch_x.size(0) # 累加训练样本数
                    print(f"train loss: {loss}")
                ## 第二阶段，验证阶段
                else:
                    with torch.no_grad():
                        output = self(batch_x).squeeze() # 计算output
                        loss = criterion(output, batch_y) # 计算损失
                        val_loss += loss.item() * batch_x.size(0) # 累加验证损失
                        if not self.reg:
                            output = torch.argmax(output, axis=1)
                        val_preds.append(output) # 累计存放batch的验证预测值
                        val_obs.append(batch_y.data) # 累计存放batch的验证观测值
                        val_numbers += batch_x.size(0) # 累加验证样本数
                        print(f"val loss: {loss}")
                
            ## 一个epoch完成后，将观测值与预测值进行cat合并
            train_obs = torch.cat(train_obs)
            train_preds = torch.cat(train_preds)
            val_obs = torch.cat(val_obs)
            val_preds = torch.cat(val_preds)
            ## 如果开启了gpu，那么此处需要将数据传回cpu类型
            if self.gpu:
                train_obs = train_obs.cpu()
                train_preds = train_preds.cpu()
                val_obs = val_obs.cpu()
                val_preds = val_preds.cpu()
            ## 可以直接计算batch的平均损失，因为loss不是tensor
            train_loss_all.append(train_loss / train_numbers)
            val_loss_all.append(val_loss / val_numbers)
            ## 对于训练预测值和训练观测值来说是tensor，且训练预测值开启了requires_grad，因此需要先detach再转为numpy
            train_obs = train_obs.numpy().reshape(-1, )
            train_preds = train_preds.detach().numpy().reshape(-1, )
            val_obs = val_obs.numpy().reshape(-1, )
            val_preds = val_preds.detach().numpy().reshape(-1, )
            for name, metric in zip(metric_criterion, metric_criterion_):
                metrics["train"][name].append(metric(train_obs, train_preds))
                metrics["val"][name].append(metric(val_obs, val_preds))
            if metrics["val"][metric_criterion[0]][-1] > metrics["best_val"][metric_criterion[0]]:
                best_epoch = epoch
                best_model_wts = copy.deepcopy(self.state_dict())
                for m in metric_criterion:
                    metrics["best_train"][m] = metrics["train"][m][-1]
                    metrics["best_val"][m] = metrics["val"][m][-1]
        ## 完成训练后，让net读取最佳模型参数
        self.load_state_dict(best_model_wts)
        
        if self.test_f:
            test_preds = [] # 累计存放测试集的预测值
            test_obs = [] # 累计存放测试集的观测值
            test_loss = 0 # 累加测试集的损失
            test_num = 0 # 累加测试集的样本数
            ## 开始测试
            for step, (batch_x, batch_y) in enumerate(self.test_loader):
                if self.dimension == 3:
                    batch_x = batch_x.unsqueeze(0).unsqueeze(0)
                ## 如果开启了GPU，那么此处要先把数据发送到GPU上
                if self.gpu:
                    batch_x, batch_y = batch_x.to(device), batch_y.to(device)
                ## 注意测试时不需要计算梯度和反向传播梯度，因此需要使用torch.no_grad()
                with torch.no_grad():
                    output = self(batch_x).squeeze() # 计算output
                    loss = criterion(output, batch_y) # 计算loss
                    if not self.reg:
                        output = torch.argmax(output, axis=1)
                    test_preds.append(output) # 累计存放测试集的预测值
                    test_obs.append(batch_y.data) # 累计存放测试集的预测值
                    test_loss += loss.item() * batch_x.size(0) # 累加测试集损失
                    test_num += batch_x.size(0) # 累加测试集的样本数
            test_loss_all = test_loss / test_num # 计算总的测试集平均损失
            test_preds = torch.cat(test_preds) # 将测试集的预测值进行合并
            test_obs = torch.cat(test_obs) # 将测试集的观测值进行合并
            ## 如果开启了GPU，那么此处需要先把观测值和预测值变回cpu类型数据
            if self.gpu:
                test_preds = test_preds.cpu()
                test_obs = test_obs.cpu()
            ## 观测值和预测值是tensor类型数据，可以直接计算。这里不用numpy方法也可直接计算
            test_obs = test_obs.numpy().reshape(-1, )
            test_preds = test_preds.detach().numpy().reshape(-1, )
            for name, metric in zip(metric_criterion, metric_criterion_):
                metrics["test"][name].append(metric(test_obs, test_preds))
        return dict(
            scaler = self.scaler,
            train = metrics["best_train"],
            test = metrics["test"],
            val = metrics["best_val"],
            train_process = metrics["train"],
            val_process = metrics["val"],
            net = self
            )
    def default_layers(self):
        s = self.X_train.shape[1]
        if self.reg:
            out_s = 1
        else:
            out_s = len(set(self.Y_train.numpy().tolist()))
        if self.dimension == 2:
            return nn.Sequential(
                nn.Linear(s, 64),
                nn.ReLU(),
                nn.Linear(64, 256),
                nn.ReLU(),
                nn.Linear(256, 512),
                nn.ReLU(),
                nn.Linear(512, 256),
                nn.ReLU(),
                nn.Linear(256, 32),
                nn.ReLU(),
                nn.Linear(32, out_s)
                )
        elif self.dimension == 3:
            if s >= 16:
                conv_core_size = 5
            elif s >= 13:
                conv_core_size = 4
            elif s >= 10:
                conv_core_size = 3
            elif s >= 7:
                conv_core_size = 2
            elif s >= 4:
                conv_core_size = 1
            else:
                conv_core_size = 0
            li_s = (s - conv_core_size + 1) // 2
            li_s = (li_s - conv_core_size + 1) // 2
            li_s = 32 * (li_s ** 2)
            return nn.ModuleList([
                nn.Sequential(
                    nn.Conv1d(s, s**2, 1),
                    ),
                nn.Sequential(
                    nn.Conv2d(1, 16, conv_core_size),
                    nn.ReLU(),
                    nn.MaxPool2d(2, 2),
                    nn.Conv2d(16, 32, conv_core_size),
                    nn.ReLU(),
                    nn.MaxPool2d(2, 2),
                    ),
                nn.Sequential(
                    nn.Linear(li_s, li_s*2),
                    nn.ReLU(),
                    nn.Linear(li_s*2, li_s),
                    nn.ReLU(),
                    nn.Linear(li_s, li_s // 2),
                    nn.ReLU(),
                    nn.Linear(li_s // 2, out_s)
                    )
                ])
if __name__ == "__main__":
    from sklearn.datasets import load_boston
    X, Y = load_boston(return_X_y=True)
    dl = CommonLayer(X, Y, dimension=2, batch=32, silent=False)
    result = dl.fit(epoches=200)
    # X = X[:64, :16]
    # s = X.shape
    # if min(s) >= 16:
    #     conv_core_size = 5
    # elif min(s) >= 13:
    #     conv_core_size = 4
    # elif min(s) >= 10:
    #     conv_core_size = 3
    # elif min(s) >= 7:
    #     conv_core_size = 2
    # elif min(s) >= 4:
    #     conv_core_size = 1
    # else:
    #     conv_core_size = 0
    # linear_s_0 = ( ( (s[0] - (conv_core_size - 1) ) // 2 ) - (conv_core_size - 1) ) // 2
    # linear_s_1 = ( ( (s[1] - (conv_core_size - 1) ) // 2 ) - (conv_core_size - 1) ) // 2
    # linear_s = linear_s_0*linear_s_1*32
    
    # X = torch.from_numpy(X.astype(np.float32)).unsqueeze(-1)
    # print(X.size())
    # X = nn.Conv1d(16, 16**2, 1)(X)
    # s = int(X.size()[1] ** 0.5)
    # X = X.view(64, 1, s, s)
    # print(X.size())
    # dense = nn.Sequential(
    #             nn.Conv2d(1, 16, conv_core_size),
    #             nn.ReLU(),
    #             nn.MaxPool2d(2, 2),
    #             nn.Conv2d(16, 32, conv_core_size),
    #             nn.ReLU(),
    #             nn.MaxPool2d(2, 2),
    #             )
    # X = dense(X)
    # X = X.view(-1, int(X.flatten().size()[0] / 64))
    # dense2 = nn.Sequential(
    #             nn.Linear(int(X.flatten().size()[0] / 64), 256),
    #             nn.ReLU(),
    #             nn.Linear(256, 128),
    #             nn.ReLU(),
    #             nn.Linear(128, 10)
    #             )
    # X = dense2(X)
    # print(X.size())
