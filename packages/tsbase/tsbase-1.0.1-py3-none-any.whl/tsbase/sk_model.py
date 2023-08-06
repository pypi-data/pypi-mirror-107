
import numpy as np
from sklearn.linear_model import BayesianRidge, SGDRegressor
from sklearn.svm import SVR
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.multioutput import MultiOutputRegressor


def br_model(tr_x, tr_y, te_x):
    br = BayesianRidge()
    br_mul = MultiOutputRegressor(br).fit(X=tr_x, y=tr_y)
    br_pred = br_mul.predict(te_x)
    # br_pred: shape=(n_samples, n_outputs)
    return br_pred, br_mul


def sgd_model(tr_x, tr_y, te_x):
    sgd = SGDRegressor()
    sgd_mul = MultiOutputRegressor(sgd).fit(X=tr_x, y=tr_y)
    sgd_pred = sgd_mul.predict(te_x)
    return sgd_pred, sgd_mul


def svr_model(tr_x, tr_y, te_x, kernel='rbf', gamma=0.01, c=1, is_default=True):
    if is_default:
        svr = SVR()
    else:
        svr = SVR(kernel=kernel, gamma=gamma, C=c, cache_size=2000)
    svr_mul = MultiOutputRegressor(svr).fit(X=tr_x, y=tr_y)
    svr_pred = svr_mul.predict(te_x)
    return svr_pred, svr_mul


def dt_model(tr_x, tr_y, te_x):
    dt = DecisionTreeRegressor()
    if tr_y.shape[1] > 1:
        dt.fit(X=tr_x, y=tr_y)
        dt_pred = dt.predict(te_x)
        return dt_pred, dt
    else:
        dt.fit(X=tr_x, y=tr_y.ravel())
        dt_pred = dt.predict(te_x)
        return np.reshape(dt_pred, (len(dt_pred), 1)), dt


def rf_model(tr_x, tr_y, te_x):
    rf = RandomForestRegressor(n_jobs=-1, n_estimators=100)
    if tr_y.shape[1] > 1:
        rf.fit(X=tr_x, y=tr_y)
        rf_pred = rf.predict(te_x)
        return rf_pred, rf
    else:
        rf.fit(X=tr_x, y=tr_y.ravel())
        rf_pred = rf.predict(te_x)
        return np.reshape(rf_pred, (len(rf_pred), 1)), rf


def gbr_model(tr_x, tr_y, te_x):
    gbr = GradientBoostingRegressor()
    gbr_mul = MultiOutputRegressor(gbr).fit(X=tr_x, y=tr_y)
    gbr_pred = gbr_mul.predict(te_x)
    return gbr_pred, gbr_mul


def mlp_model(tr_x, tr_y, te_x,
              hidden_layer_sizes, max_iter=200,
              solver='adam',
              learning_rate_init=0.001,
              random_state=None, ):

    mlp = MLPRegressor(hidden_layer_sizes=hidden_layer_sizes,
                       max_iter=max_iter,
                       solver=solver,
                       learning_rate_init=learning_rate_init,
                       random_state=random_state,
                       shuffle=False, )
    if tr_y.shape[1] > 1:
        mlp.fit(X=tr_x, y=tr_y)
        mlp_pred = mlp.predict(te_x)
        return mlp_pred, mlp
    else:
        mlp.fit(X=tr_x, y=tr_y.ravel())
        mlp_pred = mlp.predict(te_x)
        return np.reshape(mlp_pred, (len(mlp_pred), 1)), mlp


