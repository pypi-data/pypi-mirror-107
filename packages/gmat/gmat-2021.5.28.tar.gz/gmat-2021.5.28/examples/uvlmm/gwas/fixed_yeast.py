import logging
from gmat.gmatrix import agmat
from gmat.uvlmm.gwas import fixed, fixed_gbye, fixed_, fixed_repeat
logging.basicConfig(level=logging.INFO)
bed_file = 'CobaltChloride'
pheno_file = 'CobaltChloride3'
# id-id-value form
agmat_file = 'test'

agmat2 = agmat(bed_file, out_file=agmat_file, inv=False, small_val=0.001, out_fmt='id_id_val')

# 和GEMMA相同
fixed(pheno_file, bed_file, agmat_file, class_lst=['batch'], fix="batch",
out_file='res1.txt', condition_snp=None, npart=100, maxiter0=100, maxiter1=10,
          speed=True, pcut=5.0e-5)

# conditional GWAS
fixed(pheno_file, bed_file, agmat_file, class_lst=None, fix="batch",
out_file='res2.txt', condition_snp=None, npart=100, maxiter0=100, maxiter1=10,
          speed=True, pcut=5.0e-5)

# 基因环境互作、不加永久环境效应，batch是连续变量
bye = 'batch'
fixed_gbye(pheno_file, bed_file, agmat_file, bye, class_lst=None, fix=None, out_file='res3.txt', condition_snp=None, npart=100,
          maxiter0=100, maxiter1=10, speed=True, pcut=5.0e-5)

# 基因环境互作、不加永久环境效应，batch是分类变量
bye = 'batch'
fixed_gbye(pheno_file, bed_file, agmat_file, bye, class_lst=["batch"], fix=None, out_file='res4.txt', condition_snp=None, npart=100,
          maxiter0=100, maxiter1=10, speed=True, pcut=5.0e-5)


"""
# 基因环境互作、加永久环境效应，batch是连续变量
fixed_repeat(pheno_file, bed_file, agmat_file, bye=bye, class_lst=None, fix=None, out_file='res5.txt', condition_snp=None, npart=100,
          maxiter=100)


# 基因环境互作、加永久环境效应，batch是分类变量
fixed_repeat(pheno_file, bed_file, agmat_file, bye=bye, class_lst=["batch"], fix=None, out_file='res6.txt', condition_snp=None, npart=100,
          maxiter=100)
"""
