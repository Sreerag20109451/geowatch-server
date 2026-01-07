


"""
Create date range with the specified delta
Args :Delta
Returns: a date range with the specified delta
"""
import datetime


def create_date_range(delta):
    end_dtm = datetime.datetime.now() - datetime.timedelta(days=1)
    end_date = f"{end_dtm.year}-{end_dtm.month:02d}-{end_dtm.day:02d}"

    start_dtm = end_dtm - datetime.timedelta(days=delta)
    start_date = f"{start_dtm.year}-{start_dtm.month:02d}-{start_dtm.day:02d}"

    return [start_date, end_date]






