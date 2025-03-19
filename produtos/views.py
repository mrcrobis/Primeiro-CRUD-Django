from django.shortcuts import render, redirect, get_object_or_404
from .models import Produto
from .forms import ProdutoForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

@login_required
def lista_produtos(request):
    produtos = Produto.objects.all()

    nome = request.GET.get('nome', '')
    preco_min = request.GET.get('preco_min', '')
    preco_max = request.GET.get('preco_max', '')
    data_inicio = request.GET.get('data_inicio', '')
    data_fim = request.GET.get('data_fim', '')

    if nome:
        produtos = produtos.filter(nome__icontains=nome)

    if preco_min:
        produtos = produtos.filter(preco__gte=preco_min)
    if preco_max:
        produtos = produtos.filter(preco__lte=preco_max)

    if data_inicio:
        produtos = produtos.filter(data_criacao__gte=data_inicio)
    if data_fim:
        produtos = produtos.filter(data_criacao__lte=data_fim)

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
def editar_produto(request, id):

    produto = Produto.objects.get(Produto, id=id)

    if produto.usuario != request.user:
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
def excluir_produto(request, id):
    produto = Produto.objects.get(Produto, id=id)
    
    if produto.usuario != request.user:
        return HttpResponseForbidden("Você não tem permissão para excluir este produto.")
    
    produto.delete()
    return redirect('lista_produtos')