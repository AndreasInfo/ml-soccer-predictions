import numpy as np
import modules.features as feat


def test_num_features():
    unique = np.unique(feat.num_features())
    assert len(unique) == len(feat.num_features())

    for f in feat.num_features():
        assert isinstance(f, str)

    NO_OF_NUM_FEAT = 327
    assert len(feat.num_features()) == NO_OF_NUM_FEAT


def test_cat_features():
    unique = np.unique(feat.cat_features())
    assert len(unique) == len(feat.cat_features())

    for f in feat.cat_features():
        assert isinstance(f, str)

    NO_OF_CAT_FEAT = 13
    assert len(feat.cat_features()) == NO_OF_CAT_FEAT


def test_unusable_features():
    unique = np.unique(feat.unusable_features())
    assert len(unique) == len(feat.unusable_features())

    for f in feat.unusable_features():
        assert isinstance(f, str)

    NO_OF_CAT_FEAT = 21
    assert len(feat.unusable_features()) == NO_OF_CAT_FEAT


def test_label():
    assert isinstance(feat.label(), str)
