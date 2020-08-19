import pytest

from exhaust_port.models import XWing, DefenceTower

# added test for destroy Xwing
# added tests for DefenceTower

@pytest.fixture
def x_wing(admin_user):
    return XWing(
        pilot=admin_user, cost=13331.33, name="random_name", _coordinates="20305"
    )


@pytest.fixture
def defence_tower():
    return DefenceTower(
        id=1, sector=1, health=100, cost=5546123, _coordinates="20000"
    )

@pytest.mark.kuku
@pytest.mark.django_db
class TestXwing:
    def test_is_destroyed(self, x_wing):
        assert x_wing.is_destroyed(100)
        assert not x_wing.is_destroyed(99)

    def test_destroy(self, x_wing):
        x_wing.destroy()
        assert x_wing.health == 0


@pytest.mark.django_db
class TestDefenceTower:
    def test_is_destroyed(self, defence_tower):
        assert defence_tower.is_destroyed(100)
        assert not defence_tower.is_destroyed(99)

    def test_destroy(self, defence_tower):
        defence_tower.destroy()
        assert defence_tower.health == 0
