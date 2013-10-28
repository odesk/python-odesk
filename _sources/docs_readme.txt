========================
Generating documentation
========================

For documentation we use ``sphinx``, it autogenerates the documentation into html.

To generate new docs do the following:

1) Generate reference documetation for ``odesk`` module::

    sphinx-apidoc --force -o _reference-docs odesk

2) Edit the ``_reference-docs/odesk.rst``:

    * Move ``Module contents`` section to the top
    * Delete ``odesk.tests module`` section

3) Generate documentation in html format::

    sphinx-build -b html . _gh-pages

4) Check the documentation html that everything is okay.

5) Upload contents of ``_gh-pages`` folder to the Github Pages (see ``gh-pages`` branch)
