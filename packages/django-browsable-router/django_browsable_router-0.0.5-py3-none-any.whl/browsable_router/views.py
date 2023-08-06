"""Base API view that can be used with the router."""

from typing import Dict, Any, Type, Union, Literal

from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.serializers import Serializer

from .meta import APIMetadata


__all__ = ["BaseAPIView"]


method = Literal['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'HEAD', 'OPTIONS', 'TRACE']


class BaseAPIView(APIView):
    """Base view for browsable API.

    Generate views by inheriting this class and one of the mixins.
    Set the 'serializer_classes' with the appropriate key for the
    HTTP method used, and your custom serializer as the value.
    This allowes having different serializers for different HTTP methods.
    """

    serializer_classes: Dict[method, Type["Serializer"]] = {}
    status_ok: int = status.HTTP_200_OK
    metadata_class = APIMetadata

    def get_serializer(self, *args, **kwargs) -> "Serializer":
        serializer_class = self.get_serializer_class()
        kwargs.setdefault("context", self.get_serializer_context())
        return serializer_class(*args, **kwargs)

    def get_serializer_class(self) -> Type["Serializer"]:
        """Get serializer class based on request method.

        :raises KeyError: If serializer for a method was not setup in 'serializer_classes'.
        """
        try:
            return self.serializer_classes[self.request.method]
        except KeyError:
            raise KeyError(f"Serializer is not configured for method '{self.request.method}'.")

    def get_serializer_context(self) -> Dict[str, Union[Request, "BaseAPIView"]]:
        """Return serializer context, mainly for browerable api."""
        return {"request": self.request, "view": self}

    def _fallback_handle(self, request, data, *args, **kwargs) -> Dict[str, Any]:  # noqa
        """If 'run_serializer' fails to find a handle for a method, perhaps method
        was implemented without using mixins, then this handle would pass the data throught.
        """
        return data

    def run_serializer(self, request: Request, data: Dict[str, Any], *args, **kwargs) -> Response:
        data.update(**kwargs)

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        # Hook to an after serialization handle
        handle = f"handle_{self.request.method.lower()}"
        data = getattr(self, handle, self._fallback_handle)(request, data, *args, **kwargs)

        return Response(data=data, status=self.status_ok)
