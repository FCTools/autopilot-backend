from copy import deepcopy


AVAILABLE_SYMBOLS = ['(', ')', '>', '<', '=', '<=', '>=', 'or', 'and', 'not',
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
    def check(condition, campaign_id, landing=None):
        pass

    @staticmethod
    def is_valid(condition):
        if not ConditionParser.bracket_sequence_is_valid(condition):
            return False

        if not ConditionParser._all_symbols_is_correct(condition):
            return False

        return True


print(ConditionParser.is_valid("((profit < 0) and (clicks > 1000))"))
