from api.business_logic.mailing_statistics import (
    get_detailed_statistics,
    get_overall_statistics,
)
from api.tests.conftest import (
    DetailedStatisticsFixture,
    OverallStatisticsFixture,
    detailed_statistics_seller_fixture,
    overall_statistics_fixture,
)


def test_detailed_statistics(
    db, detailed_statistics_seller_fixture: DetailedStatisticsFixture
):
    """Тест на формирование детальной статистики."""

    statistics = get_detailed_statistics(
        detailed_statistics_seller_fixture.input_mailing
    )
    assert statistics == detailed_statistics_seller_fixture.expected_result


def test_overall_statistics(
    db, overall_statistics_fixture: OverallStatisticsFixture
):
    """Тест на формирование общей статистики."""

    statistics = get_overall_statistics()
    assert statistics == overall_statistics_fixture.expected_result
