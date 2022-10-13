```yaml
  - repo: https://github.com/Trim21/pre-commit-hooks
    rev: ''
    hooks:
      - id: find-trailing-comma
      - id: force-yaml-file-ext
        args: [-e, yml]

      - id: poetry-check-lock # deprecated, use `--check` args with `poetry-lock` from official repo https://github.com/python-poetry/poetry
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
