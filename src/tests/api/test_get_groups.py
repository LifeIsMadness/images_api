import pytest
from starlette import status

from schemas.image import StatusEnum


@pytest.fixture
def get_groups_api(api_client):
    def _get_groups(url=None, expected_status=status.HTTP_200_OK):
        response = api_client.get(
            url or "/api/v1/groups",
        )
        assert response.status_code == expected_status
        return response

    return _get_groups


class TestGetGroups:
    def test_get_groups_success(self, mongodb, get_groups_api):
        """
        Tests that request for getting groups works fine
        """
        result = get_groups_api()

        data = result.json()
        assert len(data) == mongodb["groups"].count_documents({}) == 3
        assert data[0]["name"] == "group1"
        assert "images" in data[0]
        assert len(data[0]["images"]) == 2

    @pytest.mark.parametrize(
        ("url", "expected_status", "verify_result"),
        [
            ("/api/v1/groups/?page=1&page_size=10", status.HTTP_200_OK, lambda res: len(res) == 3),
            ("/api/v1/groups/?page=0&page_size=100", status.HTTP_422_UNPROCESSABLE_ENTITY, lambda res: "detail" in res),
            ("/api/v1/groups", status.HTTP_200_OK, lambda res: len(res) == 3),
            ("/api/v1/groups/?page=100&page_size=10", status.HTTP_200_OK, lambda res: len(res) == 0),
        ],
    )
    def test_pagination_works(self, mongodb, get_groups_api, url, expected_status, verify_result):
        """
        Tests that request is paginated when query params are provided
        """

        result = get_groups_api(url, expected_status=expected_status)

        data = result.json()
        assert verify_result(data)

    @pytest.mark.parametrize(
        ("image_status", "expected_status", "verify_result"),
        [
            (StatusEnum.NEW, status.HTTP_200_OK, lambda res: len(res[0]["images"]) == 2 and len(res[1]["images"]) == 0),
            (
                StatusEnum.ACCEPTED,
                status.HTTP_200_OK,
                lambda res: len(res[0]["images"]) == 0 and len(res[1]["images"]) == 1,
            ),
            (
                StatusEnum.REVIEW,
                status.HTTP_200_OK,
                lambda res: len(res[0]["images"]) == 0 and len(res[1]["images"]) == 0,
            ),
            ("not_exists", status.HTTP_422_UNPROCESSABLE_ENTITY, lambda res: "detail" in res),
        ],
    )
    def test_filter_group_image_by_status(self, mongodb, get_groups_api, image_status, expected_status, verify_result):
        """
        Tests that filtering image by status works as clock
        """

        result = get_groups_api(f"/api/v1/groups/?status={image_status}", expected_status=expected_status)

        data = result.json()
        assert verify_result(data)
