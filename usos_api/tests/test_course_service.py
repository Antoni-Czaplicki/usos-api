from unittest.mock import AsyncMock, MagicMock

import pytest

from usos_api.services.courses import CourseService


@pytest.fixture
def mock_connection():
    conn = MagicMock()
    conn.post = AsyncMock()
    return conn


@pytest.fixture
def service(mock_connection):
    return CourseService(connection=mock_connection)


class TestGetUserCoursesEcts:
    """Tests for CourseService.get_user_courses_ects."""

    @pytest.mark.asyncio
    async def test_normal_values(self, service, mock_connection):
        """All ECTS values are non-None strings/numbers — should convert to float."""
        mock_connection.post.return_value = {
            "2024Z": {"CS101": "6", "MATH201": "4"},
            "2024L": {"PHYS101": "5"},
        }
        result = await service.get_user_courses_ects()

        assert result == {
            "2024Z": {"CS101": 6.0, "MATH201": 4.0},
            "2024L": {"PHYS101": 5.0},
        }

    @pytest.mark.asyncio
    async def test_none_ects_value_does_not_raise(self, service, mock_connection):
        """USOS API can return null for ECTS — must NOT raise TypeError."""
        mock_connection.post.return_value = {
            "2024Z": {"CS101": None, "MATH201": "4"},
        }
        result = await service.get_user_courses_ects()

        assert result["2024Z"]["CS101"] is None
        assert result["2024Z"]["MATH201"] == 4.0

    @pytest.mark.asyncio
    async def test_all_none_ects_values(self, service, mock_connection):
        """All ECTS values are None — should return None for all."""
        mock_connection.post.return_value = {
            "2024Z": {"CS101": None, "MATH201": None},
        }
        result = await service.get_user_courses_ects()

        assert result == {"2024Z": {"CS101": None, "MATH201": None}}

    @pytest.mark.asyncio
    async def test_empty_response(self, service, mock_connection):
        """Empty response from USOS — should return empty dict."""
        mock_connection.post.return_value = {}
        result = await service.get_user_courses_ects()

        assert result == {}

    @pytest.mark.asyncio
    async def test_empty_term(self, service, mock_connection):
        """Term with no courses — should return empty inner dict."""
        mock_connection.post.return_value = {"2024Z": {}}
        result = await service.get_user_courses_ects()

        assert result == {"2024Z": {}}

    @pytest.mark.asyncio
    async def test_numeric_ects_value(self, service, mock_connection):
        """ECTS returned as integer instead of string — should still work."""
        mock_connection.post.return_value = {
            "2024Z": {"CS101": 6, "MATH201": 4.5},
        }
        result = await service.get_user_courses_ects()

        assert result == {"2024Z": {"CS101": 6.0, "MATH201": 4.5}}
