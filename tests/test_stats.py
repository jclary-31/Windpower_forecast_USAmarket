

import src.utils as utils
import pytest
import pandas as pd
import numpy as np

@pytest.fixture
def data4stats():
    rng=np.random.default_rng(42) #for reproducibility
    sample1=rng.normal(loc=0, scale=1, size=1000)
    sample2=rng.normal(loc=0, scale=1, size=1000)
    sample3=rng.normal(loc=0, scale=1, size=1000)
    samples=np.vstack([sample1, sample2,sample3])
    data=pd.DataFrame(samples)

    assert isinstance(data, pd.DataFrame)
    assert data.shape==(3,1000)
    assert data.mean(axis=1).mean()==pytest.approx(0, abs=0.05)
    assert data.std(axis=1).mean()==pytest.approx(1, abs=0.05)
    return data

def test_confidence_interval(data4stats):
    data=data4stats
    lower, upper=utils.confidence_interval(data,.90)
    assert lower < upper
    assert len(lower)==data.shape[0]
    assert len(upper)==data.shape[0]


def test_gaussian_density(data4stats):
    data=data4stats
    density,z=utils.gaussian_density(data,n=40)
    assert isinstance(density, np.ndarray)
    assert density.shape[0]==40
    assert z.shape[0]==40
    assert density.shape[1]==data.shape[0]
    assert np.allclose(density.sum(axis=0), np.ones(density.shape[1]),rtol=1e-4) #density should sum to 1 across all samples

