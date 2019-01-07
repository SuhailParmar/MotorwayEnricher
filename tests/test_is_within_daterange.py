from lib.utils import Utils
from dateutil.parser import parse
from datetime import timedelta

ut = Utils()
t = parse("2018-10-17T08:54:13Z")
from_ts = t - timedelta(hours=2)
until_ts = t + timedelta(hours=2)


class TestDateranges:

    def test_not_within_date_boundary_minutes_under(self):
        # 1 minute over
        test = parse("2018-10-17T06:53:13Z")
        assert ut.within_daterange(test, from_ts, until_ts) is False

    def test_not_within_date_boundary_minutes_over(self):
        # 1 minute over
        test = parse("2018-10-17T10:55:13Z")
        assert ut.within_daterange(test, from_ts, until_ts) is False

    def test_not_within_date_boundary_hours_over(self):
        # 1 minute over
        test = parse("2018-10-17T14:54:13Z")
        assert ut.within_daterange(test, from_ts, until_ts) is False

    def test_not_within_date_boundary_hours_under(self):
        # 1 minute over
        test = parse("2018-10-17T05:54:13Z")
        assert ut.within_daterange(test, from_ts, until_ts) is False

    def test_within_date_boundary_on_lower(self):
        # 1 minute over
        test = parse("2018-10-17T06:54:13Z")
        assert ut.within_daterange(test, from_ts, until_ts)

    def test_within_date_boundary(self):
        # 1 minute over
        test = parse("2018-10-17T09:10:13Z")
        assert ut.within_daterange(test, from_ts, until_ts)

    def test_within_date_boundary_on_higher(self):
        # 1 minute over
        test = parse("2018-10-17T10:54:13Z")
        assert ut.within_daterange(test, from_ts, until_ts)
