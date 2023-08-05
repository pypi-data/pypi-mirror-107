from json.decoder import JSONDecodeError
from logging import getLogger
from typing import Optional

from requests.exceptions import RequestException

from ruleau.constants import OverrideLevel
from ruleau.rule import Rule

logger = getLogger(__name__)
logger.propagate = True


def api_request(func):
    def _api_request(*args, **kwargs) -> Optional[dict]:
        try:
            return func(*args, **kwargs)
        except RequestException as e:
            logger.error(f"Request error: {e}")
        except JSONDecodeError as j:
            logger.error(f"Parsing error: {j}")
        except Exception as ex:
            logger.error(f"Exception: {ex}")
        return None

    return _api_request


def rule(
    name=None,
    depends_on=None,
    override_level=OverrideLevel.ANY_OVERRIDE,
    lazy_dependencies=False,
):
    """Decorator to encapsulate a function into a rule"""
    depends_on = depends_on or []

    def _rule(func) -> Rule:
        return Rule(func, name, depends_on, override_level, lazy_dependencies)

    return _rule
