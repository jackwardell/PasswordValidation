class FormatXY:
    def __init__(self, string):
        self.string = string
        self.formatted_string = (
            f" {string} ".replace(" x ", " {x} ").replace(" y ", " {y} ").strip()
        )

    def __call__(self, x, y):
        x, y = self.make_evaluable(x, y)
        return self.formatted_string.format(x=x, y=y)

    @staticmethod
    def make_evaluable(*args):
        return tuple(f'"{i}"' if isinstance(i, str) else i for i in args)


def statement(text: str):
    def decorator(func):
        func.statement = text
        func.format_statement = FormatXY(text)
        return func

    return decorator


@statement("x >= y")
def greater_than_or_equal_to(x, y) -> bool:
    """x (actual), y (requirement)"""
    return x >= y


@statement("x <= y")
def less_than_or_equal_to(x, y) -> bool:
    """x (actual), y (requirement)"""
    return x <= y


@statement("x not in y")
def not_in(x, y) -> bool:
    """x (actual), y (requirement)"""
    return x not in y
