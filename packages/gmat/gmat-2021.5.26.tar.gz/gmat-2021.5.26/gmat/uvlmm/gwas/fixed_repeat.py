import logging
from functools import reduce
import numpy as np
import pandas as pd
from scipy import linalg
from pysnptools.snpreader import Bed
from tqdm import tqdm
from gmat.process_plink.process_plink import impute_geno
from scipy.stats import chi2
from scipy.sparse import csc_matrix
from patsy import dmatrix


def fixed_repeat(pheno_file, bed_file, agmat_file, bye=None, class_lst=None, fix=None, out_file='res.txt', condition_snp=None, npart=100,
          maxiter=100):
    """
    run GWAS based on linear mixed model and put one snp in each analysis.
    :param pheno_file: phenotypic file with head rows. The fist column is individual id. The last column is phenotypic values.
    Class variates and covariates are in the middle columns. Missing values in the phenotypic file can be
    expressed as 'NA', 'NaN', 'nan', 'na'.
    :param bed_file: the prefix for the plink binary file.
    :param agmat_file: the prefix for the additive genomic relationship matrix file.
    :param bye: the environment effect that SNP interacts with. Default is None.
    :param class_lst: a list for class variates
    :param fix: formula for the fix effect. Eg. fix='sex + herd'
    :param out_file: the output file. Default is 'res.txt'.
    :param condition_snp: A string or a list for the conditional SNP. Default is None.
    :param npart: divide the SNPs into n parts and read them into memory successively. Default is 100.
    :param maxiter: the maximum number of iteration for variance estimation in the null model.
    :return:
    """
    logging.info("###Prepare the phenotypic values, covariates and genomic matrix")
    y, xmat, zmat, ag, id_keep, bye_mat = _pre_pheno(pheno_file, agmat_file, bye, class_lst, fix)
    logging.info("###Estimate the variances in the null model.")
    init = np.array([np.var(y) / 3] * 3)
    var, convergence, vmat = _weight_emai_vmat(y, xmat, zmat, ag, init=init, maxiter=maxiter, cc_par=1.0e-8)
    vmat = linalg.inv(vmat)
    logging.info('Whether converge?: {}'.format(convergence))
    logging.info('The estimated variances: {}'.format(var))
    snp_on_disk = Bed(bed_file, count_A1=False)
    num_snp = snp_on_disk.sid_count
    fam_df = pd.read_csv(bed_file + '.fam', header=None, sep='\s+')
    id_in_fam = list(np.array(fam_df.iloc[:, 1], dtype=np.str))
    id_keep_ind = []
    for val in id_keep:
        id_keep_ind.append(id_in_fam.index(val))
    snp_index = []
    for i in range(npart):
        snp_index.append(int(num_snp / npart) * i)
    snp_index.append(num_snp)
    logging.info("Conditional SNP: {}".format(condition_snp))
    if condition_snp is not None:
        if not isinstance(condition_snp, list):
            condition_snp = [condition_snp]
        condition_snp_index = snp_on_disk.sid_to_index(condition_snp)
        condition_snp_val = snp_on_disk[id_keep_ind, condition_snp_index].read().val
        if np.any(np.isnan(condition_snp_val)):
            logging.info('Missing genotypes of conditional SNP are imputed with random genotypes.')
            condition_snp_val = impute_geno(condition_snp_val)
        xmat_con = np.array(condition_snp_val)
        if bye_mat is not None:
            xmat_con = np.concatenate([condition_snp_val, condition_snp_val*bye_mat], axis=1)
        xmat = np.concatenate([xmat, xmat_con], axis=1)
    logging.info('###Start the association')
    with open(out_file, 'w') as fout:
        if bye_mat is not None:
            fout.write('\t'.join(['chro', 'snp_ID', 'pos', 'allele1', 'allele2', 'eff', 'se', 'p_snp', 'p_gbye', 'p_all']))
            fout.write('\n')
        else:
            fout.write('\t'.join(['chro', 'snp_ID', 'pos', 'allele1', 'allele2', 'eff', 'se', 'p_snp']))
            fout.write('\n')
    for i in range(npart):
        logging.info('The {}/{} part'.format(i + 1, npart))
        snp_info = pd.read_csv(bed_file + '.bim', sep='\s+', header=None, skiprows=snp_index[i],
                               nrows=snp_index[i + 1] - snp_index[i])
        res_df = snp_info.iloc[:, [0, 1, 3, 4, 5]]
        res_df.columns = ['chro', 'snp_ID', 'pos', 'allele1', 'allele2']
        snp_mat = snp_on_disk[id_keep_ind, snp_index[i]:snp_index[i + 1]].read().val
        if np.any(np.isnan(snp_mat)):
            snp_mat = impute_geno(snp_mat)
        eff_vec = []
        se_vec = []
        p_snp_vec = []
        p_gbye_vec = []
        p_all_vec = []
        if bye_mat is not None:
            bye_df = bye_mat.shape[1]
            for k in tqdm(range(snp_mat.shape[1])):
                snpk = np.concatenate([snp_mat[:, k:(k + 1)], snp_mat[:, k:(k + 1)] * bye_mat], axis=1)
                xmat_k = np.concatenate([xmat, snpk], axis=1)
                # main
                vx = np.dot(vmat, xmat_k[:, :-bye_df])
                xvx = np.dot(xmat_k[:, :-bye_df].T, vx)
                try:
                    xvx = linalg.inv(xvx)
                except Exception as _:
                    xvx = np.diag(np.diag(xvx))*0.001 + xvx
                    xvx = linalg.inv(xvx)
                xvy = np.dot(vx.T, y)
                b_k = np.dot(xvx, xvy)
                eff = b_k[-1, -1]
                se = np.sqrt(xvx[-1, -1])
                t_val = eff / se
                p_val = chi2.sf(t_val * t_val, 1)
                # GbyE
                vx = np.dot(vmat, xmat_k)
                xvx = np.dot(xmat_k.T, vx)
                try:
                    xvx = linalg.inv(xvx)
                except Exception as _:
                    xvx = np.diag(np.diag(xvx))*0.001 + xvx
                    xvx = linalg.inv(xvx)
                xvy = np.dot(vx.T, y)
                b_k = np.dot(xvx, xvy)
                eff_bye = b_k[-bye_df:, :]
                eff_bye_cov = xvx[-bye_df:, -bye_df:]
                chi_val = np.sum(np.dot(eff_bye.T, np.dot(linalg.inv(eff_bye_cov), eff_bye)))
                p_bye = chi2.sf(chi_val, bye_df)
                chi_all = np.sum(np.dot(b_k[-(bye_df + 1):, :].T,
                                        np.dot(linalg.inv(xvx[-(bye_df + 1):, -(bye_df + 1):]),
                                               b_k[-(bye_df + 1):, :])))
                p_all = chi2.sf(chi_all, bye_df + 1)
                eff_vec.append(eff)
                se_vec.append(se)
                p_snp_vec.append(p_val)
                p_gbye_vec.append(p_bye)
                p_all_vec.append(p_all)
            res_df.loc[:, 'eff_val'] = eff_vec
            res_df.loc[:, 'se_val'] = se_vec
            res_df.loc[:, 'p_snp_val'] = p_snp_vec
            res_df.loc[:, 'p_gbye_val'] = p_gbye_vec
            res_df.loc[:, 'p_all_val'] = p_all_vec
        else:
            for k in tqdm(range(snp_mat.shape[1])):
                xmat_k = np.concatenate([xmat, snp_mat[:, k:(k + 1)]], axis=1)
                vx = np.dot(vmat, xmat_k)
                xvx = np.dot(xmat_k.T, vx)
                try:
                    xvx = linalg.inv(xvx)
                except Exception as _:
                    xvx = np.diag(np.diag(xvx)) * 0.001 + xvx
                    xvx = linalg.inv(xvx)
                xvy = np.dot(vx.T, y)
                b_k = np.dot(xvx, xvy)
                eff = b_k[-1, -1]
                se = np.sqrt(xvx[-1, -1])
                t_val = eff / se
                p_val = chi2.sf(t_val * t_val, 1)
                eff_vec.append(eff)
                se_vec.append(se)
                p_snp_vec.append(p_val)
            res_df.loc[:, 'eff_val'] = eff_vec
            res_df.loc[:, 'se_val'] = se_vec
            res_df.loc[:, 'p_snp_val'] = p_snp_vec
        res_df.to_csv(out_file, sep='\t', index=False, header=False, mode='a', na_rep='NA')
    return 0


