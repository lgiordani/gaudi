import pytest

from unittest import mock

from gaudi import response_object as res
from gaudi import use_case as uc


def test_use_case_init():
    uc.UseCase()


@mock.patch('gaudi.use_case.UseCase.process_request')
def test_use_case_handles_exceptions(mock_process_request):
    mock_process_request.side_effect = ValueError('some message')

    use_case = uc.UseCase(no_traceback=True)

    response = use_case.execute()

    assert not response
    assert response.category == res.EXCEPTION_ERROR
    assert response.content == "ValueError: some message"


@mock.patch('gaudi.use_case.traceback.format_exception')
@mock.patch('gaudi.use_case.UseCase.process_request')
def test_use_case_handles_exceptions_with_traceback(
        mock_process_request, mock_traceback):
    mock_process_request.side_effect = ValueError('some message')

    use_case = uc.UseCase()

    response = use_case.execute()

    assert not response
    assert response.category == res.EXCEPTION_ERROR
    assert mock_traceback.called


@mock.patch('gaudi.use_case.UseCase.process_request')
def test_use_case_can_raise_exception_on_failure(mock_process_request):
    mock_process_request.return_value = res.ResponseFailure.create(
        'somecategory', 'somecontent'
    )

    use_case = uc.UseCase(exception_on_failure=ValueError)
    with pytest.raises(ValueError) as excinfo:
        use_case.execute()

    assert excinfo.value.args == ('somecategory', 'somecontent')


def test_use_case_execute_returns_succeess():
    use_case = uc.UseCase()
    response = use_case.execute()

    assert response
    assert response.category == res.DEFAULT_SUCCESS


def test_use_case_mandatory_parameters():
    class MyUseCase(uc.UseCase):
        _parameters = ['param1', 'param2', 'param3']

    use_case = MyUseCase()
    response = use_case.execute({'param3': 'value3'})

    assert not response
    assert response.category == res.PARAMETERS_ERROR
    assert response.content == [
        ('param1', 'is missing'),
        ('param2', 'is missing')
    ]


def test_use_case_supports_complex_parameters():
    class MyUseCase(uc.UseCase):
        _parameters = ['param1', {'name': 'param2'}]

    use_case = MyUseCase()
    response = use_case.execute({'param1': 'value1', 'param2': 'value2'})

    assert response
    assert response.category == res.DEFAULT_SUCCESS


def test_use_case_params_with_default_value_are_not_mandatory():
    class MyUseCase(uc.UseCase):
        _parameters = ['param1', {'name': 'param2', 'default': 'value2'}]

    use_case = MyUseCase()
    response = use_case.execute({'param1': 'value1'})

    assert response
    assert response.category == res.DEFAULT_SUCCESS


@mock.patch('gaudi.use_case.UseCase.process_request')
def test_use_case_params_with_default_value_are_used(mock_process_request):
    class MyUseCase(uc.UseCase):
        _parameters = ['param1', {'name': 'param2', 'default': 'value2'}]

    use_case = MyUseCase()
    use_case.execute({'param1': 'value1'})

    mock_process_request.assert_called_with({
        'param1': 'value1',
        'param2': 'value2',
    })


@mock.patch('gaudi.use_case.UseCase.process_request')
def test_use_case_params_with_default_values_can_be_overridden(
        mock_process_request):
    class MyUseCase(uc.UseCase):
        _parameters = ['param1', {'name': 'param2', 'default': 'value2'}]

    use_case = MyUseCase()
    use_case.execute({'param1': 'value1', 'param2': 'newvalue2'})

    mock_process_request.assert_called_with({
        'param1': 'value1',
        'param2': 'newvalue2',
    })


def test_use_case_meta_is_metaclass():
    assert type(uc.UseCaseMeta) == type


def test_use_case_is_not_registered():
    assert 'UseCase' not in uc.UseCaseMeta.register


def test_use_case_meta_registers_classes_that_inherit_from_usecase():
    class ATestUseCase(uc.UseCase):
        pass

    assert uc.UseCaseMeta.register['ATestUseCase'] == ATestUseCase


def test_use_case_meta_does_not_register_if_wrong_name_ending():
    class ATest(uc.UseCase):
        pass

    assert 'ATest' not in uc.UseCaseMeta.register


def test_use_case_register():
    class ATestUseCase(uc.UseCase):
        pass

    assert uc.UseCaseRegister().ATest == ATestUseCase


def test_use_case_creator_uses_parameters():
    class ATestUseCase(uc.UseCase):
        pass

    ucc = uc.UseCaseCreator({'no_traceback': True})

    assert ucc.ATest.no_traceback is True


def test_use_case_executor_executes_the_use_case():
    class ATestUseCase(uc.UseCase):
        pass

    uce = uc.UseCaseExecutor()
    with mock.patch('gaudi.use_case.UseCase.execute') as mock_execute:
        uce.ATest()

    assert mock_execute.called
