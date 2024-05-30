from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.viewsets import ViewSet


class CategoryViewSet(ViewSet):
    def list(self, request: Request) -> Response:
        print(request)
        return Response(status=HTTP_200_OK, data=[])
