# Imports
import numpy as np
from numpy import matlib as npm
import pandas as pd
import time
import phate
from scipy import sparse
import umap.umap_ as umap
import RandomForest


#sklearn imports
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.neighbors import KNeighborsClassifier
from sklearn.inspection import permutation_importance
from scipy.stats import (spearmanr, pearsonr)
import sklearn

from distutils.version import LooseVersion
if LooseVersion(sklearn.__version__) >= LooseVersion("0.24"):
    # In sklearn version 0.24, forest module changed to be private.
    from sklearn.ensemble._forest import _generate_unsampled_indices
    from sklearn.ensemble import _forest as forest
else:
    # Before sklearn version 0.24, forest was public, supporting this.
    from sklearn.ensemble.forest import _generate_unsampled_indices
    from sklearn.ensemble import forest

from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn import (manifold, decomposition, neighbors, cross_decomposition)


def get_embeddings(data, types = ['phate'], labels = None, n_components = 2, random_state = 0, n_jobs = 1):
    
    """
    This code is written to allow easy access to multiple dimensionality reduction methods.
    
    Parameters
    ----------
    data : numpy array, required, default: None
        tabular feature data in the form of a numpy array
        
    types: list, required, default: ['phate']
        A list of dimensionality reducition algorithms to be run.  Types include: 'pca', 'pls', 'lda', 'mds',
        'tsne', 'nca', 'isomap', 'lle', 'phate', 'umap', 'kpca'
        
        if type = 'all', all embeddings are computed
        
    labels: numpy array, optional for some types, default: None
        an array of labels for the data, used for supervised methods such as 'pls', and 'lda'
        
    n_components : int (>= 1), required, default: 2
        number of dimentions of the final embeddings
        
    random_state : int, optional, default: 0
        random seed for generator used in methods with random initialzations (['mds', 'tsne',
        'nca', 'lle', 'phate', 'umap'])
        
    n_jobs : int, optional, default: 1
        The number of jobs to use for the computation.
        If -1 all CPUs are used. If 1 is given, no parallel computing code is
        used at all, which is useful for debugging.
        For n_jobs below -1, (n_cpus + 1 + n_jobs) are used. Thus for
        n_jobs = -2, all CPUs but one are used
        
    Attributes
    ----------
    
    embeddings : dictionary
        a dictionary of n_component-dimensional embeddings, keys are given by the parameter 'types'
    """
    
    if types == 'all':
        types = ['pca', 'pls', 'lda', 'mds', 'tsne', 'nca', 'isomap', 'lle', 'phate', 'umap', 'kpca']
        
    embeddings = dict()
    
    if 'pca' in  types:
        embeddings['pca'] = decomposition.PCA(n_components = n_components,
                                                      random_state = random_state).fit_transform(data)
        
    if 'pls' in types:
        embeddings['pls'] = cross_decomposition.PLSRegression().fit_transform(data, labels)[0]
        
    if 'lda' in types:
        embeddings['lda'] = LinearDiscriminantAnalysis(n_components = 2).fit_transform(data, labels)
        
    if 'mds' in types:
        embeddings['mds'] = manifold.MDS(n_components = n_components,
                                        random_state = random_state,
                                        n_jobs = n_jobs).fit_transform(data)
        
    if 'tsne' in types:
        embeddings['tsne'] = manifold.TSNE(n_components = n_components, 
                                           init = 'pca', random_state = random_state, n_jobs = n_jobs).fit_transform(data)
        
    if 'nca' in types:
        embeddings['nca'] = neighbors.NeighborhoodComponentsAnalysis(init = 'random',
                                                                     n_components = n_components,
                                                                     random_state = random_state).fit_transform(data, labels)
        
    if 'isomap' in types: 
        embeddings['isomap'] = manifold.Isomap(n_neighbors = n_neighbors,
                                               n_components = n_components,
                                               n_jobs = n_jobs).fit_transform(data)
        
    if 'lle' in types:
        embeddings['lle'] = manifold.LocallyLinearEmbedding(n_neighbors = n_neighbors,
                                                            n_components = n_components,
                                                            method = 'standard', 
                                                            n_jobs = n_jobs,
                                                            random_state = random_state).fit_transform(data)
        
    if 'phate' in types:
        embeddings['phate'] = phate.PHATE(n_components = n_components,
                                         random_state = random_state).fit_transform(data)
        
    if 'umap' in types:
        embeddings['umap'] = umap.UMAP(random_state = random_state,
                                      n_components = n_components).fit_transform(data)
        
    if 'kpca' in types:
        embeddings['kpca'] = decomposition.KernelPCA(n_components = n_components, kernel = 'rbf').fit_transform(data)
    
    
    return(embeddings)


