import functools
import inspect
from hashlib import md5
from json import dumps
from typing import AnyStr, List
from uuid import UUID

from ruleau.constants import OverrideLevel
from ruleau.docs import description, parameters, title
from ruleau.exceptions import TopLevelRuleRequiresNameException


class Rule:
    def __init__(
        self,
        func,
        name: AnyStr,
        depends_on: List["Rule"],
        override_level: OverrideLevel,
        lazy_dependencies: bool,
    ):
        """
        :param func: User defined rule
        :param name: User defined human readable name of the rule
        :param depends_on: Rule dependencies
        :param override_level: Override level
        :param lazy_dependencies: Flag to switch loading of rule dependencies lazily
        """
        self.name = name
        # Validate the rule, make sure the name is always set for a rule
        self.validate()
        # Set the user defined function
        self.func = func
        self.depends_on = depends_on
        self.override_level = override_level
        self.__name__ = func.__name__
        self.lazy_dependencies = lazy_dependencies
        # Get parsed data, set a unique rule ID
        rule_hash = md5(dumps(self.parse()).encode())
        self.id = str(UUID(rule_hash.hexdigest()))

        # This preserves the original Docstring on the decorated function
        # which allows DocTest to detect the function
        functools.update_wrapper(self, func)

    def __str__(self) -> str:
        return self.__name__

    def __call__(self, *args, **kwargs) -> bool:
        return self.func(*args, **kwargs)

    def validate(self):
        """Validator to check if top level rule has a human readable name
        :raises: TopLevelRuleRequiresNameException
        """
        if not self.name or not isinstance(self.name, str):
            raise TopLevelRuleRequiresNameException()

    def parse(self):
        return {
            "function_name": self.__name__,
            "name": self.name,
            "title": title(self.__name__),
            "override_level_name": self.override_level.name,
            "override_level": self.override_level.value,
            "source": inspect.getsource(self.func),
            "docstring": self.func.__doc__,
            "description": description(self.func.__doc__),
            "parameters": parameters(self.func.__doc__),
            "dependencies": [dependent.parse() for dependent in self.depends_on],
        }
