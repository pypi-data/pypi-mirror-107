import pytest

import cssutils


collect_ignore = [
    'cssutils/_fetchgae.py',
    'tools',
]


@pytest.fixture(autouse=True)
def hermetic_profiles():
    """
    Ensure that tests are hermetic w.r.t. profiles.
    """
    before = list(cssutils.profile.profiles)
    yield
    assert before == cssutils.profile.profiles


@pytest.fixture
def saved_profiles(monkeypatch):
    profiles = cssutils.profiles.Profiles(log=cssutils.log)
    monkeypatch.setattr(cssutils, 'profile', profiles)