def get_rf_embeddings(proximities = None, data = None, labels = None, label_type = 'classification', 
                      types = 'phate', n_components = 2, random_state = 0, n_jobs = 1):
    
    
    """
    This code is written to allow easy access to multiple dimensionality reduction methods.
    
    Parameters
    ----------
    proximities : numpy array, default: None
        a symmetric matrix of proximities produced from a random forest
        
    data : numpy array, default: None
        an (n, d) data matrix. This is not used if proximities are provided
       
    labels : numpy array, default: None
        a (n, 1) array of data labels.  Also not used if proximities are provided
        
    labels_type : string, default:'classification'
        only needed if proximity matrix is not included.  Needed to determine classification or regression forest type.
        options are 'classification' or 'regression'
        
    types: list, required, default: ['pca']
        A list of dimensionality reducition algorithms to be run. Types include ['mds', 'tsne', 'isomap', 'phate', 'umap',
        'kpca']
        if type = 'all', all embeddings are computed
        
        
        Types include: 'pca', 'pls', 'lda', 'mds',
        'tsne', 'nca', 'isomap', 'lle', 'phate', 'umap', 'kpca'
        
        
    n_components : int (>= 1), required, default: 2
        number of dimentions of the final embeddings
        
    random_state : int, optional, default: 0
        random seed for generator used in methods with random initialzations (['mds', 'tsne', 'phate', 'umap', 'kpca',
        'nca', 'lle', 'phate', 'umap'])
        
    n_jobs : int, optional, default: 1
        The number of jobs to use for the computation.
        If -1 all CPUs are used. If 1 is given, no parallel computing code is
        used at all, which is useful for debugging.
        For n_jobs below -1, (n_cpus + 1 + n_jobs) are used. Thus for
        n_jobs = -2, all CPUs but one are used
        
    Attributes
    ----------
    
    embeddings : dictionary
        a dictionary of n_component-dimensional embeddings, keys are given by the parameter 'types'
    """
    
    embeddings = dict()
        
    if types == 'all':
        types = ['mds', 'tsne', 'phate', 'umap', 'kpca', 'nca', 'lle', 'phate', 'umap']
        
        
        
    if proximities is None:
        
        
        if data is None:
            raise ValueError('Either proximities or data is required')
            
            
        elif label_type == 'classification':
            rf = RandomForest.rf_classifier(n_estimators = 500,
                                            n_jobs = n_jobs).fit(data, labels)
            proximities = rf.get_proximities(data, method = 'oob', matrix_type = 'dense')
            embeddings['proximities'] = proximities
            
            
        elif label_type == 'regression':
            rf = RandomForest.rf_regressor(n_estimators = 500,
                                            n_jobs = n_jobs).fit(data, labels)
            proximities = rf.get_proximities(data, method = 'oob', matrix_type = 'dense')
            embeddings['proximities'] = proximities
            
        else: 
            raise ValueError('label_type must be classificaiton or regression')
        
    

    if 'phate' in types:
        embeddings['phate'] = phate.PHATE(n_components = n_components,
                                     random_state = random_state,
                                     knn_dist = 'precomputed').fit_transform(proximities)
 
    if sparse.issparse(proximities):
        proximities = proximities.todense()
        
    if 'kpca' in types:
        embeddings['kpca'] = decomposition.KernelPCA(n_components = n_components,
                                                     kernel = 'precomputed').fit_transform(proximities)
            
    if 'mds' in types:
        embeddings['mds'] = manifold.MDS(n_components = n_components,
                                        random_state = random_state,
                                        n_jobs = n_jobs,
                                        dissimilarity = 'precomputed').fit_transform(1 - proximities)
    if 'isomap' in types: 
        embeddings['isomap'] = manifold.Isomap(n_neighbors = n_neighbors,
                                               n_components = n_components,
                                               n_jobs = n_jobs,
                                              metric = 'precomputed').fit_transform(1 - proximities)
        
    if 'umap' in types:
        embeddings['umap'] = umap.UMAP(random_state = random_state,
                                      n_components = n_components,
                                      metric = 'precomputed').fit_transform(1 - proximities)
        
    if 'tsne' in types:
          
        embeddings['tsne'] = manifold.TSNE(n_components = n_components, random_state = random_state,
                                           n_jobs = n_jobs,
                                          metric = 'precomputed').fit_transform(1 - proximities)
    
    return(embeddings)

