from datetime import datetime, timedelta

import pandas as pd
import pytz

CET = pytz.timezone('CET')
UTC = pytz.timezone('UTC')


def from_date_to_datetime(date):
    return datetime(date.year, date.month, date.day)


def convert_date_to_utc(aware_date: datetime) -> datetime:
    return aware_date.astimezone(pytz.utc)


def localize_to_utc(local_naive_date: datetime) -> datetime:
    utc_tz = pytz.utc
    return utc_tz.localize(local_naive_date)


def localize_to_cet(local_naive_date: datetime) -> datetime:
    be_tz = pytz.timezone('Europe/Brussels')
    return be_tz.localize(local_naive_date)


def create_datetime_range(start_datetime: datetime, end_datetime: datetime, freq: str) -> pd.DataFrame:
    datetime_index = pd.date_range(start=start_datetime, end=end_datetime, freq=freq, closed='left')
    df = pd.DataFrame(data=datetime_index, columns=['delivery_start'])
    df['delivery_start'] = df['delivery_start'].dt.tz_convert("UTC")
    df['delivery_end'] = df['delivery_start'] + (datetime_index.values[1] - datetime_index.values[0])
    df["delivery_date"] = df["delivery_start"].dt.tz_convert('CET').dt.strftime("%Y-%m-%d")
    return df


def to_utc_iso_string(date_string: str):
    return datetime.fromisoformat(date_string.replace('Z', '+00:00')).astimezone(pytz.utc).isoformat()


def get_current_time_cet():
    return datetime.now(CET)


def get_current_time_utc():
    # ALSO: datetime.now(UTC)
    return UTC.localize(datetime.utcnow())


def today_in_cet(str_format=False):
    today = datetime.now(pytz.timezone('CET')).replace(minute=0, hour=0, second=0, microsecond=0)
    if str_format:
        return today.strftime("%Y-%m-%d")
    return today


def tomorrow_in_cet(str_format=False):
    tomorrow = today_in_cet() + timedelta(days=1)
    if str_format:
        return tomorrow.strftime("%Y-%m-%d")
    return tomorrow


def shift_to_previous_qh(dt: datetime):
    """ Given a datetime object, set the value of its minutes attribute back to the previous quarter """
    return datetime(dt.year, dt.month, dt.day, dt.hour, 15 * (dt.minute // 15), tzinfo=dt.tzinfo)


def now_in_utc():
    return datetime.now(tz=UTC)


def now_in_cet():
    return datetime.now(tz=CET)
