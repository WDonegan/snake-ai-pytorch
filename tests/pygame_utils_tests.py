import pytest
import source2.pygame_utils as pgu
from source2.pygame_utils import CallbackManager, KeypressCallbackManager
from source2.pygame_utils import random_location, blit


@pytest.fixture(scope='module')
def tf1():  # Callback for testing purposes
    return lambda: '#1 - This is for testing purposes only'


@pytest.fixture(scope='module')
def tf2():  # Callback for testing purposes
    return lambda: '#2 - This is for testing purposes only'


class TestCallbackManager:
    @pytest.fixture(scope='class')
    def cbm_init(self) -> CallbackManager:
        yield CallbackManager()

    @pytest.fixture()
    def cbm(self, cbm_init) -> CallbackManager:
        cbm_init.clear()
        yield cbm_init

    def test_default_value(self, cbm):
        assert cbm.callbacks == {}

    def test_add(self, cbm, tf1, tf2):
        cbm.add('t1', tf1)
        cbm.add('t2', tf2)
        assert cbm.count == 2

    def test_add_none(self, cbm):
        cbm.add('', None)
        assert cbm.count == 0

    def test_add_doesnt_update(self, cbm, tf1, tf2):
        cbm.add('t1', tf1)  # Add
        cbm.add('t1', tf2)  # Attempt Overwrite
        assert cbm.count == 1
        assert cbm['t1'] == tf1  # Verify NOT overridden

    def test_update(self, cbm, tf1, tf2):
        cbm.add('t1', tf1)  # Add
        cbm.update('t1', tf2)
        assert cbm.count == 1
        assert cbm['t1'] == tf2

    def test_update_none(self, cbm):
        cbm.update('', None)
        assert cbm.count == 0

    def test_remove(self, cbm, tf1):
        cbm.add('t1', tf1)  # Add
        cbm.remove('t1')
        assert cbm.count == 0

    def test_clear(self, cbm, tf1, tf2):
        cbm.add('t1', tf1)  # Add
        cbm.add('t2', tf2)  # Add
        cbm.clear()
        assert cbm.count == 0

    def test_execute(self, cbm, tf1, tf2):
        cbm.add('t1', tf1)  # Add
        assert cbm.execute('t1')

    def test_execute_all(self, cbm, tf1, tf2):
        cbm.add('t1', tf1)  # Add
        cbm.add('t2', tf2)  # Add
        assert cbm.execute_all()

    def test_execute_empty(self, cbm):
        assert cbm.execute('t1') is not True
        assert cbm.execute_all() is not True


class TestKeypressCallbackManager:
    @pytest.fixture(scope='class')
    def kpm_init(self) -> KeypressCallbackManager:
        yield KeypressCallbackManager()

    @pytest.fixture()
    def kpm(self, kpm_init):
        kpm_init.clear()
        yield kpm_init

    def test_default_value(self, kpm):
        assert kpm.key_callbacks == {}

    def test_register_key(self, kpm):
        kpm.register_key(1)
        assert kpm.count == 1
        assert kpm[1].count == 0

    def test_register_key_existing(self, kpm):
        kpm.register_key(1)
        kpm.register_key(1)
        assert kpm.count == 1
        assert kpm[1].count == 0

    def test_register_key_unique(self, kpm):
        kpm.register_key(1)
        kpm.register_key(2)
        assert kpm.count == 2
        assert kpm[1].count == 0
        assert kpm[2].count == 0

    def test_register_key_none(self, kpm):
        kpm.register_key(None)
        assert kpm.count == 0

    def test_unregister_key(self, kpm):
        kpm.register_key(1)
        kpm.unregister_key(1)
        assert not kpm.__contains__(1)
        assert kpm.count == 0

    def test_register_cbk(self, kpm, tf1, tf2):
        pass
