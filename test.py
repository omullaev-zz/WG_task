import random

import enum
from hamcrest import assert_that, equal_to

from base_tests import base_test
from lib.utils import random_sample


class ShipAttribute(enum.Enum):
    HULL = 'hull'
    WEAPON = 'weapon'
    ENGINE = 'engine'


def _rvalue():
    return random.randint(1, 100)


def _get_ship(db_client, ship_number):
    ship = db_client.select_condition(table="ships", condition="ship='ship-%s'" % ship_number)[0]
    return {'ship': ship[0], 'weapon': ship[1], 'hull': ship[2], 'engine': ship[3]}


def _get_ship_with_attribute(db_client, ship, attribute):
    params = {
        ShipAttribute.HULL: ["hull", "armor", "type", "capacity"],
        ShipAttribute.WEAPON: ["reload speed", "rotational speed", "diameter", "power volley", "count"],
        ShipAttribute.ENGINE: ["power", "type"]
    }
    param = db_client.select_condition(table="{0}s".format(attribute),
                                       condition="{0}='{1}'".format(attribute, ship[attribute]))[0]
    ship[attribute] = dict(zip(params[attribute], param))
    return ship


class Test(object, base_test.WgBaseTest):
    def setup(self):
        super(Test, self).setup()

        engine_params = ["power", "type"]
        weapon_params = ["reload speed", "rotational speed", "diameter", "power volley", "count"]
        hull_params = ["armor", "type", "capacity"]
        ship_params = ["weapon", "hull", "engine"]

        for i in xrange(1, 7):
            for param in random_sample(engine_params):
                self.wg_db_client.update("engines", param, _rvalue(), "engine='engine-%s'" % i)

        for i in xrange(1, 21):
            for param in random_sample(weapon_params):
                self.wg_db_client.update("weapons", param, _rvalue(), "weapon='weapon-%s'" % i)

        for i in xrange(1, 6):
            for param in random_sample(hull_params):
                self.wg_db_client.update("hulls", param, _rvalue(), "hull='hull-%s'" % i)

        for i in xrange(1, 201):
            for param in random_sample(ship_params):
                value = random.choice(self.wg_db_client.select('%ss' % param, param))[0]
                self.wg_db_client.update("ships", param, value, "ship='ship-%s'" % i)

    def test_hulls(self):
        for i in xrange(1, 201):
            yield self.check_hull, i

    def test_weapons(self):
        for i in xrange(1, 201):
            yield self.check_weapon, i

    def test_engines(self):
        for i in xrange(1, 201):
            yield self.check_engine, i

    def check_hull(self, n):
        self._check_ship_attribute(n, ShipAttribute.HULL)

    def check_weapon(self, n):
        self._check_ship_attribute(n, ShipAttribute.WEAPON)

    def check_engine(self, n):
        self._check_ship_attribute(n, ShipAttribute.ENGINE)

    def _check_ship_attribute(self, ship_number, ship_attribute):
        wg_db_ship = _get_ship(self.wg_db_client, ship_number)
        memory_db_ship = _get_ship(self.memory_db, ship_number)
        assert_that(wg_db_ship, equal_to(memory_db_ship))

        wg_db_ship = _get_ship_with_attribute(self.wg_db_client, wg_db_ship, ship_attribute)
        memory_db_ship = _get_ship_with_attribute(self.memory_db, memory_db_ship, ship_attribute)
        assert_that(wg_db_ship, equal_to(memory_db_ship))
