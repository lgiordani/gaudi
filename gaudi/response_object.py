DEFAULT_SUCCESS = 'DEFAULT_SUCCESS'
USE_CASE_ERROR = 'USE_CASE_ERROR'
PARAMETERS_ERROR = 'PARAMETERS_ERROR'
EXCEPTION_ERROR = 'EXCEPTION_ERROR'


class Response:

    def __init__(self, boolean_value, category, content=None):
        self.boolean_value = boolean_value
        self.category = category
        self.content = content

    def __bool__(self):
        return self.boolean_value

    def __repr__(self):
        return "{} {} {}".format(
            super().__repr__(),
            self.category,
            self.content
        )  # pragma: no cover


class ResponseSuccess:

    def __init__(self, *args, **kwds):
        raise NotImplementedError

    @classmethod
    def create(cls, category, content=None):
        return Response(True, category, content)

    @classmethod
    def create_default_success(cls, content=None):
        return Response(True, DEFAULT_SUCCESS, content)


class ResponseFailure:

    def __init__(self, *args, **kwds):
        raise NotImplementedError

    @classmethod
    def create(cls, category, content=None):
        return Response(False, category, content)

    @classmethod
    def create_use_case_error(cls, content=None):
        return cls.create(USE_CASE_ERROR, content)

    @classmethod
    def create_exception_error(cls, content=None):
        return cls.create(EXCEPTION_ERROR, content)

    @classmethod
    def create_parameters_error(cls, content=None):
        return cls.create(PARAMETERS_ERROR, content)
