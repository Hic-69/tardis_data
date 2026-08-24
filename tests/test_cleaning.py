"""Tests du module de nettoyage.

Ces tests tournent en CI et servent de filet : si quelqu'un modifie le
parsing, ils cassent avant que les notebooks produisent des donnees fausses.
"""

import pandas as pd
import pytest

from tardis import cleaning, config


class TestToNumeric:
    @pytest.mark.parametrize(
        ("raw", "expected"),
        [
            ("5,04", 5.04),
            ("6.7 min", 6.7),
            ("9.52%", 9.52),
            (" 6.51 ", 6.51),
            ("141.0", 141.0),
            ("-12,5", -12.5),
        ],
    )
    def test_parses_dirty_numbers(self, raw, expected):
        result = cleaning.to_numeric(pd.Series([raw]))
        assert result.iloc[0] == pytest.approx(expected)

    def test_unparseable_becomes_nan(self):
        result = cleaning.to_numeric(pd.Series(["abc", None, ""]))
        assert result.isna().all()


class TestParseDates:
    @pytest.mark.parametrize(
        ("raw", "year", "month"),
        [
            ("2018-01", 2018, 1),
            ("2018 01", 2018, 1),
            ("2018/01", 2018, 1),
            ("01-2018", 2018, 1),
            ("2025-10 ", 2025, 10),
        ],
    )
    def test_parses_every_known_format(self, raw, year, month):
        result = cleaning.parse_dates(pd.Series([raw]))
        assert result.iloc[0].year == year
        assert result.iloc[0].month == month

    def test_garbage_becomes_nat(self):
        result = cleaning.parse_dates(pd.Series(["pas une date"]))
        assert pd.isna(result.iloc[0])


class TestNormalizeStation:
    def test_uppercases_and_strips(self):
        result = cleaning.normalize_station(pd.Series([" paris lyon "]))
        assert result.iloc[0] == "PARIS LYON"

    def test_collapses_inner_spaces(self):
        result = cleaning.normalize_station(pd.Series(["PARIS    NORD"]))
        assert result.iloc[0] == "PARIS NORD"

    def test_applies_aliases(self):
        result = cleaning.normalize_station(pd.Series(["Angers St Laud"]))
        assert result.iloc[0] == "ANGERS SAINT LAUD"

    def test_junk_becomes_na(self):
        result = cleaning.normalize_station(pd.Series(["0", "  "]))
        assert result.isna().all()


class TestBusinessRules:
    def test_cancelled_above_scheduled_is_nulled(self):
        df = pd.DataFrame(
            {
                config.COL_SCHEDULED: [100.0],
                config.COL_CANCELLED: [150.0],
            }
        )
        result = cleaning.fix_business_rules(df)
        assert pd.isna(result[config.COL_CANCELLED].iloc[0])

    def test_negative_counts_are_nulled(self):
        df = pd.DataFrame({"Number of trains delayed > 30min": [-44.0, 12.0]})
        result = cleaning.fix_business_rules(df)
        assert pd.isna(result.iloc[0, 0])
        assert result.iloc[1, 0] == 12.0

    def test_slightly_negative_delay_is_kept(self):
        # Un train en avance de 2 minutes est plausible, pas une erreur.
        df = pd.DataFrame({config.TARGET: [-2.0, -472.0]})
        result = cleaning.fix_business_rules(df)
        assert result[config.TARGET].iloc[0] == -2.0
        assert pd.isna(result[config.TARGET].iloc[1])


class TestDropDuplicates:
    def test_removes_logical_duplicates(self):
        df = pd.DataFrame(
            {
                config.COL_DATE: ["2018-01", "2018-01"],
                config.COL_DEPARTURE: ["LE MANS", "LE MANS"],
                config.COL_ARRIVAL: ["PARIS MONTPARNASSE", "PARIS MONTPARNASSE"],
                config.TARGET: [5.0, 7.0],
            }
        )
        assert len(cleaning.drop_duplicates(df)) == 1


class TestConfigIntegrity:
    def test_target_is_not_listed_as_leaky(self):
        # Sinon build_feature_matrix supprimerait la cible elle-meme.
        assert config.TARGET not in config.LEAKY_COLUMNS