def _pre_pheno(pheno_file, agmat_file, bye, class_lst, fix):
    id_in_agmat = []
    with open(agmat_file + '.id') as fin:
        for line in fin:
            arr = line.split()
            id_in_agmat.append(arr[0])
    data_df = pd.read_csv(pheno_file, sep='\s+', header=0)
    data_df = data_df.dropna()
    col_names = data_df.columns
    class_lst2 = [col_names[0]]
    if class_lst is not None:
        class_lst2 = class_lst + class_lst2
    for val in col_names:
        if val in class_lst2:
            data_df[val] = data_df[val].astype('str')
        else:
            data_df[val] = data_df[val].astype('float')
    id_keep = []  # keep the id both in the agmat file and pheno file, without missing phenotypes and covariates.
    for i in range(data_df.shape[0]):
        if data_df.iloc[i, 0] in id_in_agmat:
            id_keep.append(True)
        else:
            id_keep.append(False)
    data_df = data_df.iloc[id_keep, :]
    id_keep = list(data_df.iloc[:, 0])
    y = np.array(data_df.iloc[:, -1]).reshape(-1, 1)
    bye_mat = None
    xmat = np.ones((y.shape[0], 1))
    if bye is not None:
        xmat = dmatrix(bye, data_df)
        xmat = np.asarray(xmat).reshape(y.shape[0], -1)
        bye_mat = xmat[:, 1:]
    if fix is not None:
        xmat = dmatrix(fix, data_df)
        xmat = np.asarray(xmat)
        _, r = np.linalg.qr(xmat)
        indexes = np.absolute(np.diag(r)) >= 1e-10
        xmat = xmat[:, indexes]
    val = 0
    id_dct = {}
    col = []
    for v in id_keep:
        if v not in id_dct:
            id_dct[v] = val
            val += 1
        col.append(id_dct[v])
    row = range(len(id_keep))
    zmat = csc_matrix(([1.0]*len(row), (row, col)))
    ag = np.zeros((len(id_dct), len(id_dct)))
    with open(agmat_file + '.agrm.id_fmt') as fin:
        for line in fin:
            arr = line.split()
            try:
                ag[id_dct[arr[0]], id_dct[arr[1]]] = ag[id_dct[arr[1]], id_dct[arr[0]]] = float(arr[2])
            except Exception as e:
                del e
    return y, xmat, zmat, ag, id_keep, bye_mat