def get_importance_correlation(data, labels, embeddings, label_type = 'classification', n_jobs = 1, 
                              n_repeats = 30, random_state = 0, corr_type = 'pearson'):
    """
    This code produces the correlation between the feature importances in the data's classification / 
    regression problem and the feature importance in determining the embedding.
    
    Parameters
    ----------
    data : numpy array, default: None
        an (n, d) data matrix. This is not used if proximities are provided
       
    labels : numpy array, default: None
        a (n, 1) array of data labels.  Also not used if proximities are provided
      
      
    embeddings : numpy array, default: None
        an (n, p) embedding of the data
        
    labels_type : string, default:'classification'
        only needed if proximity matrix is not included.  Needed to determine classification or regression forest type.
        options are 'classification' or 'regression'
        
    corr_type: string, default: 'pearson'
        designation of whether Spearman or Pearson correlatoin should be used
        Please choose 'spearman' or 'pearson'
        
    n_repeats : int, default: 30
        the number of repetitions used in the kNN permutation importance
        
    random_state : int, optional, default: 0
        random seed for generator used in methods with random initialzations (['mds', 'tsne', 'phate', 'umap', 'kpca',
        'nca', 'lle', 'phate', 'umap'])
        
    n_jobs : int, optional, default: 1
        The number of jobs to use for the computation.
        If -1 all CPUs are used. If 1 is given, no parallel computing code is
        used at all, which is useful for debugging.
        For n_jobs below -1, (n_cpus + 1 + n_jobs) are used. Thus for
        n_jobs = -2, all CPUs but one are used
    
    Returns
    -------
    correlation : numeric
        the Spearman or Pearson correlation between the embedding feature importance and the prediction feature importance
    """
    emb_model = KNeighborsRegressor(weights = 'distance')
    
    if label_type == 'classification':
        model = KNeighborsClassifier()
        score = 'accuracy'
        
    elif label_type == 'regression':
        model = KNeighborsRegressor(weights = 'distance')
        score = 'r2'
        
    model.fit(data, labels)
    emb_model.fit(data, embeddings)
    
    importance = permutation_importance(model, data, labels, n_repeats = n_repeats,
                                        scoring = score,
                                        n_jobs = n_jobs, random_state = random_state)['importances_mean']
    
    emb_importance = permutation_importance(emb_model, data, embeddings,
                                            n_repeats = n_repeats,
                                            n_jobs = n_jobs,
                                            scoring = 'r2', random_state = 0)['importances_mean']
    
    if corr_type == 'pearson':
        return pearsonr(emb_importance, importance)[0]
    elif corr_type == 'spearman':
        return spearmanr(emb_importance, importance).correlation
         