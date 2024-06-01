from uuid import UUID

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from rest_framework.viewsets import ViewSet

from .repository import DjangoORMCategoryRepository
from .serializers import ListCategoriesResponseSerializer, RetrieveCategoryResponseSerializer, \
    RetrieveCategoryRequestSerializer, CreateCategoryRequestSerializer, CreateCategoryResponseSerializer
from ...core.category.application.create_category import CreateCategory, CreateCategoryRequest
from ...core.category.application.exceptions import CategoryNotFound
from ...core.category.application.get_category import GetCategory, GetCategoryRequest
from ...core.category.application.list_categories import ListCategories


class CategoryViewSet(ViewSet):
    def list(self, request: Request) -> Response:
        repository = DjangoORMCategoryRepository()
        use_case = ListCategories(repository)
        categories_response = use_case.execute()

        response_data = ListCategoriesResponseSerializer(categories_response)

        return Response(status=HTTP_200_OK, data=response_data.data)

    def retrieve(self, request: Request, pk=None) -> Response:
        request_serializer = RetrieveCategoryRequestSerializer(data={"id": pk})
        request_serializer.is_valid(raise_exception=True)

        use_case = GetCategory(DjangoORMCategoryRepository())
        try:
            category = use_case.execute(request=GetCategoryRequest(id=request_serializer.validated_data["id"]))
        except CategoryNotFound:
            return Response(status=HTTP_404_NOT_FOUND)

        print(category)
        response_serializer = RetrieveCategoryResponseSerializer(instance=category)

        print(response_serializer.data)
        return Response(status=HTTP_200_OK, data=response_serializer.data)

    def create(self, request: Request) -> Response:
        serializer = CreateCategoryRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        use_case = CreateCategory(DjangoORMCategoryRepository())
        created_category_id = use_case.execute(CreateCategoryRequest(**serializer.validated_data))

        response_serializer = CreateCategoryResponseSerializer(instance=created_category_id)

        return Response(
            status=201,
            data=response_serializer.data
        )
