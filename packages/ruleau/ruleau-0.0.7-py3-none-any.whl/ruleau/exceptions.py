class TopLevelRuleRequiresNameException(Exception):
    """Exception raised if top level aggregators don't have a human readable name"""

    pass


class MethodNotAllowedException(Exception):
    """Exception raised if a forbidden RuleauDict method is called"""

    pass


class CaseIdRequiredException(Exception):
    """Exception raised if a json path for case identifier is not found"""

    pass


class CannotOverrideException(Exception):
    """Exception raised if a API tries to override a rule marked as NO_OVERRIDE"""


class DuplicateRuleNameException(Exception):
    """Exception raised if more than 1 rule has same name"""

    pass
