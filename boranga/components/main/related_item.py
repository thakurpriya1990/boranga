from rest_framework import serializers


class RelatedItem:
    def __init__(
        self, model_name="", identifier="", descriptor="", status="", action_url=""
    ):
        self.model_name = model_name
        self.identifier = identifier
        self.descriptor = descriptor
        self.status = status
        self.action_url = action_url


class RelatedItemsSerializer(serializers.Serializer):
    model_name = serializers.CharField()
    identifier = serializers.CharField()
    descriptor = serializers.CharField()
    status = serializers.CharField()
    action_url = serializers.CharField(allow_blank=True)
