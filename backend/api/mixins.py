from django.shortcuts import get_object_or_404

from rest_framework import serializers, status
from rest_framework.response import Response


class CreateDeleteAPIViewMixin:
    serializer_view = None
    database_view = None

    def post(self, request, recipe_id):
        serializer = self.serializer_view(
            data={'user': request.user.id, 'recipe': recipe_id}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                data=serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
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
