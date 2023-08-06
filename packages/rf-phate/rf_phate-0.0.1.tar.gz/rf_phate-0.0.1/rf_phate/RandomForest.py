# Imports
import numpy as np
import pandas as pd
from scipy import sparse

#sklearn imports
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import RandomForestRegressor
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


# In[32]:


class rf_classifier(RandomForestClassifier):

    """
    This class takes on a random forest predictors (sklearn) and addes methods to 
    construct proximities from the random forest object. 

    Note: most methods here will not work until your forst is fit.  That is, use 
    rf_classifier.fit(X, y) prior to generating proximities.
    """

    def __init__(self, **kwargs):
        super().__init__()
        
    
    def _get_oob_samples(self, data):
        
      """
      This is a helper function for get_oob_indices. 
      
      Parameters
      ----------
      data : (n, d) array_like (numeric)
      
      """
      n = len(data)
      oob_samples = []
      for tree in self.estimators_:
    
        # Here at each iteration we obtain out of bag samples for every tree.
        oob_indices = _generate_unsampled_indices(tree.random_state, n, n)
        oob_samples.append(oob_indices)
      return oob_samples


    #get_oob_indices proces an N x t matrix of zeros and ones to indicate oob samples in the t trees
    def get_oob_indices(self, data): #The data here is your X_train matrix
        
      """
      This generates a matrix of out-of-bag samples for each decision tree in the forest
      
      
      Parameters
      ----------
      data : (n, d) array_like (numeric)
      
      
      Returns
      -------
      oob_matrix : (n, n_estimators) array_like
      
      
      """
      n = len(data)
      num_trees = self.n_estimators
      oob_matrix = np.zeros((n, num_trees))
      oob_samples = self._get_oob_samples(data)
      for i in range(n):
        for j in range(num_trees):
          if i in oob_samples[j]:
            oob_matrix[i, j] = 1
      return oob_matrix
    
    def get_proximity_vector(self, ind, leaf_matrix, oob_indices, method = 'oob'):
        """
        This method produces a vector of proximity values for a given observation index. This is typically
        used in conjunction with get_proximities.
        
        Parameters
        ----------
        leaf_matrix : (n, n_estimators) array_like
        oob_indices : (n, n_estimators) array_like
        method      : string: methods may be 'original' or 'oob' (default)
        
        Returns
        ------
        prox_vec : (n, 1) array)_like: a vector of proximity values
        """
        n, num_trees = leaf_matrix.shape
        prox_vec = np.zeros((1, n))
        
        
        if method == 'oob':
            treeCounts = np.zeros((1, n)) 
            for t in range(num_trees): 
                if oob_indices[ind, t] == 0:
                    continue
                else:
                    index = leaf_matrix[ind, t]
                    oob_matches = leaf_matrix[:, t] * oob_indices[:, t] == index 
                    oob_obs = oob_indices[:, t] == 1
                    treeCounts[0, oob_obs] += 1
                    prox_vec[0, oob_matches] += 1

            treeCounts[treeCounts == 0] = 1
            prox_vec /= treeCounts 

            cols = np.nonzero(prox_vec)[1]
            rows = np.ones(len(cols), dtype = int) * ind
            data = prox_vec[0, cols]
            
        elif method == 'original':

            treeCounts = np.zeros((1, n)) 
            for t in range(num_trees): 

                index = leaf_matrix[ind, t]
                matches = leaf_matrix[:, t] == index
                prox_vec[0, matches] += 1
            prox_vec /= num_trees 

            cols = np.nonzero(prox_vec)[1]
            rows = np.ones(len(cols), dtype = int) * ind
            data = prox_vec[0, cols]
 
        return data.tolist(), rows.tolist(), cols.tolist()
    
    
    def get_proximities(self, data, method = 'oob', matrix_type = 'dense'):
        
        """
        This method produces a proximity matrix for the random forest object.
        
        
        Parameters
        ----------
        data : (n, d) array_like (numeric)
        method : string: methods may be 'original' or 'oob' (default)
        matrix_type: string: 'dense' (default) to return a dense matrix, 'sparse' to return a sparse crs matrix
        
        
        Returns
        -------
        prox (if matrix_type = dense) : a matrix of random forest proximities
        prox_sparse (if matrix_type = sparse) : a sparse crs_matrix of proximities
        
        """
            
        oob_indices  = self.get_oob_indices(data)
        leaf_matrix  = self.apply(data)
        n, num_trees = leaf_matrix.shape

        for i in range(n):
            if i == 0:
                prox_vals, rows, cols = self.get_proximity_vector(i, leaf_matrix, oob_indices)
            else:
                if i % 100 == 0:
                    print('Finished with {} rows'.format(i))
                prox_val_temp, rows_temp, cols_temp = self.get_proximity_vector(i, leaf_matrix, oob_indices, method = method)
                prox_vals.extend(prox_val_temp)
                rows.extend(rows_temp)
                cols.extend(cols_temp)

        prox_sparse = sparse.csr_matrix((np.array(prox_vals), (np.array(rows), np.array(cols))), shape = (n, n)) 
        
        if matrix_type == 'dense':
            return prox_sparse.todense()
        
        else:
            return prox_sparse


