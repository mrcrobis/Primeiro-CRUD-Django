from django.urls import path
from .views import lista_produtos, criar_produto, editar_produto, excluir_produto

urlpatterns = [
    path('', lista_produtos, name='lista_produtos'),
    path('novo/', criar_produto, name='criar_produto'),
    path('editar/<int:id>/', editar_produto, name='editar_produto'),
    path('excluir/<int:id>/', excluir_produto, name='excluir_produto'),
]
