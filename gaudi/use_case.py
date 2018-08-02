import sys
import traceback
import collections

from gaudi import response_object as res


class UseCaseMeta(type):
    register = {}

    def __init__(cls, clsname, bases, attrs):
        super(UseCaseMeta, cls).__init__(clsname, bases, attrs)
        if clsname != 'UseCase' and clsname.endswith('UseCase'):
            UseCaseMeta.register[clsname] = cls


class UseCase(metaclass=UseCaseMeta):
    _parameters = []

    def __init__(self, exception_on_failure=None, no_traceback=False):
        self.exception_on_failure = exception_on_failure
        self.no_traceback = no_traceback

    def execute(self, request=None):
        req = {}

        for parameter in self._parameters:
            if isinstance(parameter, collections.Mapping) and \
                    'default' in parameter:
                req[parameter['name']] = parameter['default']

        if request:
            req.update(request)

        try:
            response = self._process_request(req)
        except Exception as exc:
            if self.no_traceback:
                response = res.ResponseFailure.create_exception_error(
                    "{}: {}".format(exc.__class__.__name__, "{}".format(exc)))
            else:
                exc_type, exc_value, exc_tb = sys.exc_info()
                response = res.ResponseFailure.create_exception_error(
                    traceback.format_exception(exc_type, exc_value, exc_tb)
                )

        if response or not self.exception_on_failure:
            return response
        else:
            raise self.exception_on_failure(
                response.category,
                response.content
            )

    def _process_request(self, req):
        errors = []
        mandatory_parameters = []

        for parameter in self._parameters:
            if isinstance(parameter, collections.Mapping):
                mandatory_parameters.append(parameter['name'])
            else:
                mandatory_parameters.append(parameter)

        for mandatory_parameter in mandatory_parameters:
            if mandatory_parameter not in req.keys():
                errors.append((mandatory_parameter, "is missing"))

        if errors:
            return res.ResponseFailure.create_parameters_error(errors)

        return self.process_request(req)

    def process_request(self, req):
        return res.ResponseSuccess.create_default_success()


class UseCaseRegister:
    def __getattr__(self, attr):
        clsname = attr + "UseCase"
        return UseCaseMeta.register[clsname]


class UseCaseCreator(UseCaseRegister):
    def __init__(self, use_case_parameters=None):
        super().__init__()
        self.use_case_parameters = use_case_parameters or {}

    def __getattr__(self, attr):
        cls = super().__getattr__(attr)
        return cls(**self.use_case_parameters)


class UseCaseExecutor(UseCaseCreator):

    def __getattr__(self, attr):
        use_case = super().__getattr__(attr)
        return use_case.execute
