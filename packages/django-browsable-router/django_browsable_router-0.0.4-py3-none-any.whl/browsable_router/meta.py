"""Metadata classes."""

from rest_framework.serializers import HiddenField, Serializer, ListSerializer
from rest_framework.request import clone_request, Request
from rest_framework.metadata import SimpleMetadata
from rest_framework.mixins import ListModelMixin


__all__ = [
    "APIMetadata",
    "SerializerAsOutputMetadata",
]


class APIMetadata(SimpleMetadata):
    """Metadata class that adds input and output info for each of the attached views methods based on
    the serializer for that method. """

    recognized_methods = {"GET", "POST", "PUT", "PATCH", "DELETE"}

    def determine_actions(self, request: Request, view):
        """Return information about the fields that are accepted for methods in self.recognized_methods."""
        actions = {}
        for method in self.recognized_methods & set(view.allowed_methods):
            view.request = clone_request(request, method)
            many = isinstance(view, ListModelMixin) or getattr(view.get_serializer_class(), "many", False)
            serializer = view.get_serializer(many=many)
            actions[method] = self.get_serializer_info(serializer)
            view.request = request

        return actions

    def get_serializer_info(self, serializer: Serializer):
        """Given an instance of a serializer, return a dictionary of metadata about its fields."""
        input_serializer = getattr(serializer, "child", serializer)

        input_data = {
            field_name: self.get_field_info(field)
            for field_name, field in input_serializer.fields.items()
            if not isinstance(field, HiddenField)
        }

        if isinstance(serializer, ListSerializer):
            input_data = [input_data]

        # Get output from OutputSerializer or 'output_data' attribute.
        output_data = getattr(input_serializer, "output_metadata", {})
        if output_serializer_class := getattr(input_serializer, "OutputSerializer", False):

            # Check from special attribute "many" to see if the output is supposed
            # have many-to-many relationship and construct serializer accordingly
            many = getattr(output_serializer_class, "many", False)
            output_serializer_parent = output_serializer_class(many=many)

            output_serializer = getattr(output_serializer_parent, "child", output_serializer_parent)

            output_data = {
                field_name: self.get_field_info(field)
                for field_name, field in output_serializer.fields.items()
                if not isinstance(field, HiddenField)
            }

            if isinstance(output_serializer_parent, ListSerializer):
                output_data = [output_data]

        return {"input": input_data, "output": output_data}

    def get_field_info(self, field):
        if getattr(field, "child", False):
            return [self.get_field_info(field.child)]
        elif getattr(field, "fields", False):
            return self.get_serializer_info(field)["input"]
        else:
            return super().get_field_info(field)


class SerializerAsOutputMetadata(APIMetadata):
    """Metadata class that presumes that view serializer is used as response data with no request data."""

    def get_serializer_info(self, serializer: Serializer):
        output_serializer = getattr(serializer, "child", serializer)

        output_data = {
            field_name: self.get_field_info(field)
            for field_name, field in output_serializer.fields.items()
            if not isinstance(field, HiddenField)
        }

        if isinstance(serializer, ListSerializer):
            output_data = [output_data]

        return {"input": {}, "output": output_data}

    def get_field_info(self, field):
        if getattr(field, "child", False):
            return [self.get_field_info(field.child)]
        elif getattr(field, "fields", False):
            return self.get_serializer_info(field)["output"]
        else:
            return super().get_field_info(field)