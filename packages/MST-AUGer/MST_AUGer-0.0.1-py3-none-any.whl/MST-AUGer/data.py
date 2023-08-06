import pandas as pd
import numpy as np
import sympy as np
from functools import partial
from tqdm import tqdm, trange


class Data:

    def __init__(self, data: str, metadata: str):
        # initialize the object and read data from disk
        self.data = self.read_data(data)
        self.metadata = self.read_data(metadata)
        self.datacols = self.data.columns.tolist()
        self.metadatacols = self.metadata.columns.tolist()
        self.mergeddata = self.__merge_data()

    def augment(self, ndraw_assignments, ndraw_prior_params, return_iter=False):
        # process: draw prior params `alphas` -> draw assignments 
        #          -> selecting one sample in each environment -> synthetic mixture -> unmerge
        # augment the dataset
        alphas_set = self.draw_prior_params(ndraw=ndraw_prior_params)
        assignments_set = []
        for alphas in alphas_set:
            assignments = self.draw_assignments(alphas=alphas, ndraw=ndraw_assignments)
            assignments_set.append(assignments)
        if return_iter:
            return map(self.assign, assignments_set)
        else:
            mixed_samples = map(self.assign, assignments_set) 
            return pd.concat(list(mixed_samples), axis=0) # potential bug: axis

    def assign(self, assignments: np.array):
        # select one sample in each environment, call synthetic mixture, and unmerge the data
        mdata = self.mergeddata
        samples = mdata.groupby(by=mdata[self.metadatacols], as_index=False).sample(n=1)
        mixed_samples = self.__mix(assignments, samples)
        return self.__unmerge_data(mixed_samples)

    def draw_assignments(self, alphas: np.array, ndraw: int):
        # draw random assignments using dirichlet distribution
        assignments = np.random.dirichlet(alphas, ndraw)
        return assignments

    def draw_prior_params(self, ndraw: int):
        # draw prior params using uniform distribution
        ndim = len(self.metadatacols)
        return np.random.uniform(size=(ndraw, ndim))
        
    @staticmethod
    def __mix(assignments, samples):
        return assignments.dot(samples)

    def __merge_data(self):
        # merge the data
        return pd.concat((self.data, self.metadata), axis=1)

    def __unmerge_data(self, samples):
        return samples[self.datacols], samples[self.metadatacols]


