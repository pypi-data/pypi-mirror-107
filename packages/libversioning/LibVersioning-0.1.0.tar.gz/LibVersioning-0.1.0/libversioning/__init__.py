import typing as _typing

import re as _re



class VersionModifier():
    PRE_RELEASE       = 0
    RELEASE_CANDIDATE = 1
    SNAPSHOT          = 2

    def __init__(self, modifier: int) -> None:
        self.modifier = modifier

    def __repr__(self) -> str:
        for modifier in dir(self):
            if (getattr(self, modifier) == self.modifier):
                return(modifier)

    def __mini__(self) -> str:
        return({
            self.PRE_RELEASE       : 'pre',
            self.RELEASE_CANDIDATE : 'rc',
            self.SNAPSHOT          : 'snap'
        }[self.modifier])



class Version():
    def __init__(self, *args) -> None:
        if (len(args) == 0 or len(args) >= 6):
            raise(TypeError('`Version` takes 1~3 integer arguments, and optionally 1 modifier and integer argument'))


        if (len(args) == 1):
            if (isinstance(args[0], str)):
                pattern = _re.fullmatch('([0-9]+)(?:\\.([0-9]+)(?:\\.([0-9]+))?)?(?:-(pre|rc|snap)([0-9]+)?)?', args[0])
                if (pattern == None):
                    raise(ValueError(f'`{args[0]}` is not a valid version number.'))

                self.major    = int(pattern.group(1))
                self.minor    = int(pattern.group(2) or 0)
                self.patch    = int(pattern.group(3) or 0)
                self.modifier = pattern.group(4) or None
                if (isinstance(self.modifier, str)):
                    self.modifier = VersionModifier({
                        'pre'  : VersionModifier.PRE_RELEASE,
                        'rc'   : VersionModifier.RELEASE_CANDIDATE,
                        'snap' : VersionModifier.SNAPSHOT
                    }[self.modifier])
                self.modvalue = pattern.group(5) or (None if self.modifier == None else 0)
                if (isinstance(self.modvalue, str)):
                    self.modvalue = int(self.modvalue)

            elif (isinstance(args[0], int)):
                self.major = args[0]


        elif (len(args) >= 2 and len(args) <= 5):
            self.minor    = 0
            self.patch    = 0
            self.modifier = None
            self.modvalue = None

            index = 0
            requiredType = []
            for arg in args:
                requiredType = []

                if (index == 0):
                    requiredType = [int]

                elif (index >= 1 and index <= 2):
                    if (self.modifier == None):
                        requiredType = [int, VersionModifier]
                    elif (self.modvalue == None):
                        requiredType = [int]

                elif (index >= 3 and index <= 4):
                    if (self.modifier == None):
                        requiredType = [VersionModifier]
                    elif (self.modvalue == None):
                        requiredType = [int]

                requiredType = tuple(requiredType)


                if (not isinstance(arg, requiredType)):
                    if (len(requiredType) == 0):
                        requiredType = 'void'
                    elif (len(requiredType) == 1):
                        requiredType = requiredType[0].__name__
                    else:
                        requiredType = f'Union[{", ".join(requiredType)}]'
                    raise(TypeError(f'Argument {index} must be of type {requiredType}'))


                if (index == 0):
                    self.major = arg

                elif (index >= 1 and index <= 2):
                    if (self.modifier == None):
                        if (isinstance(arg, int)):
                            if (index == 1):
                                self.minor = arg
                            elif (index == 2):
                                self.patch = arg
                    elif (self.modvalue == None):
                        self.modvalue = arg

                elif (index >= 3 and index <= 4):
                    if (self.modifier == None):
                        self.modifier = arg
                    elif (self.modvalue == None):
                        self.modvalue = arg


                index += 1


            if (self.modifier != None):
                if (self.modvalue == None):
                    self.modvalue = 0



    def __repr__(self):
        res = f'{self.major}.{self.minor}'
        if (self.patch != 0):
            res += f'.{self.patch}'
        if (self.modifier != None):
            res += f'-{self.modifier.__mini__()}{self.modvalue}'
        return(res)



__version__ = Version(0, 1)
