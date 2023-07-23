from django.db.models import Sum
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import (decorators, mixins, permissions, response, status,
                            views, viewsets)

from api.filters import RecipeFilter
from api.mixins import CreateDeleteAPIViewMixin
from api.permissions import OwnerSuperUserOrReadOnly
from api.serializers import (CartCreateSerializer, FavoriteCreateSerializer,
                             IngredientSerializer, RecipeInitialSerializer,
                             RecipeRepresentSerializer, SubscribeSerializer,
                             SubscribeUserSerializer, TagSerializer)
from api.utils import creating_pdf_list, query_validation
from recipes.models import (Cart, Favorite, Ingredient, IngredientRecipe,
                            Recipe, Tag)
from users.models import Subscriber


class ListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    pass


class CreateUpdateRetrieveDestroyListSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    ListViewSet
):
    pass


class RecipeViewSet(CreateUpdateRetrieveDestroyListSet):
    """Viewset for recipes endpoint."""
    queryset = Recipe.objects.all()
    serializer_class = RecipeInitialSerializer
    permission_classes = (permissions.AllowAny,)
    filterset_class = RecipeFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return RecipeRepresentSerializer
        return RecipeInitialSerializer

    def get_queryset(self):
        return super().get_queryset().prefetch_related(
            'ingredient_recipes'
        )


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Viewset for tags endpoint."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (OwnerSuperUserOrReadOnly,)
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Viewset for ingredients endpoint."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    pagination_class = None
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name',)


class SubscribeView(views.APIView):
    """View functions for subscribe endpoint."""
    def post(self, request, user_id):
        recipes_limit = request.query_params.get('recipes_limit')
        if recipes_limit is not None:
            query_validation(recipes_limit)
            serializer = SubscribeUserSerializer(
                data={'user': request.user.id, 'subscriber': user_id},
                context={'request': request, 'recipes_limit': recipes_limit}
            )
        else:
            serializer = SubscribeUserSerializer(
                data={'user': request.user.id, 'subscriber': user_id}
            )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response(
            data=serializer.data,
            status=status.HTTP_201_CREATED
        )

    def delete(self, request, user_id):
        subscribe = get_object_or_404(
            Subscriber,
            user=request.user.id,
            subscriber=user_id
        )
        subscribe.delete()
        return response.Response(status=status.HTTP_204_NO_CONTENT)


class SubscribeList(ListViewSet):
    """View class for subscriptions list."""
    serializer_class = SubscribeSerializer

    def get_queryset(self):
        return Subscriber.objects.filter(user=self.request.user)

    def get_serializer_context(self):
        recipes_limit = self.request.query_params.get('recipes_limit')
        context = super().get_serializer_context()
        if recipes_limit is not None:
            query_validation(int(recipes_limit))
            context.update({
                "request": self.request,
                "recipes_limit": recipes_limit
            })
        return context


class FavoriteView(CreateDeleteAPIViewMixin, views.APIView):
    """View class for favorite endpoint."""
    serializer_view = FavoriteCreateSerializer
    database_view = Favorite


class CartView(CreateDeleteAPIViewMixin, views.APIView):
    """View class for shopping_cart endpoint."""
    serializer_view = CartCreateSerializer
    database_view = Cart


@decorators.api_view(['GET'])
def download_shopping_cart(request):
    """View function for downloading shopping cart endpoint."""
    ingredients = IngredientRecipe.objects.filter(
        recipe__cart__user=request.user
    ).values(
        'ingredient__name',
        'ingredient__measurement_unit',
    ).annotate(amount=Sum('amount')).order_by()

    return creating_pdf_list(ingredients)
