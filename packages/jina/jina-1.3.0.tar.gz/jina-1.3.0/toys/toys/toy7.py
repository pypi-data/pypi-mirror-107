from jina import Flow, Document
import numpy as np
from itertools import product

f = (Flow()
     .add(name='encoding_pod',
          uses='''
jtype: FilterVectorIndexer
with:
    - index_tags
        - color
        - category
''')
     .add(name='encoding_pod_no_filtering',
          uses='NumpyIndexer'))

colors = ('red', 'blue')
categories = ('dress', 't-shirt')
docs = [
    Document(chunks=[
        Document(embedding=np.random.rand(5), tags={'color': _color, 'category': _ctg}),
    ]) for _color, _ctg in product(colors, categories)]

with f:
    f.index(docs)
    f.search(Document(embedding=docs[0].embedding),
             queryset={'tags__color: red, tags__category: dress'})
