from bson import ObjectId
import pytest
from starlette import status


@pytest.fixture
def update_image_api(api_client):
    def _update_image(image_id: str, body: dict, url=None, expected_status=status.HTTP_200_OK):
        response = api_client.patch(
            url or f"/api/v1/images/{image_id}",
            json=body,
        )
        assert response.status_code == expected_status
        return response

    return _update_image


class TestImageUpdate:
    def test_partial_update_image_success(self, mongodb, update_image_api):
        """
        Tests that request for getting groups works fine
        """

        result = update_image_api(image_id="61fbaf25671c45f3f5f4074c", body={"status": "review"})

        data = result.json()
        assert data["id"] == "61fbaf25671c45f3f5f4074c"
        assert data["status"] == "review"
        assert mongodb["images"].find_one({"_id": ObjectId("61fbaf25671c45f3f5f4074c")})["status"] == "review"
