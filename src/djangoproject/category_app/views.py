from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.viewsets import ViewSet

from .repository import DjangoORMCategoryRepository
from ...core.category.application.list_categories import ListCategoriesRequest, ListCategories


class CategoryViewSet(ViewSet):
    def list(self, request: Request) -> Response:
        repository = DjangoORMCategoryRepository()
        use_case = ListCategories(repository)
        categories_response = use_case.execute()

        response_data = [
            {
                "id": str(category.id),
                "name": category.name,
                "description": category.description,
                "is_active": category.is_activate
            } for category in categories_response.data
        ]

        return Response(status=HTTP_200_OK, data=response_data)
