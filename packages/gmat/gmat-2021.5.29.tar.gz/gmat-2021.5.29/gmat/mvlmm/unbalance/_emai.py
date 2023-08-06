import numpy as np
import pandas as pd


def _emai(y_lst, xmat_lst, zmat_lst, ag, error_lst, init=init, maxiter=maxiter, cc_par=cc_par,
                      cc_gra=cc_gra, em_weight_step=em_weight_step):
    def init_var(y_lst):
        """
        initialize the variances
        """
        y_var_lst = np.array(list(map(np.var, y_lst)))/2
        add_cov = np.diag(y_var_lst)
        add_ind = np.tril_indices_from(add_cov)
        error_cov = np.diag(y_var_lst)
        error_ind = np.tril_indices_from(error_cov)
        cov_ind = [1] * len(add_ind[0]) + [2] * len(error_ind[0])
        cov_ind_i = list(add_ind[0] + 1) + list(error_ind[0] + 1)
        cov_ind_j = list(add_ind[1] + 1) + list(error_ind[1] + 1)
        var_com = list(add_cov[add_ind]) + list(error_cov[error_ind])
        var_df = {'var': cov_ind,
                  "vari": cov_ind_i,
                  "varj": cov_ind_j,
                  "var_com": var_com}
        var_df = pd.DataFrame(var_df, columns=['var', "vari", "varj", "var_com"])
        return np.array(var_com), var_df
    var_com, var_df = init_var(y_lst)
    if init is not None:
        if len(var_com) != len(init):
            logging.error('The length of initial variances should be {}'.format(len(var_com)))
            sys.exit()
        else:
            var_com = np.array(init)
            var_df['var_com'] = var_com

   def pre_cov(y_lst, var_df):
        """
        return the covariance matrix. If one covariance matrix is not positive, return None.
        """
        add_cov = np.zeros((len(y_lst), len(y_lst)))
        add_cov[np.tril_indices(len(y_lst))] = np.array(var_df[var_df['var']==1].iloc[:, -1])
        add_cov = np.add(add_cov, np.tril(add_cov, -1).T)
        error_cov = np.zeros((len(y_lst), len(y_lst)))
        error_cov[np.tril_indices(len(y_lst))] = np.array(var_df[var_df['var'] == 2].iloc[:, -1])
        error_cov = np.add(error_cov, np.tril(error_cov, -1).T)
        try:
            linalg.cholesky(add_cov)
            linalg.cholesky(error_cov)
        except Exception as _:
                return None
        return add_cov, error_cov

    cov_lst = pre_cov(y_lst, var_df)
    if cov_lst is None:
        logging.error("ERROR: Initial variances is not positive define, please check!")
        sys.exit()
    iter_count = 0
    cc_par_val = 1000.0
    cc_gra_val = 1000.0
    delta = 1000.0
    var_com_update = var_com * 1000
    logging.info("initial variances: {}".format(var_df))
    while iter_count < maxiter:
