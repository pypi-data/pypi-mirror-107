import os
from jina.executors import BaseExecutor
os.environ['VAR_A'] = 'hello-world'

# foo_exec = BaseExecutor.load_config('toy.yml')
#
# print(f'name: {foo_exec.metas.name}')
# print(f'workspace: {foo_exec.metas.workspace}')

b = BaseExecutor.load_config(
    'toy.yml', context={'VAR_A': 'hello-jina'})

c = BaseExecutor.load_config(
    'toy.yml', context={'VAR_A': 'hello-jina'},
substitute=False)

print(f'b.name: {b.metas.name}')
print(f'c.name: {c.metas.name}')
