from src.bayesian import bayesian_update

def test_bayesian_update_no_data_returns_prior():
    assert bayesian_update(0.5, 0, 0) == 0.5

def test_bayesian_update_changes_prob():
    result = bayesian_update(0.5, 5, 10)
    assert 0 <= result <= 1
