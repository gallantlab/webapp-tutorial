import docdb
import numpy as np

docdbi = docdb.getclient()

def get_motparams(expname, runnum):
    mcims = docdbi.query(experiment_name = expname, generated_by_name="MotionCorrectFSL", block_number = runnum)
    motdata = mcims.generated_by.outputs["transforms"].get_params()
    return np.hstack(motdata)