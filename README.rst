Gaudi
=====

`Build Status <https://travis-ci.org/lgiordani/gaudi>`__
`Version <https://github.com/lgiordani/gaudi>`__

A helper library for Clean Architectures in Python

Full documentation available at
http://gaudilib.readthedocs.io/en/latest/

About Gaudi
-----------

Gaudi (pronounced /ˈɡaʊdi/) is a library that provides some helper
structures to build projects based on a clean architecture in Python.
The very nature of a clean architecture is the opposite of a framework,
so Gaudi provides the minimum amount of classes and methods to avoid
boring repetition in your code.

Gaudi is opinionated, as some of the structures provided enforce minimum
conventions, like requests being dictionary-like objects and responses
having a category and a content. It is also extensible, however, as you
are free to change the behaviour of the components at any time.

As you are following the clean architecture model you are free to build
the internal protocols and objects like you prefer. Using Gaudi saves
you some typing and enforces a minimum of conventions in your project.
You are free to use just some of the components of Gaudi without
breaking the clean architecture model.

Origin
------

In 2016 I wrote `Clean architectures in Python: a step-by-step
example <http://blog.thedigitalcatonline.com/blog/2016/11/14/clean-architectures-in-python-a-step-by-step-example/>`__,
a detailed analysis of a clean architecture written in Python from
scratch following a pure TDD methodology. Since then I created many
successful projects following this model, but I quickly realised that
there was a core of code that I copied from project to project (the
``shared`` module in the original article). So I decided to try to clean
it up and to publish it as a library.

The name is an homage to `Antoni
Gaudí <https://en.wikipedia.org/wiki/Antoni_Gaud%C3%AD>`__ a genius that
gave the world some of the most beautiful architectural works ever
conceived by men.

Development
-----------

Gaudi is an helper library for clean architectures, so it provides the
very minimum amount of code to avoid repetitions among projects. This
means that the library shouldn’t grow too much in the future. There will
be bug fixes and maybe some new helpers if there are good use cases (no
pun intended) for them. I’m however ready to be surprised, so it might
be that there are many other aspects of the clean architecture that can
be automated while keeping the nature of the whole methodology: clean
separation between layers.

Feel free to submit issues or pull requests or to get in touch if you
have ideas about Gaudi. Maybe you can see what I can’t! And thanks for
using Gaudi and the Clean Architecture model!

Installation
------------

Gaudi is available for Python 3 through pip. Just create a virtual
environment and run

.. code:: sh

   pip install gaudi

Contributing
------------

See the CONTRIBUTING file for detailed information. Please remember that
this project is actively developed in the ``develop`` branch, so be sure
to work there if you try to implement new feature of fix bugs.
