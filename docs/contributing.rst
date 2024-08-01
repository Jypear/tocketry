
Contributing
============

All help is welcome. There are several ways to contribute:

- `Report an issue (bug, feature request etc.) <https://github.com/Jypear/tocketry/issues>`_
- `Do code a change <https://github.com/Jypear/tocketry/pulls>`_
- `Join the discussion <https://github.com/Jypear/tocketry/discussions>`_


Have an Idea?
-------------

If you have a concrete idea of a feature you wish Tocketry had, 
feel free to open `a feature request <https://github.com/Jypear/tocketry/issues/new?assignees=&labels=enhancement&template=feature_request.md&title=ENH>`_.

If you have ideas about broader or more abstract features or would like to discuss about the future directions of the framework, 
feel free to open a discussion about it to `Tocketry's discussion board <https://github.com/Jypear/tocketry/discussions>`_.

Found a bug?
------------

If you found a bug,
`please report it as a bug <https://github.com/Jypear/Tocketry/issues/new?assignees=&labels=bug&template=bug_report.md&title=BUG>`_.

Unclear documentation?
----------------------

If you found an issue with the documentation,
`please report it <https://github.com/Jypear/tocketry/issues/new?assignees=&labels=documentation&template=documentation_improvement.md&title=DOCS>`_.

Want to do a code contribution?
------------------------------- 

Good place to start is to look for open issues 
`from issue tracker <https://github.com/Jypear/tocketry/issues>`_. 

If you found a problem and the fix is simple, you don't have to create an issue 
for it. Complex changes require an issue.

Development Guidelines
^^^^^^^^^^^^^^^^^^^^^^

How to do code contribution:

1. Create an issue (you don't need an issue if it's simple)
2. Fork and clone the project
3. Do your changes
4. Run the tests locally or check the documentation
5. Create a pull request

There are some criteria that new code must pass:

- Well tested (with unit tests)
- Well documented
- No breaking changes (unless strictly necessary)
- Follows best practices and standard naming conventions

Improving documentation
^^^^^^^^^^^^^^^^^^^^^^^

If you made a change to documentation, please build them by:
```
pip install tox
tox -e docs
```
Then go to the ``/docs/_build/html/index.html`` and check the 
change looks visually good.

Improving code
^^^^^^^^^^^^^^

To do code changes:

1. Open an issue (unless trivial)
2. Fork and clone the repository
3. Do the changes
4. Run the tests (see below)
5. Do a pull request

To run the tests, you can use tox:

```
pip install tox
tox
```

To ensure your pull request gets approved:

- Create unit tests that demonstrates the bug it fixed or the feature implemented
- Write documentation (unless it's a bug fix)
- Ensure standard behaviour raises no warnings
- Ensure the code follows best practices and fits to the project

Don't feel overwhelmed with these, there are automatic pipelines to ensure code quality
and your code can be updated after the pull request. Tocketry's maintainers understand 
that you are using your free time to contribute on free open-source software.
