from uuid import UUID

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from rest_framework.viewsets import ViewSet

from .repository import DjangoORMCategoryRepository
from ...core.category.application.exceptions import CategoryNotFound
from ...core.category.application.get_category import GetCategory, GetCategoryRequest
from ...core.category.application.list_categories import ListCategories


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

    def retrieve(self, request: Request, pk=None) -> Response:
        try:
            category_id = UUID(pk)
        except ValueError:
            return Response(status=HTTP_400_BAD_REQUEST)

        use_case = GetCategory(DjangoORMCategoryRepository())
        try:
            category = use_case.execute(request=GetCategoryRequest(id=category_id))
        except CategoryNotFound:
            return Response(status=HTTP_404_NOT_FOUND)

        category_output = {
            "id": str(category.id),
            "name": category.name,
            "description": category.description,
            "is_active": category.is_active
        }

        return Response(status=HTTP_200_OK, data=category_output)
