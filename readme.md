```yaml
  - repo: https://github.com/trim21/pre-commit-hooks
    rev: 'v0.5.1'
    hooks:
      - id: find-trailing-comma
      - id: force-yaml-file-ext
        args: [-e, yml]


      # deprecated, use `--check` args with `poetry-lock`
      # from official repo https://github.com/python-poetry/poetry
      # - id: poetry-check-lock
```


## find-trailing-comma

find trailing comma like this in python

```python
a = 1, # not ok
b = (1, ) # ok
c = {1, 2,
     3, 4}, # not ok
d = ['element'][0, ] # not ok because it's a tuple in `[]`
e = 1, 2, 3, # ok, not a single element
```
