"""API router that allows documentation and nesting itself to make a 'hyperlinked' browsable router."""

from typing import Dict, Union, Type, Callable

from django.http.request import HttpRequest
from django.http.response import HttpResponseBase
from django.urls import re_path, include, path
from django.urls.resolvers import URLResolver, URLPattern

from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter, APIRootView
from rest_framework.viewsets import ViewSetMixin, ViewSet
from rest_framework.views import APIView


__all__ = ["APIRouter"]


_urls_type = list[Union[URLResolver, URLPattern]]


# Root view docstring becomes the browsable API description, so we overwrite it here
class APIRoot(APIRootView):
    """Welcome! This is the API root."""


class APIRouter(DefaultRouter):
    """Router that will show APIViews in API root."""

    root_view_name: str = "api-root"
    APIRootView: APIRootView = APIRoot

    def __init__(self, *args, **kwargs):
        self._navigation_routes: Dict[str, "DefaultRouter"] = {}
        super(APIRouter, self).__init__(*args, **kwargs)

    @property
    def navigation_routes(self) -> Dict[str, "DefaultRouter"]:
        """Add urls from these routers to this routers urls under the root-view of the added router,
        which will be named after the given key. This enables browser navigation of the API."""
        return self._navigation_routes

    @navigation_routes.setter
    def navigation_routes(self, value: Dict[str, "DefaultRouter"]):
        self._navigation_routes = value

    def format_root_view(self, name: str, docstring: str) -> None:
        """Format the root view browsable API documentation.

        :param name: Root display name. CamelCase or snake_case to separate words.
        :param docstring: Used as view documentation.
        """
        new_root: APIRootView = type(name, (APIRootView,), {})  # noqa
        new_root.__doc__ = docstring
        self.APIRootView = new_root

    def get_routes(self, viewset: Type[Union[ViewSet, APIView]]):
        if issubclass(viewset, ViewSetMixin):
            return super().get_routes(viewset)
        return []

    def get_api_root_view(self, api_urls: _urls_type = None) -> Callable[[HttpRequest, ...], HttpResponseBase]:
        api_root_dict = {}
        list_name = self.routes[0].name

        for prefix, viewset, basename in self.registry:
            if issubclass(viewset, ViewSetMixin):
                api_root_dict[prefix] = list_name.format(basename=basename)
            else:
                api_root_dict[prefix] = basename

        for basename in self.navigation_routes:
            api_root_dict[fr"{basename}"] = basename

        return self.APIRootView.as_view(api_root_dict=api_root_dict)

    def get_urls(self) -> _urls_type:
        urls = []
        for prefix, view, basename in self.registry:
            if issubclass(view, ViewSetMixin):
                continue

            regex = r"^{prefix}{trailing_slash}$".format(prefix=prefix, trailing_slash=self.trailing_slash)

            urls.append(re_path(regex, view.as_view(), name=basename))

        urls = format_suffix_patterns(urls)

        for basename, router in self.navigation_routes.items():
            router.root_view_name = basename
            urls.append(path(f"{basename}/", include(router.urls)))

        return super().get_urls() + urls

