========================
Generating documentation
========================

For documentation we use ``sphinx``, it autogenerates the documentation into html.

To generate new docs do the following:

1) Generate reference documetation for ``odesk`` module::

    sphinx-apidoc --force -o reference-docs odesk

2) Edit the ``reference-docs/odesk.rst``:

    * Move ``Module contents`` section to the top
    * Delete ``odesk.tests module`` section

3) Edit the ``reference-docs/odesk.routers.rst``:

   * Move ``Module contents`` section to the top

4) Generate documentation in html format::

    sphinx-build -b html . _gh-pages

5) Check the documentation html that everything is okay.

6) Upload contents of ``_gh-pages`` folder to the Github Pages (see ``gh-pages`` branch)::

     sh update_docs.sh
