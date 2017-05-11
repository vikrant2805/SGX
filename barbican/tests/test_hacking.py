#    Copyright 2016 GohighSec
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import textwrap

import ddt
import mock
import pep8

from barbican.hacking import checks
from barbican.tests import utils


@ddt.ddt
class HackingTestCase(utils.BaseTestCase):
    """Hacking test cases

    This class tests the hacking checks in barbican.hacking.checks by passing
    strings to the check methods like the pep8/flake8 parser would. The parser
    loops over each line in the file and then passes the parameters to the
    check method. The parameter names in the check method dictate what type of
    object is passed to the check method. The parameter types are::

        logical_line: A processed line with the following modifications:
            - Multi-line statements converted to a single line.
            - Stripped left and right.
            - Contents of strings replaced with "xxx" of same length.
            - Comments removed.
        physical_line: Raw line of text from the input file.
        lines: a list of the raw lines from the input file
        tokens: the tokens that contribute to this logical line
        line_number: line number in the input file
        total_lines: number of lines in the input file
        blank_lines: blank lines before this one
        indent_char: indentation character in this file (" " or "\t")
        indent_level: indentation (with tabs expanded to multiples of 8)
        previous_indent_level: indentation on previous line
        previous_logical: previous logical line
        filename: Path of the file being run through pep8

    When running a test on a check method the return will be False/None if
    there is no violation in the sample input. If there is an error a tuple is
    returned with a position in the line, and a message. So to check the result
    just assertTrue if the check is expected to fail and assertFalse if it
    should pass.
    """

    # We are patching pep8 so that only the check under test is actually
    # installed.
    @mock.patch('pep8._checks',
                {'physical_line': {}, 'logical_line': {}, 'tree': {}})
    def _run_check(self, code, checker, filename=None):
        pep8.register_check(checker)

        lines = textwrap.dedent(code).strip().splitlines(True)

        checker = pep8.Checker(filename=filename, lines=lines)
        checker.check_all()
        checker.report._deferred_print.sort()
        return checker.report._deferred_print

    def _assert_has_errors(self, code, checker, expected_errors=None,
                           filename=None):
        actual_errors = [e[:3] for e in
                         self._run_check(code, checker, filename)]
        self.assertEqual(expected_errors or [], actual_errors)

    def _assert_has_no_errors(self, code, checker, filename=None):
        self._assert_has_errors(code, checker, filename=filename)

    def test_logging_format_no_tuple_arguments(self):
        checker = checks.CheckLoggingFormatArgs
        code = """
               import logging
               LOG = logging.getLogger()
               LOG.info("Message without a second argument.")
               LOG.critical("Message with %s arguments.", 'two')
               LOG.debug("Volume %s caught fire and is at %d degrees C and"
                         " climbing.", 'volume1', 500)
               """
        self._assert_has_no_errors(code, checker)

    @ddt.data(*checks.CheckLoggingFormatArgs.LOG_METHODS)
    def test_logging_with_tuple_argument(self, log_method):
        checker = checks.CheckLoggingFormatArgs
        code = """
               import logging
               LOG = logging.getLogger()
               LOG.{0}("Volume %s caught fire and is at %d degrees C and "
                      "climbing.", ('volume1', 500))
               """
        self._assert_has_errors(code.format(log_method), checker,
                                expected_errors=[(4, 21, 'B310')])

    def test_str_on_exception(self):

        checker = checks.CheckForStrUnicodeExc
        code = """
               def f(a, b):
                   try:
                       p = str(a) + str(b)
                   except ValueError as e:
                       p = str(e)
                   return p
               """
        errors = [(5, 16, 'B314')]
        self._assert_has_errors(code, checker, expected_errors=errors)

    def test_no_str_unicode_on_exception(self):
        checker = checks.CheckForStrUnicodeExc
        code = """
               def f(a, b):
                   try:
                       p = unicode(a) + str(b)
                   except ValueError as e:
                       p = e
                   return p
               """
        self._assert_has_no_errors(code, checker)

    def test_unicode_on_exception(self):
        checker = checks.CheckForStrUnicodeExc
        code = """
               def f(a, b):
                   try:
                       p = str(a) + str(b)
                   except ValueError as e:
                       p = unicode(e)
                   return p
               """
        errors = [(5, 20, 'B314')]
        self._assert_has_errors(code, checker, expected_errors=errors)

    def test_str_on_multiple_exceptions(self):
        checker = checks.CheckForStrUnicodeExc
        code = """
               def f(a, b):
                   try:
                       p = str(a) + str(b)
                   except ValueError as e:
                       try:
                           p  = unicode(a) + unicode(b)
                       except ValueError as ve:
                           p = str(e) + str(ve)
                       p = e
                   return p
               """
        errors = [(8, 20, 'B314'), (8, 29, 'B314')]
        self._assert_has_errors(code, checker, expected_errors=errors)

    def test_str_unicode_on_multiple_exceptions(self):
        checker = checks.CheckForStrUnicodeExc
        code = """
               def f(a, b):
                   try:
                       p = str(a) + str(b)
                   except ValueError as e:
                       try:
                           p  = unicode(a) + unicode(b)
                       except ValueError as ve:
                           p = str(e) + unicode(ve)
                       p = str(e)
                   return p
               """
        errors = [(8, 20, 'B314'), (8, 33, 'B314'), (9, 16, 'B314')]
        self._assert_has_errors(code, checker, expected_errors=errors)

    def test_dict_constructor_with_list_copy(self):
        self.assertEqual(1, len(list(checks.dict_constructor_with_list_copy(
            "    dict([(i, connect_info[i])"))))

        self.assertEqual(1, len(list(checks.dict_constructor_with_list_copy(
            "    attrs = dict([(k, _from_json(v))"))))

        self.assertEqual(1, len(list(checks.dict_constructor_with_list_copy(
            "        type_names = dict((value, key) for key, value in"))))

        self.assertEqual(1, len(list(checks.dict_constructor_with_list_copy(
            "   dict((value, key) for key, value in"))))

        self.assertEqual(1, len(list(checks.dict_constructor_with_list_copy(
            "foo(param=dict((k, v) for k, v in bar.items()))"))))

        self.assertEqual(1, len(list(checks.dict_constructor_with_list_copy(
            " dict([[i,i] for i in range(3)])"))))

        self.assertEqual(1, len(list(checks.dict_constructor_with_list_copy(
            "  dd = dict([i,i] for i in range(3))"))))

        self.assertEqual(0, len(list(checks.dict_constructor_with_list_copy(
            "        create_kwargs = dict(snapshot=snapshot,"))))

        self.assertEqual(0, len(list(checks.dict_constructor_with_list_copy(
            "      self._render_dict(xml, data_el, data.__dict__)"))))

    def test_no_xrange(self):
        self.assertEqual(1, len(list(checks.no_xrange("xrange(45)"))))

        self.assertEqual(0, len(list(checks.no_xrange("range(45)"))))

    def test_validate_assertTrue(self):
        test_value = True
        self.assertEqual(0, len(list(checks.validate_assertTrue(
            "assertTrue(True)"))))
        self.assertEqual(1, len(list(checks.validate_assertTrue(
            "assertEqual(True, %s)" % test_value))))

    def test_validate_assertIsNone(self):
        test_value = None
        self.assertEqual(0, len(list(checks.validate_assertIsNone(
            "assertIsNone(None)"))))
        self.assertEqual(1, len(list(checks.validate_assertIsNone(
            "assertEqual(None, %s)" % test_value))))

    def test_validate_assertIsNotNone(self):
        test_value = None
        self.assertEqual(0, len(list(checks.validate_assertIsNotNone(
            "assertIsNotNone(NotNone)"))))
        self.assertEqual(1, len(list(checks.validate_assertIsNotNone(
            "assertNotEqual(None, %s)" % test_value))))
        self.assertEqual(1, len(list(checks.validate_assertIsNotNone(
            "assertIsNot(None, %s)" % test_value))))

    def test_no_log_warn_check(self):
        self.assertEqual(0, len(list(checks.no_log_warn_check(
            "LOG.warning('This should not trigger LOG.warn"
            "hacking check.')"))))
        self.assertEqual(1, len(list(checks.no_log_warn_check(
            "LOG.warn('We should not use LOG.warn')"))))
