import logging
from copy import deepcopy
from json import dumps
from typing import Any, AnyStr, Dict, Iterable, Optional

from jsonpath_ng import parse

from ruleau.adapter import ApiAdapter
from ruleau.constants import OverrideLevel
from ruleau.exceptions import (
    CannotOverrideException,
    CaseIdRequiredException,
    DuplicateRuleNameException,
)
from ruleau.rule import Rule
from ruleau.structures import RuleauDict

logger = logging.getLogger(__name__)


class DependantResults:
    def __init__(
        self,
        case_id: AnyStr,
        dependants: Iterable[Rule],
        payload: Dict[AnyStr, Any],
        api_adapter: Optional[ApiAdapter] = None,
        lazy: bool = False,
    ):
        self.case_id = case_id
        self.dependants = {dep.__name__: dep for dep in dependants}
        self.payload = deepcopy(payload)
        self.api_adapter = api_adapter
        self.results = {}
        if not lazy:
            for depend in dependants:
                self.run(depend.__name__)

    def run(self, name):
        """
        Run and store the result of a rule dependency
        :param name:
        :return:
        """

        if name not in self.dependants:
            raise AttributeError(
                f"Result for rule '{name}' not available, as it was not "
                f"declared as a dependency. "
                f"depends_on={dumps(list(self.dependants.keys()))}"
            )
        # If the result of rule execution is not set, run & cache it
        if name not in self.results:
            self.results[name] = execute_rule(
                self.case_id,
                self.dependants[name],
                self.payload,
                self.api_adapter,
            )
        # Return the rule execution result
        return self.results[name]

    def __getattr__(self, name):
        try:
            # Enable access to normal python properties
            return super().__getattr__(name)
        except AttributeError:
            # If an attribute wasn't found, check for the dependency
            return self.run(name)

    def __iter__(self):
        for dep in self.dependants:
            yield self.__getattr__(dep)


class ExecutionResult:
    def __init__(
        self,
        executed_rule: Rule,
        payload: RuleauDict,
        result,
        dependant_results: DependantResults,
        override: AnyStr = None,
        original_result: Optional[bool] = None,
    ):
        self.executed_rule = executed_rule
        self.payload = payload
        self.result = result
        self.override = override
        self.original_result = original_result
        self.dependant_results = dependant_results


def apply_override(
    case_id,
    executable_rule: Rule,
    execution_result: ExecutionResult,
    api_adapter: ApiAdapter,
):
    # Get overrides for the rule in a case
    override = api_adapter.fetch_override(case_id, executable_rule)

    # Apply override to the executed rule result, if any
    # Overrides should only be applied to allowed rule and if they're present
    if override:
        # Throw an exception if the backend is trying to override a NO_OVERRIDE rule
        if executable_rule.override_level == OverrideLevel.NO_OVERRIDE:
            raise CannotOverrideException(f"Cannot override {executable_rule.name}")
        else:
            # Override the rule result and set the overridden flag
            execution_result.override = override["id"]
            execution_result.original_result = execution_result.result
            execution_result.result = override["applied"]
    return execution_result


def execute_rule(
    case_id: AnyStr,
    executable_rule: Rule,
    payload: Dict[AnyStr, Any],
    api_adapter: Optional[ApiAdapter] = None,
):
    api_result = {}
    # Create the rule result so that the execution can store the result
    if api_adapter:
        api_result = api_adapter.create_result(case_id, executable_rule)
    # Prep the rule payload
    rule_payload = RuleauDict(payload)
    # Prep the dependent results
    depend_results = DependantResults(
        case_id,
        executable_rule.depends_on,
        payload,
        api_adapter,
        lazy=executable_rule.lazy_dependencies,
    )
    # Prepare execution result for context from all dependencies
    context = ExecutionResult(executable_rule, rule_payload, None, depend_results)
    # Prepare execution result for the rule to be executed
    execution_result = ExecutionResult(
        executable_rule,
        rule_payload,
        executable_rule(context, rule_payload),
        depend_results,
    )
    # Store the rule result
    if api_adapter:
        # Apply overrides on the rule result
        execution_result = apply_override(
            case_id, executable_rule, execution_result, api_adapter
        )

        api_adapter.update_result(
            case_id, executable_rule, api_result, execution_result
        )
    # Return the rule result
    return execution_result


def flatten_rules(rule: Rule, flattened_rules: list = [], order: int = 0):
    """Flatten the rule to find it's dependencies
    :param rule:
    :param flattened_rules: Output to append flattened results to
    :param order: Execution Order of the rule
    :return:
    """
    dependencies = {
        "id": rule.id,
        "rule": rule,
        "name": rule.name or rule.__name__,
        "dependencies": [],
    }
    # Check if there are any rule dependencies
    if len(rule.depends_on):
        # If yes, find the rule IDs
        for dependency in rule.depends_on:
            # Recursively flatten rules
            flatten_rules(dependency, flattened_rules, order + 1)
            # Append the rule as a dependency
            dependencies["dependencies"].append(dependency.id)
    # Set the order of the current rule
    dependencies["order"] = order
    # Append th
    flattened_rules.append(dependencies)
    return flattened_rules


def execute(
    executable_rule: Rule,
    payload: Dict[AnyStr, Any],
    case_id_jsonpath: AnyStr = None,
    case_id: Optional[AnyStr] = None,
    api_adapter: Optional[ApiAdapter] = None,
) -> ExecutionResult:
    """
    Executes the provided rule, following dependencies and
    passing in results accordingly
    """

    # If neither case_id_jsonpath or case_id are present, raise exception
    if not case_id_jsonpath and not case_id:
        raise CaseIdRequiredException()

    # If case_id is not present in parameters, find it
    if not case_id:
        case_id_results = parse(case_id_jsonpath).find(payload)
        if not case_id_results:
            raise ValueError("Case ID not found in payload")
        case_id = str(case_id_results[0].value)

    # If there's no case ID, don't run
    if not case_id:
        raise ValueError("Case ID not found")

    # Flatten the rules
    rule_hierarchy = {x["id"]: x for x in flatten_rules(executable_rule, [], 0)}
    # Validate unique rule name
    rule_names = [x["name"] for _, x in rule_hierarchy.items()]
    unique_rule_names = list(set(rule_names))
    duplicate_rule_names = {
        x: rule_names.count(x) for x in unique_rule_names if rule_names.count(x) > 1
    }
    if len(duplicate_rule_names):
        raise DuplicateRuleNameException(dumps(duplicate_rule_names))
    # If API adapter was was passed sync the case
    if api_adapter:
        # Sync the rules
        for _, hierarchy in rule_hierarchy.items():
            api_adapter.sync_rule(
                hierarchy["rule"], hierarchy["order"], hierarchy["dependencies"]
            )
        # Sync the case
        api_adapter.sync_case(case_id, executable_rule.id, payload)
    # Trigger the rule execution, from the top level rule
    return execute_rule(case_id, executable_rule, payload, api_adapter)
