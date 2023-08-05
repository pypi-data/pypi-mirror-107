from dataclasses import dataclass, asdict
from schema import product
import dataclasses
from typing import List, Optional, Dict, Union
import json


@dataclass
class Product:
    productID: int
    embedding: Optional[List[float]] = None
    title: Optional[str] = None
    description: Optional[str] = None
    brand: Optional[str] = None
    category: Optional[str] = None
    active: Optional[bool] = None

    def keyify(self):
        return asdict(self)


class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        return super().default(o)


def package_json_product_list(
    product_list: List[Dict[str, Union[str, List[float]]]]
        ) -> List[product.Product]:
    products: List[product.Product] = [
        product.Product(**x) for x in product_list  # type: ignore
    ]
    return products
