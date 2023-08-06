import paddle
import numpy as np

from jina import Executor, requests


class PaddleMwuExecutor(Executor):
    def __init__(self, **kwargs):
        super().__init__()
        self.dims = 5
        self.encoding_mat = paddle.to_tensor(np.random.rand(self.dims, self.dims))

    @requests
    def encode(self, docs, **kwargs):
        for doc in docs:
            _input = paddle.to_tensor(doc.blob)
            _output = _input.matmul(self.encoding_mat)
            doc.embedding = np.array(_output)


from jina import Flow, Document

f = Flow().add(uses=PaddleMwuExecutor)

with f:
    f.post(on='/', inputs=Document(content=np.random.rand(3, 5)), on_done=print)
