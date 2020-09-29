from copy import deepcopy


AVAILABLE_SYMBOLS = ['(', ')', '>', '<', '=', '<=', '>=', 'OR', 'AND',
                     '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.']
AVAILABLE_VARIABLES = ['revenue', 'cost', 'profit', 'clicks', 'CPC', 'ROI', 'CR', 'EPC', 'leads']


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
    def _all_symbols_is_correct(condition):
        condition_copy = deepcopy(condition)

        for symbol in AVAILABLE_SYMBOLS:
            condition_copy = condition_copy.replace(symbol, '')
        for variable in AVAILABLE_VARIABLES:
            condition_copy = condition_copy.replace(variable, '')

        return len(condition_copy.replace(' ', '')) == 0

    @staticmethod
    def _split_into_parts(condition):
        condition_copy = deepcopy(condition)

        tokens = list(condition_copy)
        intervals = []
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
        print(first_part)
        print(conn)
        print(second_part)

        return first_part, conn, second_part

    @staticmethod
    def check(condition, campaign_id, landing=None):
        if not ConditionParser.is_valid(condition):
            return False

        # term recursion branch
        if 'OR' not in condition and 'AND' not in condition:
            pass

        condition = condition[1:-1]

        first_cond, conn, second_cond = ConditionParser._split_into_parts(condition)

        if conn == 'AND':
            return ConditionParser.check(first_cond, campaign_id) and ConditionParser.check(second_cond, campaign_id)
        else:
            return ConditionParser.check(first_cond, campaign_id) or ConditionParser.check(second_cond, campaign_id)

    @staticmethod
    def is_valid(condition):
        if not ConditionParser.bracket_sequence_is_valid(condition):
            return False

        if not ConditionParser._all_symbols_is_correct(condition):
            return False

        return True


print(ConditionParser.check("(((revenue < 50) AND (profit < 0)) OR (cost > 100))", 0))
