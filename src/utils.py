import numpy as np
from sklearn.model_selection import TimeSeriesSplit

def cross_validate(model_fn, n_splits, fit_params, X, y):
    """
    Cross validates time-series data.
    """
    tssplit = TimeSeriesSplit(n_splits=n_splits)
    results = []

    for i, (train_idx, test_idx) in enumerate(tssplit.split(X, y)):
        print(f'Fold {i}...')
        model = model_fn()
        history = model.fit(X[train_idx],
                            y[train_idx],
                            validation_data=(X[test_idx], y[test_idx]),
                            **fit_params)
        results.append(history.history)
    
    return results

def inverse_ids(ids, rng):
    """
    Finds indexes that is not in `ids` in range [0, rng]
    """
    return [i for i in range(rng) if i not in ids]

import torch
from torch.utils.data import TensorDataset, DataLoader

def to_torch_dataloader(X, y, params):
    X = torch.tensor(X).float()
    y = torch.tensor(y).squeeze().float()
    
    dataset = TensorDataset(X, y)
    return DataLoader(dataset, **params)