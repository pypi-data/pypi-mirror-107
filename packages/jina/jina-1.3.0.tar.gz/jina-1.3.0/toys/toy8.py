from jina import Flow, Document, Executor, requests, DocumentArray


class MyExecutor(Executor):
    @requests
    def foo(self, docs, **kwargs):
        return DocumentArray([d for d in docs if d.text=='a'])


f = Flow().add(uses=MyExecutor)

with f:
    f.post(on='/', inputs=[Document(text=foo_str) for foo_str in ('a', 'b') * 3], on_done=print)

