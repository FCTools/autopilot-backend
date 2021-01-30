# Copyright © 2020-2021 Filthy Claws Tools - All Rights Reserved
#
# This file is part of autopilot.autopilot-backend.
#
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Author: German Yakimov <german13yakimov@gmail.com>

from copy import deepcopy


AVAILABLE_SYMBOLS = ['(', ')', '>', '<', '=', '<=', '>=', '|', '&',
                     '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.', '-']
AVAILABLE_VARIABLES = ['revenue', 'cost', 'profit', 'clicks', 'CPC', 'ROI', 'CR', 'EPC', 'leads', 'CPA']


class ConditionParser:
    @staticmethod
    def bracket_sequence_is_valid(condition):
        if condition[0] != '(' or condition[-1] != ')':
            return False

        counter = 0

        bracket_sequence = [symbol for symbol in list(deepcopy(condition)[1:-1]) if symbol in ['(', ')']]

        for bracket in bracket_sequence:
            if bracket == '(':
                counter += 1
            else:
                counter -= 1

            if counter < 0:
                return False

        return counter == 0

    @staticmethod
    def _all_symbols_are_correct(condition):
        condition_copy = deepcopy(condition).replace('AND', '&').replace('OR', '|')

        for symbol in AVAILABLE_SYMBOLS:
            condition_copy = condition_copy.replace(symbol, '')
        for variable in AVAILABLE_VARIABLES:
            condition_copy = condition_copy.replace(variable, '')

        return len(condition_copy.replace(' ', '')) == 0

    @staticmethod
    def _split_into_parts(condition):
        condition_copy = deepcopy(condition)

        tokens = list(condition_copy)
        first_condition_end = 0

        counter = 0
        for n, symbol in enumerate(tokens):
            if symbol == '(':
                counter += 1
            elif symbol == ')':
                counter -= 1

            if counter == 0:
                first_condition_end = n
                break

        first_part = condition_copy[:first_condition_end + 1]
        conn = condition_copy[first_condition_end + 1:].strip().split()[0]
        second_part = condition_copy[first_condition_end + 3 + len(conn):]

        return first_part, conn, second_part

    @staticmethod
    def is_valid(condition):
        return ConditionParser.bracket_sequence_is_valid(condition) and \
               ConditionParser._all_symbols_are_correct(condition)
