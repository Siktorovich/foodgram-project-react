import io

from reportlab.pdfbase import pdfmetrics, ttfonts
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, inch

from api.permissions import OwnerSuperUserOrReadOnly
from api.mixins import (
    CreateDeleteAPIViewMixin
)
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

from django.db.models import Sum
from django.shortcuts import get_object_or_404
from django.http import FileResponse

from recipes.models import (
    Cart,
    Favorite,
    Ingredient,
    IngredientRecipe,
    Recipe,
    Subscriber,
    Tag,
)

from rest_framework import (
    decorators,
    exceptions,
    mixins,
    permissions,
    response,
    status,
    views,
    viewsets
)


class ListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    pass


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeInitialSerializer
    permission_classes = (OwnerSuperUserOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    # def perform_update(self, serializer):
    #     if serializer.instance.author != self.request.user:
    #         raise exceptions.PermissionDenied('You are not author of this recipe')
    #     super(RecipeViewSet, self).perform_update(serializer)

    # def perform_destroy(self, instance):
    #     if instance.author != self.request.user:
    #         raise exceptions.PermissionDenied('You are not author of this recipe')
    #     super(RecipeViewSet, self).perform_destroy(instance)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return RecipeRepresentSerializer
        return RecipeInitialSerializer


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (permissions.AllowAny,)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)



class SubscribeView(views.APIView):
    def post(self, request, user_id):
        serializer = SubscribeUserSerializer(
            data={'user_id': request.user.id, 'subscriber_id': user_id}
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
            user_id=request.user.id,
            subscriber_id=user_id
        )
        subscribe.delete()
        return response.Response(status=status.HTTP_204_NO_CONTENT)


class SubscribeList(ListViewSet):
    serializer_class = SubscribeSerializer

    def get_queryset(self):
        return Subscriber.objects.filter(user_id=self.request.user)


class FavoriteView(CreateDeleteAPIViewMixin, views.APIView):
    serializer_view = FavoriteCreateSerializer
    database_view = Favorite


class CartView(CreateDeleteAPIViewMixin, views.APIView):
    serializer_view = CartCreateSerializer
    database_view = Cart


@decorators.api_view(['GET'])
def download_shopping_cart(request):
    buffer = io.BytesIO()
    pdfmetrics.registerFont(ttfonts.TTFont('Arial', 'static/arial.ttf'))
    my_canvas = canvas.Canvas(buffer, pagesize=letter, bottomup=0)
    text = my_canvas.beginText()
    text.setTextOrigin(inch, inch)
    text.setFont(
        psfontname='Arial',
        size=16
    )
    ingredients = IngredientRecipe.objects.filter(
        recipe_id__cart__user_id=request.user
    ).values(
        'ingredient_id__name',
        'ingredient_id__measurement_unit',
    ).annotate(amount=Sum('amount')).order_by()

    for ingredient in ingredients:
        name = ingredient['ingredient_id__name']
        measurement_unit = ingredient['ingredient_id__measurement_unit']
        amount = ingredient['amount']
        line = f'{name} {amount} {measurement_unit}'
        text.textLine(line)
    
    my_canvas.drawText(text)
    my_canvas.showPage()
    my_canvas.save()
    buffer.seek(0)
    return FileResponse(
        buffer,
        as_attachment=True,
        filename='your_shop_list.pdf',
        content_type='application/pdf',
    )
