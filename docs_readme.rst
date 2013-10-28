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

3) Generate documentation in html format::

    sphinx-build -b html . _gh-pages

4) Check the documentation html that everything is okay.

5) Upload contents of ``_gh-pages`` folder to the Github Pages (see ``gh-pages`` branch)::

    cp -r _gh-pages /tmp/.
    mv /tmp/_gh-pages/_static /tmp/_gh-pages/static
    mv /tmp/_gh-pages/_sources /tmp/_gh-pages/sources
    perl -pi -e "s/_static/static/g;" /tmp/_gh-pages/*.html
    perl -pi -e "s/_sources/sources/g;" /tmp/_gh-pages/*.html
    perl -pi -e "s/_static/static/g;" /tmp/_gh-pages/reference-docs/*.html
    perl -pi -e "s/_sources/sources/g;" /tmp/_gh-pages/reference-docs/*.html
    git checkout gh-pages
    cp -rf /tmp/_gh-pages/* .