class rf_regressor(RandomForestRegressor):

    """
    This class takes on a random forest predictors (sklearn) and addes methods to 
    construct proximities from the random forest object. 

    Note: most methods here will not work until your forst is fit.  That is, use 
    rf_regressor.fit(X, y) prior to generating proximities.

    """

    def __init__(self, **kwargs):
        super().__init__()
        
    
    def _get_oob_samples(self, data):
        
      """
      This is a helper function for get_oob_indices. 
      
      Parameters
      ----------
      data : (n, d) array_like (numeric)
      
      """
      n = len(data)
      oob_samples = []
      for tree in self.estimators_:
    
        # Here at each iteration we obtain out of bag samples for every tree.
        oob_indices = _generate_unsampled_indices(tree.random_state, n, n)
        oob_samples.append(oob_indices)
      return oob_samples


    #get_oob_indices proces an N x t matrix of zeros and ones to indicate oob samples in the t trees
    def get_oob_indices(self, data): #The data here is your X_train matrix
        
      """
      This generates a matrix of out-of-bag samples for each decision tree in the forest
      
      
      Parameters
      ----------
      data : (n, d) array_like (numeric)
      
      
      Returns
      -------
      oob_matrix : (n, n_estimators) array_like
      
      
      """
      n = len(data)
      num_trees = self.n_estimators
      oob_matrix = np.zeros((n, num_trees))
      oob_samples = self._get_oob_samples(data)
      for i in range(n):
        for j in range(num_trees):
          if i in oob_samples[j]:
            oob_matrix[i, j] = 1
      return oob_matrix
    
    def get_proximity_vector(self, ind, leaf_matrix, oob_indices, method = 'oob'):
        """
        This method produces a vector of proximity values for a given observation index. This is typically
        used in conjunction with get_proximities.
        
        Parameters
        ----------
        leaf_matrix : (n, n_estimators) array_like
        oob_indices : (n, n_estimators) array_like
        method      : string: methods may be 'original' or 'oob' (default)
        
        Returns
        ------
        prox_vec : (n, 1) array)_like: a vector of proximity values
        """
        n, num_trees = leaf_matrix.shape
        prox_vec = np.zeros((1, n))
        
        
        if method == 'oob':
            treeCounts = np.zeros((1, n)) 
            for t in range(num_trees): 
                if oob_indices[ind, t] == 0:
                    continue
                else:
                    index = leaf_matrix[ind, t]
                    oob_matches = leaf_matrix[:, t] * oob_indices[:, t] == index 
                    oob_obs = oob_indices[:, t] == 1
                    treeCounts[0, oob_obs] += 1
                    prox_vec[0, oob_matches] += 1

            treeCounts[treeCounts == 0] = 1
            prox_vec /= treeCounts 

            cols = np.nonzero(prox_vec)[1]
            rows = np.ones(len(cols), dtype = int) * ind
            data = prox_vec[0, cols]
            
        elif method == 'original':

            treeCounts = np.zeros((1, n)) 
            for t in range(num_trees): 

                index = leaf_matrix[ind, t]
                matches = leaf_matrix[:, t] == index
                prox_vec[0, matches] += 1
            prox_vec /= num_trees 

            cols = np.nonzero(prox_vec)[1]
            rows = np.ones(len(cols), dtype = int) * ind
            data = prox_vec[0, cols]
 
        return data.tolist(), rows.tolist(), cols.tolist()
    
    
    def get_proximities(self, data, method = 'oob', matrix_type = 'dense'):
        
        """
        This method produces a proximity matrix for the random forest object.
        
        
        Parameters
        ----------
        data : (n, d) array_like (numeric)
        method : string: methods may be 'original' or 'oob' (default)
        matrix_type: string: 'dense' (default) to return a dense matrix, 'sparse' to return a sparse crs matrix
        
        
        Returns
        -------
        prox (if matrix_type = dense) : a matrix of random forest proximities
        prox_sparse (if matrix_type = sparse) : a sparse crs_matrix of proximities
        
        """
            
        oob_indices  = self.get_oob_indices(data)
        leaf_matrix  = self.apply(data)
        n, num_trees = leaf_matrix.shape

        for i in range(n):
            if i == 0:
                prox_vals, rows, cols = self.get_proximity_vector(i, leaf_matrix, oob_indices)
            else:
                if i % 100 == 0:
                    print('Finished with {} rows'.format(i))
                prox_val_temp, rows_temp, cols_temp = self.get_proximity_vector(i, leaf_matrix, oob_indices, method = method)
                prox_vals.extend(prox_val_temp)
                rows.extend(rows_temp)
                cols.extend(cols_temp)

        prox_sparse = sparse.csr_matrix((np.array(prox_vals), (np.array(rows), np.array(cols))), shape = (n, n)) 
        
        if matrix_type == 'dense':
            return prox_sparse.todense()
        
        else:
            return prox_sparse