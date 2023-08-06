import typing as _typing

__version__ = '0.1.0'



def separate(bitwiseValue) -> _typing.List:
    value = bitwiseValue.value
    values = []

    while (value >= 1):
        id = 1
        while (id <= value):
            id *= 2
        id = int(id / 2)
        valueName = None
        for key, val in bitwiseValue.bitwiseClass.__values__.items():
            if (getattr(bitwiseValue.bitwiseClass, key).value == id):
                valueName = key
                break
        if (valueName == None):
            raise(ValueError('This bitwise dataclass is corrupted.'))
        values.append(Value(bitwiseValue.bitwiseClass, [valueName], id))
        value -= id

    return(sorted(values))



def has(bitwiseValue, hasValue) -> bool:
    separated = bitwiseValue.separate()
    return(any([hasValue.value == i.value for i in separated]))



class Value():
    def __init__(self, bitwiseClass, valueName: _typing.List[str], value: int) -> None:
        self.bitwiseClass = bitwiseClass
        self.valueName = valueName
        self.value = value


    def __repr__(self) -> str:
        return(f'<{type(self.bitwiseClass).__name__} ({"|".join(self.valueName)})>')


    def __or__(self, other):
        if (not isinstance(other, type(self))):
            raise(TypeError(f'unsupported operand type(s) for |: \'{type(self).__name__}\' and \'{type(other).__name__}\''))
        elif (self.bitwiseClass != other.bitwiseClass):
            raise(TypeError(f'unsupported operand type(s) for |: \'{self.__bitwiseType__}\' and \'{other.__bitwiseType__}\''))

        value = Value(self.bitwiseClass, self.valueName + other.valueName, self.value | other.value)
        return(value)


    def __lt__(self, other):
        return(self.value < other.value)


    def __bitwiseType__(self) -> str:
        return(f'{type(self).__name__}:{type(self.bitwiseClass).__name__}')


    def separate(self) -> _typing.List:
        return(separate(self))


    def has(self, hasValue) -> bool:
        return(has(self, hasValue))



def dataclass(bitwiseClass):
    annotations = bitwiseClass.__annotations__
    values = []

    for key, value in annotations.items():
        if (value == Value):
            values.append(key)

    bitwiseClass = bitwiseClass()
    bitwiseClass.__annotations__ = {}
    bitwiseClass.__values__ = {}

    id = 1
    for value in values:
        bitwiseValue = Value(bitwiseClass, [value], id)
        setattr(bitwiseClass, value, bitwiseValue)
        bitwiseClass.__values__[value] = id
        id *= 2

    bitwiseClass.separate = separate
    bitwiseClass.has = has

    return(bitwiseClass)
