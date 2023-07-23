from django.shortcuts import get_object_or_404
from rest_framework import serializers, status
from rest_framework.response import Response


class CreateDeleteAPIViewMixin:
    """Mixin for endpoints that create and delete instances."""
    serializer_class = None
    model_name = None

    def post(self, request, recipe_id):
        serializer = self.serializer_view(
            data={'user': request.user.id, 'recipe': recipe_id}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            data=serializer.data,
            status=status.HTTP_201_CREATED
        )

    def delete(self, request, recipe_id):
        object = get_object_or_404(
            self.database_view,
            user=request.user.id,
            recipe=recipe_id
        )
        object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MixinCreateSerializer(serializers.ModelSerializer):
    """Mixin serializer that create instances in models and
        use for representation other serializer.
    """
    def __init__(self):
        self.serializer = None
        super(MixinCreateSerializer).__init__()

    class Meta:
        model = None
        fields = (
            'user',
        )

    def to_representation(self, instance):
        request = self.context.get('request')
        return self.serializer(
            instance, context={'request': request}
        ).data
