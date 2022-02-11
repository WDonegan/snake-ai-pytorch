import pytest
import source2.pygame_utils as pgu
from source2.pygame_utils import CallbackManager, KeypressCallbackManager
from source2.pygame_utils import random_location, blit


class TestCallbackManager:
    @pytest.fixture(scope='class')
    def cbm(self) -> CallbackManager:
        return CallbackManager()

    @staticmethod
    def func_1():
        return 'This is a function #1'

    @staticmethod
    def func_2():
        return 'This is a function #2'

    @staticmethod
    def func_3():
        return 'This is a function #3'

    def test_default_value(self, cbm):
        assert cbm.callbacks == {}

    def test_execute_empty(self, cbm):
        assert cbm.execute() is not True

    def test_add(self, cbm):
        cbm.add('test1', self.func_1)
        cbm.add('test2', self.func_2)
        cbm.add('test3', self.func_3)
        assert cbm.count == 3

    def test_add_existing_fails(self, cbm):
        cbm.add('test1', self.func_3())
        assert cbm.count == 3
        assert cbm['test1'] == self.func_1

    def test_update(self, cbm):
        cbm.update('test1', self.func_3)
        assert cbm.count == 3
        assert cbm['test1'] == self.func_3

    def test_execute(self, cbm):
        assert cbm.execute("test2")

    def test_execute_all(self, cbm):
        assert cbm.execute()

    def test_remove(self, cbm):
        cbm.remove('test1')
        assert cbm.count == 2

    def test_remove_non_existent(self, cbm):
        cbm.remove('abcd')
        assert cbm.count == 2

    def test_remove_all(self, cbm):
        cbm.remove_all()
        assert cbm.count == 0
