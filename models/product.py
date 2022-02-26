from dataclasses import dataclass


class ProductModel:
 def __init__(self, id: int, name: str, price: float, url: str):
     self.id = id
     self.name = name
     self.price = price
     self.url = url