def _weight_emai_vmat(y, xmat, zmat, ag, init=None, maxiter=100, cc_par=1.0e-8):
    """
    Estimate variance parameters with vmat based on em
    :param y: Phenotypic vector
    :param xmat: the design matrix for fixed effect
    :param zmat: Design matrix for random effects
    :param ag: Genomic relationship matrix
    :param init: Default is None. A list for initial values of variance components
    :param maxiter: Default is 100. The maximum number of iteration times.
    :param cc_par: Convergence criteria for update vector.
    :return: The estimated variances.
    """
    logging.info("#####Prepare#####")
    var_com = np.array(init)
    num_var = len(var_com)
    zgzmat_lst = [zmat.dot((zmat.dot(ag)).T), zmat.dot(zmat.T)]
    logging.info('Initial variances: {}'.format(var_com))
    logging.info("#####Start the iteration#####")
    weight_vec = list(np.arange(0, 1, 0.01)) + [1.0]
    iter = 0
    cc_par_val = 1000.0
    delta = 1000.0
    while iter < maxiter:
        iter += 1
        logging.info('\n\nRound: {:d}'.format(iter))
        # V, the inverse of V and P
        vmat = zgzmat_lst[0] * var_com[0] + zgzmat_lst[1].toarray() * var_com[1] + np.diag([var_com[-1]] * y.shape[0])
        vmat = linalg.inv(vmat)
        vxmat = np.dot(vmat, xmat)
        xvxmat = np.dot(xmat.T, vxmat)
        xvxmat = linalg.inv(xvxmat)
        pmat = vmat - reduce(np.dot, [vxmat, xvxmat, vxmat.T])
        pymat = np.dot(pmat, y)
        # first partial derivatives and working variates
        fd_mat = np.zeros(num_var)
        wv_mat = []
        fd_mat[-1] = np.trace(pmat) - np.sum(np.dot(pymat.T, pymat))
        fd_mat[-1] = -0.5 * fd_mat[-1]
        fd_mat[0] = np.sum(pmat * zgzmat_lst[0]) - np.sum(reduce(np.dot, [pymat.T, zgzmat_lst[0], pymat]))
        fd_mat[0] = -0.5 * fd_mat[0]
        wv_mat.append(np.dot(zgzmat_lst[0], pymat))
        fd_mat[1] = np.sum(zgzmat_lst[1].multiply(pmat)) - np.sum(np.dot(pymat.T, zgzmat_lst[1].dot(pymat)))
        fd_mat[1] = -0.5 * fd_mat[1]
        wv_mat.append(zgzmat_lst[1].dot(pymat))
        wv_mat.append(pymat)
        wv_mat = np.concatenate(wv_mat, axis=1)
        ai_mat = 0.5 * reduce(np.dot, [wv_mat.T, pmat, wv_mat])
        em_mat = []
        for k in range(num_var - 1):
            em_mat.append(ag.shape[0] / (2 * var_com[k] * var_com[k]))
        em_mat.append(y.shape[0] / (2 * var_com[-1] * var_com[-1]))
        em_mat = np.diag(em_mat)
        for weight in weight_vec:
            wemai_mat = weight * em_mat + (1 - weight) * ai_mat
            delta = np.dot(linalg.inv(wemai_mat), fd_mat)
            var_com_new = var_com + delta
            if min(var_com_new) > 0:
                logging.info('EM weight value: ' + str(weight))
                break
        var_com_new = var_com + delta
        logging.info("Updated variances: {}".format(var_com_new))
        cc_par_val = np.sum(delta * delta) / np.sum(np.array(var_com_new) * np.array(var_com_new))
        cc_par_val = np.sqrt(cc_par_val)
        var_com = np.array(var_com_new)
        if cc_par_val < cc_par:
            break
    if cc_par_val < cc_par:
        logging.info('Variances converged.')
        convergence=True
    else:
        logging.info('Variances not converged.')
        convergence=False
    vmat = zgzmat_lst[0] * var_com[0] + zgzmat_lst[1].toarray() * var_com[1] + np.diag([var_com[-1]] * y.shape[0])
    return var_com, convergence, vmat
