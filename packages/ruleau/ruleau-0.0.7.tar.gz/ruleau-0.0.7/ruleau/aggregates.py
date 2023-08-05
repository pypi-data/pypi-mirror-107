from typing import AnyStr

from ruleau.decorators import rule
from ruleau.execute import ExecutionResult


def Any(name: AnyStr, *args):
    """Aggregator to implement OR operation
    Returns truthy, if any one of the rule result is truthy
    """

    @rule(name=name, depends_on=args)
    def any_aggregator(context: ExecutionResult, _):
        return any(result.result for result in context.dependant_results)

    return any_aggregator


def All(name: AnyStr, *args):
    """Aggregator to implement AND operation
    Returns truthy, if and all of the rule results are truthy
    """

    @rule(name=name, depends_on=args)
    def all_aggregator(context: ExecutionResult, _):
        return all(result.result for result in context.dependant_results)

    return all_aggregator
