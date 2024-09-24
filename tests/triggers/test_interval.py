from __future__ import annotations

from datetime import datetime, timedelta

import pytest

from apscheduler.triggers.interval import IntervalTrigger


def test_bad_interval():
    exc = pytest.raises(ValueError, IntervalTrigger)
    exc.match("The time interval must be positive")


def test_bad_end_time(timezone):
    start_time = datetime(2020, 5, 16, tzinfo=timezone)
    end_time = datetime(2020, 5, 15, tzinfo=timezone)
    exc = pytest.raises(
        ValueError, IntervalTrigger, seconds=1, start_time=start_time, end_time=end_time
    )
    exc.match("end_time cannot be earlier than start_time")


def test_end_time(timezone, serializer):
    start_time = datetime(2020, 5, 16, 19, 32, 44, 649521, tzinfo=timezone)
    end_time = datetime(2020, 5, 16, 22, 33, 1, tzinfo=timezone)
    interval = timedelta(hours=1, seconds=6)
    trigger = IntervalTrigger(
        start_time=start_time, end_time=end_time, hours=1, seconds=6
    )
    assert trigger.next() == start_time

    if serializer:
        trigger = serializer.deserialize(serializer.serialize(trigger))

    assert trigger.next() == start_time + interval
    assert trigger.next() == start_time + interval * 2
    assert trigger.next() is None


def test_repr(timezone, serializer):
    start_time = datetime(2020, 5, 15, 12, 55, 32, 954032, tzinfo=timezone)
    end_time = datetime(2020, 6, 4, 16, 18, 49, 306942, tzinfo=timezone)
    trigger = IntervalTrigger(
        weeks=1,
        days=2,
        hours=3,
        minutes=4,
        seconds=5,
        milliseconds=1234,
        microseconds=123525,
        start_time=start_time,
        end_time=end_time,
    )
    if serializer:
        trigger = serializer.deserialize(serializer.serialize(trigger))

    assert repr(trigger) == (
        "IntervalTrigger(weeks=1, days=2, hours=3, minutes=4, seconds=5, milliseconds=1234, "
        "microseconds=123525, start_time='2020-05-15 12:55:32.954032+02:00', "
        "end_time='2020-06-04 16:18:49.306942+02:00')"
    )


def test_interval_property():
    trigger = IntervalTrigger(
        weeks=1,
        days=2,
        hours=3,
        minutes=4,
        seconds=5,
        milliseconds=1234,
        microseconds=123525,
    )
    assert trigger.interval == timedelta(
        weeks=1,
        days=2,
        hours=3,
        minutes=4,
        seconds=5,
        milliseconds=1234,
        microseconds=123525,
    )


def test_interval_setter():
    trigger = IntervalTrigger(
        seconds=1,
    )
    interval = timedelta(
        weeks=1,
        days=2,
        hours=3,
        minutes=4,
        seconds=5,
        milliseconds=1234,
        microseconds=123525,
    )
    trigger.interval = interval
    assert trigger.interval == interval


def test_fields_from_interval_setter():
    interval = timedelta(
        weeks=47,
        days=9,
        hours=27,
        minutes=64,
        seconds=65,
        milliseconds=1234,
        microseconds=1525,
    )
    trigger = IntervalTrigger(seconds=1)
    trigger.interval = interval
    assert trigger.weeks == 48
    assert trigger.days == 3
    assert trigger.hours == 4
    assert trigger.minutes == 5
    assert trigger.seconds == 6
    assert trigger.milliseconds == 235
    assert trigger.microseconds == 525
