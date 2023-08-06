import sys
import pandas as pd
import numpy as np
from scipy import linalg
import logging
from scipy.sparse import csr_matrix

from ._common import _design_matrix


def _pre_data(data_file, id, trait, agmat_file, fix=None):
    logging.info('Data file: {}'.format(data_file))
    data_df = pd.read_csv(data_file, sep='\s+', header=0)
    col_names = data_df.columns
    logging.info('The column names of data file: {}'.format(col_names))
    logging.info('Note: Variates beginning with a capital letter is converted into factors.')
    class_vec = []
    for val in col_names:
        if not val[0].isalpha():
            logging.info("The first character of columns names must be alphabet!")
            sys.exit()
        if val[0] == val.capitalize()[0]:
            class_vec.append(val)
            data_df[val] = data_df[val].astype('str')
        else:
            try:
                data_df[val] = data_df[val].astype('float')
            except Exception as e:
                logging.info(e)
                logging.info("{} may contain string, please check!".format(val))
                sys.exit()
    data_df = data_df.sort_values(by=id)
    id_in_gmat = list(pd.read_csv(agmat_file + '.id', sep='\s+', header=None, dtype={0: 'str'}).iloc[:, 0])
    logging.info('Individual column: ' + id)
    if id not in class_vec:
        logging.info('The initial letter of {} should be capital'.format(id))
        sys.exit()
    id_order = []   # id in order
    ind_keep = []  # keep id both in phenotype and genotype file
    for val in data_df[id]:
        if val in id_in_gmat:
            ind_keep.append(True)
            if val not in id_order:
                id_order.append(val)
        else:
            ind_keep.append(False)
    data_df = data_df.iloc[ind_keep, :]
    id_dct = dict(zip(id_order, range(len(id_order))))
    id_code = []  # code the id in the data file from 0 to ...
    for val in data_df[id]:
        id_code.append(id_dct[val])
    logging.info("The genomic relationship matrix file is: {}.agrm.id_fmt".format(agmat_file))
    ag = np.zeros((len(id_order), len(id_order)))
    with open(agmat_file + '.agrm.id_fmt') as fin:
        for line in fin:
            arr = line.split()
            try:
                ag[id_dct[arr[0]], id_dct[arr[1]]] = ag[id_dct[arr[1]], id_dct[arr[0]]] = float(arr[2])
            except Exception as _:
                pass
    logging.info('Trait column: {}'.format(trait))
    for val in trait:
        if val in class_vec:
            logging.error('The initial letter of {} should be lowercase'.format(trait))
            sys.exit()
    logging.info("The expression for the fixed effect: {}".format(fix))
    if fix is None:
        fix = "1"
    fix_vec = []
    for val in list(col_names):
        if val in fix:
            fix_vec.append(val)
    xmat_lst = []
    zmat_lst = []
    y_lst = []
    id_lst = []
    for val in trait:
        trait_df = data_df[[id] + fix_vec + [val]]
        ind = list(trait_df.isnull().any(axis=1)==False)
        trait_df = trait_df.iloc[ind, :]
        #print(trait_df)
        y_lst.append(np.array(trait_df[val]).reshape(-1, 1))
        xmat_lst.append(_design_matrix(fix, trait_df))
        id_code_keep = np.array(id_code)[ind]
        len_row = len(id_code_keep)
        len_col = len(id_order)
        zmat = csr_matrix(([1.0]*len_row, (list(range(len_row)), id_code_keep)), shape=(len_row, len_col))
        zmat_lst.append(zmat)
        id_lst.append(id_code_keep)

    def ind_cross(id1, id2):
        row = []
        col = []
        for i in range(len(id1)):
            try:
                col_i = id2.index(id1[i])
                col.append(col_i)
                row.append(i)
            except Exception as _:
                pass
        return row, col
    error_lst = []
    for i in range(len(id_lst)):
        error_vec = []
        for j in range(len(id_lst)):
            row, col = ind_cross(list(id_lst[i]), list(id_lst[j]))
            error = csr_matrix(([1.0]*len(row), (row, col)), shape=(len(id_lst[i]), len(id_lst[j])))
            error_vec.append(error)
        error_lst.append(error_vec)
    return y_lst, xmat_lst, zmat_lst, ag, error_lst
