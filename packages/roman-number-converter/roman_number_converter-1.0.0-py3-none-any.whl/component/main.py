class RomanConverter:
    # noinspection PyMethodMayBeStatic
    def decode(self, roman):
        """
        Calculate the numeric value of a Roman numeral (in capital letters)

        :param roman: roman number
        :return: arabic number
        """
        trans = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
        values = [trans[r] for r in roman]
        return sum(
            val if val >= next_val else -val
            for val, next_val in zip(values[:-1], values[1:])
        ) + values[-1]

    def _encode_digit(self, digit, one, five, nine):
        """
        Encodes one digit as roman letters

        :param digit: arabic digit
        :param one: roman number representing 1
        :param five: roman number representing 5
        :param nine: roman number representing 9
        :return: roman letters
        """
        return (
            nine if digit == 9 else
            five + one * (digit - 5) if digit >= 5 else
            one + five if digit == 4 else
            one * digit
        )

    # noinspection PyMethodMayBeStatic
    def encode(self, num):
        """
        Calculate Roman number value from number

        :param num: arabic number
        :return: roman number representing arabic number
        """


        num = int(num)
        return (
                'M' * (num // 1000) +
                self._encode_digit((num // 100) % 10, 'C', 'D', 'CM') +
                self._encode_digit((num // 10) % 10, 'X', 'L', 'XC') +
                self._encode_digit(num % 10, 'I', 'V', 'IX')
        )
