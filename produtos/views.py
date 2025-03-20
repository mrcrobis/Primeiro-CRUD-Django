from django.shortcuts import render, redirect, get_object_or_404
from .models import Produto
from .forms import ProdutoForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .serializers import ProdutoSerializer
from rest_framework import viewsets

@login_required
def lista_produtos(request):
    produtos = Produto.objects.filter(usuario=request.user)
    return render(request, 'produtos/lista.html', {'produtos': produtos})

@login_required
def criar_produto(request):
    if request.method == "POST":
        form = ProdutoForm(request.POST)
        if form.is_valid():
            produto = form.save(commit=False)
            produto.usuario = request.user
            produto.save()
            return redirect('lista_produtos')
    else:
        form = ProdutoForm()
    return render(request, 'produtos/form.html', {'form': form})

@login_required
def editar_produto(request, produto_id):

    produto = Produto.objects.get(id=produto_id)

    if produto.usuario != request.user:  # Verifica se o produto pertence ao usuário
        return HttpResponseForbidden("Você não tem permissão para editar este produto.")
    
    if request.method == 'POST':
        form = ProdutoForm(request.POST, instance=produto)
        if form.is_valid():
            form.save()
            return redirect('lista_produtos')
    else:
        form = ProdutoForm(instance=produto)
    
    return render(request, 'seu_app/editar_produto.html', {'form': form})

@login_required
def excluir_produto(request, produto_id):

    produto = Produto.objects.get(id=produto_id)
    
    if produto.usuario != request.user:  # Verifica se o produto pertence ao usuário
        return HttpResponseForbidden("Você não tem permissão para excluir este produto.")
    
    produto.delete()
    return redirect('lista_produtos')

class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer