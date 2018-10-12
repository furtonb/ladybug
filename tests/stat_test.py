# coding=utf-8

import unittest
from pytest import approx
import os
from ladybug.stat import Stat
from ladybug.designday import Ddy


class StatTestCase(unittest.TestCase):
    """Test for (ladybug/stat.py)"""

    # preparing to test.
    def setUp(self):
        """set up."""
        pass

    def tearDown(self):
        """Nothing to tear down as nothing gets written to file."""
        pass

    def test_import_stat(self):
        """Test import standard stat."""
        relative_path = './tests/stat/chicago.stat'
        abs_path = os.path.abspath(relative_path)

        stat_rel = Stat(relative_path)
        stat = Stat(abs_path)

        # Test imports don't break
        assert stat.file_path == abs_path
        assert stat_rel.file_path == os.path.normpath(relative_path)
        assert hasattr(stat, 'isStat')

    def test_stat_properties(self):
        relative_path = './tests/stat/tokyo.stat'
        stat = Stat(relative_path)

        # Test accuracy of import
        assert len(stat.header) == 10
        assert stat.location.city == 'TOKYO HYAKURI'
        assert stat.location.country == 'JPN'
        assert stat.location.source == 'IWEC Data'
        assert stat.location.station_id == '477150'
        assert stat.location.latitude == approx(36.18, rel=1e-1)
        assert stat.location.longitude == approx(140.42, rel=1e-1)
        assert stat.location.time_zone == 9
        assert stat.location.elevation == 35

        assert stat.monthly_tau_beam == \
            [0.341, 0.392, 0.48, 0.601, 0.654, 0.632, 0.553, 0.546, 0.473,
             0.423, 0.388, 0.338]
        assert stat.monthly_tau_diffuse == \
            [2.214, 1.999, 1.765, 1.546, 1.501, 1.591, 1.811, 1.827, 2.024,
             2.083, 2.105, 2.267]
        assert stat.ashrae_climate_zone == '4A'
        assert stat.koppen_climate_zone == 'Cfa'

    def test_annual_heating_design_days(self):
        relative_path = './tests/stat/chicago.stat'
        stat = Stat(relative_path)

        ann_hdd_96 = stat.annual_heating_design_day_996
        ann_hdd_90 = stat.annual_heating_design_day_990

        assert ann_hdd_96.day_type == 'WinterDesignDay'
        assert ann_hdd_96.name == '99.6% Heating Design Day for Chicago Ohare Intl Ap'
        assert ann_hdd_96.analysis_period.st_month == \
            ann_hdd_96.analysis_period.end_month == \
            ann_hdd_96.sky_condition.month == 1
        assert ann_hdd_96.analysis_period.st_day == \
            ann_hdd_96.analysis_period.end_day == 21
        assert ann_hdd_96.humidity_condition.hum_type == 'Wetbulb'
        assert ann_hdd_96.dry_bulb_condition.dry_bulb_max == \
            ann_hdd_96.humidity_condition.hum_value == -20
        assert ann_hdd_96.dry_bulb_condition.dry_bulb_range == 0
        assert ann_hdd_96.wind_condition.wind_speed == 4.9
        assert ann_hdd_96.wind_condition.wind_direction == 270
        assert ann_hdd_96.sky_condition.solar_model == 'ASHRAEClearSky'
        assert ann_hdd_96.sky_condition.clearness == 0

        assert ann_hdd_90.name == '99.0% Heating Design Day for Chicago Ohare Intl Ap'
        assert ann_hdd_90.dry_bulb_condition.dry_bulb_max == \
            ann_hdd_90.humidity_condition.hum_value == -16.6

    def test_annual_cooling_design_days(self):
        relative_path = './tests/stat/tokyo.stat'
        stat = Stat(relative_path)
        ann_cdd_04 = stat.annual_cooling_design_day_004
        ann_cdd_10 = stat.annual_cooling_design_day_010

        assert ann_cdd_04.day_type == 'SummerDesignDay'
        assert ann_cdd_04.name == '0.4% Cooling Design Day for TOKYO HYAKURI'
        assert ann_cdd_04.analysis_period.st_month == \
            ann_cdd_04.analysis_period.end_month == \
            ann_cdd_04.sky_condition.month == 8
        assert ann_cdd_04.analysis_period.st_day == \
            ann_cdd_04.analysis_period.end_day == 21
        assert ann_cdd_04.humidity_condition.hum_type == 'Wetbulb'
        assert ann_cdd_04.dry_bulb_condition.dry_bulb_max == 32.1
        assert ann_cdd_04.humidity_condition.hum_value == 26.0
        assert ann_cdd_04.dry_bulb_condition.dry_bulb_range == 7.7
        assert ann_cdd_04.wind_condition.wind_speed == 4.8
        assert ann_cdd_04.wind_condition.wind_direction == 210
        assert ann_cdd_04.sky_condition.solar_model == 'ASHRAETau'
        assert ann_cdd_04.sky_condition.tau_b == 0.546
        assert ann_cdd_04.sky_condition.tau_d == 1.827

        assert ann_cdd_10.name == '1.0% Cooling Design Day for TOKYO HYAKURI'
        assert ann_cdd_10.dry_bulb_condition.dry_bulb_max == 30.9
        assert ann_cdd_10.humidity_condition.hum_value == 25.8

    def test_monthly_cooling_design_days(self):
        relative_path = './tests/stat/chicago.stat'
        stat = Stat(relative_path)

        m_ddy_050 = stat.monthly_cooling_design_days_050
        m_ddy_100 = stat.monthly_cooling_design_days_100
        m_ddy_020 = stat.monthly_cooling_design_days_020
        m_ddy_004 = stat.monthly_cooling_design_days_004

        assert len(m_ddy_050) == len(m_ddy_100) == len(m_ddy_020) == \
            len(m_ddy_004) == 12

        ddy_path = './tests/ddy'
        ddy_name = 'chicago_monthly.ddy'
        monthly_ddy = Ddy(stat.location, m_ddy_050)
        monthly_ddy.save(ddy_path, ddy_name)


if __name__ == "__main__":
    unittest.main()
