import copy

import pytest
from lxml import etree


class AssertFailureRolesMixin:
    def assert_failure_roles(self, actual_failures, expected_dict):
        """Makes assertions about the failures. Specifically, their roles as well as
        what assertions they failed on

        :param actual_failures: list of Failures
        :param expected_dict: dict, keys are roles and values are the number of occurrences of that failure role
        """
        actual = failures_by_role(copy.deepcopy(actual_failures))
        expected = copy.deepcopy(expected_dict)
        for expected_role in list(expected.keys()):
            if expected[expected_role] != 0:
                assert expected_role in actual, f"Expected to find failure with role {expected_role}"
                actual_failures = actual.pop(expected_role)
                assert expected[expected_role] == len(actual_failures), f"Expected failures does not equal actual failures for role {expected_role}"
            else:
                assert expected_role not in actual, f"Expected to NOT find failure with role {expected_role}"
        
        assert len(actual) == 0, f"Expected to account for all failure roles, but found some unaccounted for: {list(actual.keys())}"


def failures_by_role(failures):
    """Returns a dict of array of failures, keyed by failure role

    :param failures: list of Failures
    :return: dict
    """
    res = {}
    for failure in failures:
        if failure.role in res:
            res[failure.role].append(failure)
        else:
            res[failure.role] = [failure]

    return res

def golden_tree(name):
    """Returns parsed lxml tree of the golden file

    :param name: str, name of the file, without any file extension
    :return: lxml.etree
    """
    golden_file = f'schematron/v2.0.0/golden_files/{name}.xml'
    return etree.parse(golden_file)
