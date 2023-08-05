# Ruleau

A Python Rules Engine library

## Using the library

```python
from ruleau import execute, rule
from ruleau.adapter import ApiAdapter

# create a rule
@rule(name="over_18")
def over_18(context, payload):
    return "age" in payload and payload["age"] >= 18

# create a payload (the answers to the rule's questions)
payload = {"age": 17}

# execute the rule against the payload
result = execute(over_18, payload)

# integrate with the backend web API
api_adapter = ApiAdapter(base_url="http://localhost:8000/")

# send the results
result = execute(
    over_18, payload, api_adapter=api_adapter, case_id_jsonpath="$.case_id"
)
# result.result will be False due to applicant being 17

# if the rule for this case is overriden in the backend
# then running again will return True

```

### Testing Rules
Rules should be tested using [doctest](https://docs.python.org/3/library/doctest.html).

Example of these tests can be found in the [Kitchen Sink example](examples/kitchen_sink/rules.py).

## Development Notes

```bash
# install pre-commit config
pre-commit install

# test individual file
python -m pytest --log-cli-level=debug tests/test_adapter.py

# full test
make format
make lint
make test

# all together
make format_lint_test

```
