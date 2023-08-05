from schema import product
from typing import List, Dict


def package_embeddings(embedding_list: List[product.Product]
                       ) -> Dict[int, product.Product]:
    return {
        p.productID: p for p in embedding_list
    }
