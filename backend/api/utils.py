import io

from django.http import FileResponse

from reportlab.lib.pagesizes import inch, letter
from reportlab.pdfbase import pdfmetrics, ttfonts
from reportlab.pdfgen import canvas

from rest_framework import serializers


def creating_pdf_list(ingredients):
    """Creating pdf file function"""

    buffer = io.BytesIO()
    pdfmetrics.registerFont(ttfonts.TTFont('Arial', 'static/arial.ttf'))
    my_canvas = canvas.Canvas(buffer, pagesize=letter, bottomup=0)
    text = my_canvas.beginText()
    text.setTextOrigin(inch, inch)
    text.setFont(
        psfontname='Arial',
        size=16
    )

    for index, ingredient in enumerate(ingredients):
        name = ingredient['ingredient__name']
        measurement_unit = ingredient['ingredient__measurement_unit']
        amount = ingredient['amount']
        line = f'{index+1}. {name.title()} ({measurement_unit}) - {amount}'

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


class QuerySerializer(serializers.Serializer):
    query = serializers.IntegerField(min_value=0)


def query_validation(query_param):
    query_serializer = QuerySerializer(data={"query": query_param})
    query_serializer.is_valid(raise_exception=True)
