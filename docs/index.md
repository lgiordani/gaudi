# Gaudi

[![Build Status](https://travis-ci.org/lgiordani/gaudi.svg?branch=master)](https://travis-ci.org/lgiordani/gaudi)
[![Version](https://img.shields.io/pypi/v/gaudi.svg)](https://github.com/lgiordani/gaudi)

A helper library for Clean Architectures in Python

Full documentation available at http://gaudi.readthedocs.io/en/latest/

## About Gaudi

Gaudi (pronounced /ˈɡaʊdi/) is a library that provides some helper structures to build projects based on a clean architecture in Python. The very nature of a clean architecture is the opposite of a framework, so Gaudi provides the minimum amount of classes and methods to avoid boring repetition in your code.

Gaudi is opinionated, as some of the structures provided enforce minimum conventions, like requests being dictionary-like objects and responses having a category and a content. It is also extensible, however, as you are free to change the behaviour of the components at any time.

As you are following the clean architecture model you are free to build the internal protocols and objects like you prefer. Using Gaudi saves you some typing and enforces a minimum of conventions in your project. You are free to use just some of the components of Gaudi without breaking the clean architecture model.

## Origin

In 2016 I wrote [Clean architectures in Python: a step-by-step example](http://blog.thedigitalcatonline.com/blog/2016/11/14/clean-architectures-in-python-a-step-by-step-example/), a detailed analysis of a clean architecture written in Python from scratch following a pure TDD methodology. Since then I created many successful projects following this model, but I quickly realised that there was a core of code that I copied from project to project (the `shared` module in the original article). So I decided to try to clean it up and to publish it as a library.

The name is an homage to [Antoni Gaudí](https://en.wikipedia.org/wiki/Antoni_Gaud%C3%AD) a genius that gave the world some of the most beautiful architectural works ever conceived by men.

## Development

Gaudi is an helper library for clean architectures, so it provides the very minimum amount of code to avoid repetitions among projects. This means that the library shouldn't grow too much in the future. There will be bug fixes and maybe some new helpers if there are good use cases (no pun intended) for them. I'm however ready to be surprised, so it might be that there are many other aspects of the clean architecture that can be automated while keeping the nature of the whole methodology: clean separation between layers.

Feel free to submit issues or pull requests or to get in touch if you have ideas about Gaudi. Maybe you can see what I can't! And thanks for using Gaudi and the Clean Architecture model!

## Installation

Gaudi is available for Python 3 through pip. Just create a virtual environment and run

``` sh
pip install gaudi
```

## Domain models

Gaudi provides the `gaudi.domain_model.DomainModel` abstract base class to register you models.

``` python
from gaudi.domain_model import DomainModel

class Board:
    pass

DomainModel.register(Board)
```

This allows you to categorise your classes as domain models and to check them with `isinstance()`.
For the time being this is not used in the rest of the library.

## Response objects

Gaudi provides a single class that represents a response, `gaudi.response_object.Response`. It provides two factory TODO classes to build success responses (`gaudi.response_object.ResponseSuccess`) and failure responses (`gaudi.response_object.ResponseFailure`).

A `Response` is initialised with a `boolean_value`, a `category`, and a `content` (default `None`)

``` python
class Response:
    def __init__(self, boolean_value, category, content=None):
```

The `boolean_value` is the truth value of the response in boolean comparisons like `response id True` or `response is False`.

The `category` value is used to categorise your responses if you need a complex workflow when receiving them. It accepts any type of value, but I recommend to use a string.

Last, the `content` value is the content of the response. This is up to your implementation, it might be a string, a dictionary, or whatever you need to pass as part of the response.

### Successful responses

To create a successful response you can just run the following code

``` python
r = Response(True, category, content)
```

where `category` and `content` are the values you want to put in the response. You can omit `content` if you don't have anything to return

``` python
r = Response(True, category)
```

Gaudi, however, provides the `ResponseSuccess` class that simplifies the process, while giving a visual hint of what is going on

``` python
r = ResponseSuccess.create(category, content)
```

or, if the response is empty

``` python
r = ResponseSuccess.create(category)
```

As a further simplification, if you are not categorising your responses you might rely on the default category `gaudi.response_object.DEFAULT_SUCCESS` and use the `create_default_success` method

``` python
r = ResponseSuccess.create_default_success(content)
```

or, if the response is empty

``` python
r = ResponseSuccess.create_default_success()
```

### Unsuccessful responses

To create unsuccessful response you can just run the following code

``` python
r = Response(False, category, content)
```

where `category` and `content` are the values you want to put in the response. You can omit `content` if you don't have anything to return

``` python
r = Response(False, category)
```

As happened for successful responses, Gaudi provides the `ResponseFailure` class that simplifies the process

``` python
r = ResponseFailure.create(category, content)
```

or, if the response is empty

``` python
r = ResponseFailure.create(category)
```

When designing a system based on a clean architecture, you can categorise most of the errors as coming from use cases, parameters, or exceptions.

Errors generated by use cases are usually errors that you foresee in your business logic and are explicitly created in the use cases. For these errors you can rely on the `gaudi.response_object.USE_CASE_ERROR` category and use `create_use_case_error`

``` python
r = ResponseFailure.create_use_case_error(content)
```

or, if the response is empty

``` python
r = ResponseFailure.create_use_case_error()
```

Another type of error is the one that originates from wrong parameters (either missing ones or parameters with wrong values or types). For these errors you can use the `gaudi.response_object.PARAMETERS_ERROR` category given by `create_parameters_error`

``` python
r = ResponseFailure.create_parameters_error(content)
```

or, if the response is empty

``` python
r = ResponseFailure.create_parameters_error()
```

The last type of error is used for exceptions, or errors that cannot be foreseen when designing the clean architecture. This definition may encompass both system errors that cannot be considered when writing an algorithm (the disk is full) and errors that you simply forgot to consider in the algorithm, that are thus not properly handled. These errors can have the standard `gaudi.response_object.EXCEPTION_ERROR` category used by `create_exception_error`

``` python
r = ResponseFailure.create_exception_error(content)
```

or, if the response is empty

``` python
r = ResponseFailure.create_exception_error()
```

## Use cases

Use cases are represented by the `gaudi.use_case.UseCase` class. To define a use case you can inherit from this class in the traditional way

``` python
from gaudi import use_case as uc

class InitialiseSystemUseCase(uc.UseCase):
```

The `__init__` method of `UseCase` accepts two parameters, `exception_on_failure` and `no_traceback`.

When the use case returns an unsuccessful response you might choose to raise a specific Python exception instead of returning the original error. The `exception_on_failure` argument is the exception class that will be returned, initialised with the unsuccessful response category and content. Pay attention that this is not a properly formatted unsuccessful response but a real Python exception.

By default, if the use case raises an exception (for example if you try to access an element of an empty list) the returned response contains the exception traceback. If you pass the `no_traceback` argument as `True` the returned response will contain only the exception name and content.

## Process the request

You have to put the use case logic in the `process_request` method, that receives the incoming request as the only parameter. The request is supposed to be an object with a dictionary-like interface.

``` python
class InitialiseSystemUseCase(uc.UseCase):
    def process_request(self, request):
```

Inside this function you can process the incoming data contained in the request and eventually return a `Response` (see the previous section).

``` python
from gaudi import use_case as uc
from gaudi import response_object as res
from mysystem import System


class InitialiseSystemUseCase(uc.UseCase):

    def process_request(self, request):
        c = request['cpus']

        s = System(cpus_number=c)

        return res.ResponseSuccess.create_default_success({
            'system': s,
        })
```

As already explained, any Python exception occurring inside the `process_request` function will result in an unsuccessful `Response` with category `EXCEPTION_ERROR`.

## Processing the request parameters

When you create the use case you can define a class attribute called `_parameters`, which is a list of mandatory parameters. The presence of these parameters is checked inside the incoming request, and if a parameter is missing an unsuccessful `Response` is returned by the use case, with the `PARAMETERS_ERROR` category and an apt content that signals the error.

Parameters can be specified as simple strings or as dictionaries. As strings you are supposed to pass the parameter name, and the only check that Gaudi does is to verify that the parameter is present in the request. These are pure mandatory parameters.

``` python
class InitialiseSystemUseCase(uc.UseCase):
    _parameters = ['cpus']

    def process_request(self, request):
```

If you specify a parameter as a dictionary you have to include the `name` key, which value is the name of the parameter as it is supposed to be contained in the request. You can also include a `default` key, which value is the default value of the parameter.

``` python
class InitialiseSystemUseCase(uc.UseCase):
    _parameters = [
        {
            'name': 'cpus',
            'default': 4
        }
    ]

    def process_request(self, request):
```

## Use case execution

The `UseCase` class provides an `execute` method that actually runs the use case. This method performs the following actions:

* It initialises an empty request
* It runs through all the parameters and sets the default value of the ones that provide it
* It updates the request with the one provided as an argument
* It checks if all the parameters mentioned in the `_parameters` class attribute are contained in the request.
* If something goes wrong here it returns a `PARAMETERS_ERROR` unsuccessful response
* It runs the `process_request` method that you provided
* If a Python exception is raised during this step it returns an `EXCEPTION_ERROR` unsuccessful response
* If the response is unsuccessful and `exception_on_failure` is set it raises the given exception
* In all the other cases it returns the response (successful or unsuccessful)

An example of code that runs a use case is the following

``` python
use_case = InitialiseSystemUseCase()

res = use_case.execute({
    'cpus': 5
})
```

According to the previous definition of `InitialiseSystemUseCase` this will run the code `s = System(cpus_number=5)` and return a successful `Response` with content `{'system': s}`.

Instead the following code

``` python
use_case = InitialiseSystemUseCase()

res = use_case.execute()
```

will return an unsuccessful `Response` categorised as `PARAMETERS_ERROR`, as `cpus` is listed among the mandatory parameters of the `InitialiseSystemUseCase` use case.

## Helper classes

Initialising a use case and executing it will be a pretty common pattern in your code. To provide shortcuts for this pattern all the classes that inherit from `UseCase` are registered into the `UseCaseMeta` metaclass and accessible through the `UseCaseRegister` class.

``` python
ucr = UseCaseRegister()
use_case = ucr.InitialiseSystem
```

this code puts in the `use_case` variable the class `InitialiseSystemUseCase`. Pay attention that use cases are registered without the suffix `UseCase`. Note also that the returned value is the class and not an instance of it.

The `UseCaseCreator` class retrieves the use case and initialises it

``` python
ucc = UseCaseCreator()
use_case = ucc.InitialiseSystem
```

Here, `use_case` is an instance of `InitialiseSystemUseCase`. `UseCaseCreator` can be initialised with some parameters that are used then to initialise all the use cases

``` python
ucc = UseCaseCreator(exception_on_failure=ValueError)
use_case = ucc.InitialiseSystem
```

Now `use_case` is an instance of `InitialiseSystemUseCase` that has been created with `exception_on_failure=ValueError`.

The last helper class is `UseCaseExecutor` that behaves exactly like `UseCaseCreator` but returns the `execute` method of the use case. Thus, it can be used to run the use case in one single line of code

``` python
uce = UseCaseExecutor()

res = uce.InitialiseSystem({
    'cpus': 5
})
```

**ATTENTION** The registration and the helper classes work if you imported the modules containing your use cases. So you have either to import them at the beginning of each file or to import them once and for all in the `__init__.py` file of your module.

