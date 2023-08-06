# RF-PHATE

RF-PHATE provides code used in the paper, "Random Forest-based Diffusion Information Geometry for Supervised Visualization and Data Exploration"
The code may be used to generate random forest proximities which may, in turn, be used in multiple dimensionality-reduction algorithms.

## Installation

```bash
pip install rf_phate
```

## Usage

```python
from rf_phate import RandomForest, Embeddings

# Creates a random forest classifier object
rf = RandomForest.rf_classifier(n_estimators = 500, n_jobs = -2).fit(X, y)

# Generates random forest proximities based on the data matrix X
proximities = rf.get_proximities(X, method = 'oob', matrix_type = 'sparse')

# Generates the RF-PHATE embeddings
rf_phate = get_rf_embeddings(proximities, label_type = 'classification', types = 'phate',
				n_components = 2, random_state = 0, n_jobs = -2)

importance_correlation = get_importance_correlation(X, y, rf_phate)
```

## License
[GNU]