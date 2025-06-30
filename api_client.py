import requests

API_URL = "http://localhost:3000/produtos"  # ou sua rota da API JSON Server

def listar():
    return requests.get(API_URL).json()

def criar(item):
    return requests.post(API_URL, json=item).json()

def alterar(item_id, item):
    return requests.put(f"{API_URL}/{item_id}", json=item).json()

def deletar(item_id):
    return requests.delete(f"{API_URL}/{item_id}")
