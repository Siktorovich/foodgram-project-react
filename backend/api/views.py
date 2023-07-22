from api.filters import RecipeFilter
from api.mixins import CreateDeleteAPIViewMixin
from api.permissions import OwnerSuperUserOrReadOnly
from api.serializers import (
    CartCreateSerializer,
    FavoriteCreateSerializer,
    IngredientSerializer,
    RecipeInitialSerializer,
    RecipeRepresentSerializer,
    SubscribeSerializer,
    SubscribeUserSerializer,
    TagSerializer
)
from api.utils import creating_pdf_list

from django.db.models import Sum
from django.shortcuts import get_object_or_404

from recipes.models import (
    Cart,
    Favorite,
    Ingredient,
    IngredientRecipe,
    Recipe,
    Tag,
)

from rest_framework import (
    decorators,
    mixins,
    permissions,
    response,
    status,
    views,
    viewsets
)

from users.models import Subscriber


class ListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    pass


class RecipeViewSet(viewsets.ModelViewSet):
    """Viewset for recipes endpoint"""

    queryset = Recipe.objects.all()
    serializer_class = RecipeInitialSerializer
    permission_classes = (permissions.AllowAny,)
    http_method_names = (
        'get', 'post', 'patch', 'delete', 'retrieve', 'options'
    )
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
    """Viewset for tags endpoint"""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (OwnerSuperUserOrReadOnly,)
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Viewset for ingredients endpoint"""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    pagination_class = None


class SubscribeView(views.APIView):
    """View functions for subscribe endpoint"""

    def post(self, request, user_id):
        serializer = SubscribeUserSerializer(
            data={'user': request.user.id, 'subscriber': user_id}
        )
        if serializer.is_valid():
            serializer.save()
            return response.Response(
                data=serializer.data,
                status=status.HTTP_201_CREATED
            )
        return response.Response(
            data=serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
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
    serializer_class = SubscribeSerializer

    def get_queryset(self):
        return Subscriber.objects.filter(user=self.request.user)


class FavoriteView(CreateDeleteAPIViewMixin, views.APIView):
    """View class for favorite endpoint"""

    serializer_view = FavoriteCreateSerializer
    database_view = Favorite


class CartView(CreateDeleteAPIViewMixin, views.APIView):
    """View class for shopping_cart endpoint"""

    serializer_view = CartCreateSerializer
    database_view = Cart


@decorators.api_view(['GET'])
def download_shopping_cart(request):
    """View function for downloading shopping cart endpoint"""

    ingredients = IngredientRecipe.objects.filter(
        recipe__cart__user=request.user
    ).values(
        'ingredient__name',
        'ingredient__measurement_unit',
    ).annotate(amount=Sum('amount')).order_by()

    return creating_pdf_list(ingredients)
