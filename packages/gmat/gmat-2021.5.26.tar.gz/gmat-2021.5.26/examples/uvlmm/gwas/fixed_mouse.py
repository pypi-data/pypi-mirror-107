import logging
from gmat.gmatrix import agmat
from gmat.uvlmm.gwas import fixed, fixed_gbye
logging.basicConfig(level=logging.INFO)
pheno_file = 'pheno'
bed_file = 'plink'


agmat_file = 'test'
agmat2 = agmat(bed_file, out_file=agmat_file, inv=False, small_val=0.001, out_fmt='id_id_val')

fixed(pheno_file, bed_file, agmat_file, class_lst=["mean", "sex", "treat"], fix="mean + sex + age + treat", out_file='res.txt', 
     condition_snp=None, npart=100, maxiter0=100, maxiter1=10, speed=True, pcut=5e-05)


# 基因环境互作、不加永久环境效应，batch是连续变量
bye = 'age'
fixed_gbye(pheno_file, bed_file, agmat_file, bye, class_lst=["mean", "sex", "treat"], fix="mean + sex + age + treat",
           out_file='res3.txt', condition_snp=None, npart=100,
          maxiter0=100, maxiter1=10, speed=True, pcut=5.0e-5)

# 基因环境互作、不加永久环境效应，batch是分类变量
bye = 'age'
fixed_gbye(pheno_file, bed_file, agmat_file, bye, class_lst=["mean", "sex", "treat"], fix="mean + sex + age + treat",
           out_file='res4.txt', condition_snp=None, npart=100,
          maxiter0=100, maxiter1=10, speed=True, pcut=5.0e-5)
