import pytest

from gaudi import response_object as res


def test_response_init_no_content():
    r = res.Response(True, 'somecategory')

    assert bool(r) is True
    assert r.category == 'somecategory'


def test_response_init_no_content_false():
    r = res.Response(False, 'somecategory')

    assert bool(r) is False
    assert r.category == 'somecategory'


def test_response_init_content():
    r = res.Response(True, 'somecategory', 'somecontent')

    assert r.content == 'somecontent'


def test_response_success_cannot_be_instantiated():
    with pytest.raises(NotImplementedError):
        res.ResponseSuccess()


def test_response_success_create_no_content():
    r = res.ResponseSuccess.create('somecategory')

    assert bool(r) is True
    assert r.category == 'somecategory'


def test_response_success_create_content():
    r = res.ResponseSuccess.create('somecategory', 'somecontent')

    assert r.content == 'somecontent'


def test_response_success_create_default_success():
    r = res.ResponseSuccess.create_default_success('somecontent')

    assert bool(r) is True
    assert r.category == res.DEFAULT_SUCCESS
    assert r.content == 'somecontent'


def test_response_failure_cannot_be_instantiated():
    with pytest.raises(NotImplementedError):
        res.ResponseFailure()


def test_response_failure_create_no_content():
    r = res.ResponseFailure.create('somecategory')

    assert bool(r) is False
    assert r.category == 'somecategory'


def test_response_failure_create_content():
    r = res.ResponseFailure.create('somecategory', 'somecontent')

    assert r.content == 'somecontent'


def test_response_failure_create_use_case_error():
    r = res.ResponseFailure.create_use_case_error()

    assert bool(r) is False
    assert r.category == res.USE_CASE_ERROR


def test_response_failure_create_exception_error():
    r = res.ResponseFailure.create_exception_error()

    assert bool(r) is False
    assert r.category == res.EXCEPTION_ERROR


def test_response_failure_create_parameters_error():
    r = res.ResponseFailure.create_parameters_error()

    assert bool(r) is False
    assert r.category == res.PARAMETERS_ERROR
