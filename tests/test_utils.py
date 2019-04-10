from lib.utils import Utils
from dateutil.parser import parse
from datetime import timedelta
from dateutil.tz import tzutc
from lib.document_clusterer import DocumentClusterer

documents = [
        "Lorry Caused The Accident On the m6 j25",
        "m6 incident was caused by overturned lorry",
        "Lorry is flipped over on m6",
        "m6 accident on j25 south",
        "Seems to be an accident on the m6 j25",
]

ut = Utils()
t = parse("2018-10-17T08:54:13Z")
from_ts = t - timedelta(hours=2)
until_ts = t + timedelta(hours=2)


class TestUtils:

    def test_calc_boundaries(self):
        a, b = ut.calc_daterange_boundaries(t, from_offset=0, to_offset=3)

        assert a.isoformat() == "2018-10-17T08:54:13+00:00"
        assert b.isoformat() == "2018-10-17T11:54:13+00:00"

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

    def test_timestamp_naive_datetimes(self):
        uad = '2019-01-09T09:36:52'
        parsed_timestamp = ut.parse_timestamp_with_utc(uad)
        assert parsed_timestamp.tzinfo == tzutc()
