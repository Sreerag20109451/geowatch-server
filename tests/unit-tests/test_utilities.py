import unittest
import datetime

from utility.earthengineutilities import create_date_range, create_legend


class UtilityTests(unittest.TestCase):
    """
    End date -yesterday
    Start date - yesterday - delta
    Convert the date to YYYY-MM-DD formats

    """
    def test_custom_date_range(self):
        now_date = datetime.datetime.now().date() - datetime.timedelta(days=1)
        now_date_formatted = f"{now_date.year}-{now_date.month:02d}-{now_date.day:02d}"
        delta = 10
        delta_starttm = now_date - datetime.timedelta(days=delta)
        delta_starttm_formatted = f"{delta_starttm.year}-{delta_starttm.month:02d}-{delta_starttm.day:02d}"

        daterange = create_date_range(delta)
        self.assertEqual(len(daterange), 2)
        self.assertEqual(daterange[0], delta_starttm_formatted)
        self.assertEqual(daterange[1], now_date_formatted)


def test_legend(self):
    legend_test_data = {
        'palette': ['red', 'green', 'yellow', 'green'],
        'min': 0,
        'max': 80
    }
    legend = create_legend(legend_test_data, 'Test legend')



if __name__ == '__main__':
    unittest.main()
