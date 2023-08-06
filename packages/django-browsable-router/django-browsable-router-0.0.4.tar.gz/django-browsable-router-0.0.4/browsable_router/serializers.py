"""Base serialiers."""

from typing import Dict, Any

from rest_framework import serializers


__all__ = [
    "BaseAPISerializer",
]


class BaseAPISerializer(serializers.Serializer):
    """Base serializer that runs bound method and output validation through an OutputSerializer."""

    class OutputSerializer(serializers.Serializer):
        """Serializer that defines this serializers output."""

        many = False
        """Set many=True or subclass ListSerializer instead to indicate that output is a list."""

        def create(self, validated_data): pass
        def update(self, instance, validated_data): pass

    def validate(self, attrs):
        """Run bound service or selector method, and validate/document output through the output serializer."""
        results = self.bound_method(**attrs)

        many = getattr(self.OutputSerializer, "many", False)
        output = self.OutputSerializer(many=many, data=results)
        output.is_valid(raise_exception=True)
        data = output.validated_data
        return data

    def bound_method(self, *args, **kwargs) -> Dict[str, Any]:
        """Service or selector function to call during serialization. 'kwargs' contain all field data.
        Attached method should raise exceptions that django can handle to responses.
        """
        raise NotImplementedError("Bound method should be set.")

    def create(self, validated_data): pass
    def update(self, instance, validated_data): pass
