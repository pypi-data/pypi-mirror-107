from pprint import pprint

from ruleau import All, OverrideLevel, execute, rule
from ruleau.adapter import ApiAdapter
from ruleau.rule import Rule


# create a rule
@rule(name="over_18")
def over_18(context, payload):
    """
    Check applicant over 18
    >>> age(None, {"age": 18})
    True
    >>> age(None, {"age": 17})
    False
    """
    return "age" in payload and payload["age"] >= 18


@rule(name="over_18")
def not_short(context, payload):
    """
    Check applicant isn't short
    """
    return "height" in payload and payload["height"] == "tall"


collection = All(
    "Top level", All("sub level", over_18, All("sub sub level", not_short))
)

# create a payload (the answers to the rule's questions)
payload = {"age": 17, "height": "tall", "case_id": "testing-xx"}
api_adapter = ApiAdapter(base_url="http://localhost:8000/")
# send the results
result = execute(
    collection,
    payload,
    # api_adapter=api_adapter,
    case_id_jsonpath="$.case_id",
)
print(f"result: {result.result}")
