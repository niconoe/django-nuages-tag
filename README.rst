What is it ?
============

A simple Django TemplateTag (named compute\_tag\_cloud) to help in the
creation of tag clouds.

Tiny tutorial
=============

Install the app in your Django project
--------------------------------------

This should be as simple as 

::

    pip install django-nuages-tag

and adding ‘django\_nuages\_tag’ to your ``INSTALLED_APPS`` settings.

Example usage
-------------

1. Source data
~~~~~~~~~~~~~~

Given that we have a my\_favourite\_tools context variable defined like
this:

::

    my_favourite_tools = [{'name': 'Python', 'interest': 30},
                          {'name': 'Django', 'interest': 70},
                          {'name': 'Ruby', 'interest': 6}]

Note: example shows a simple list, but **this also works with a Django
QuerySet**.

2. Compute the tag cloud
~~~~~~~~~~~~~~~~~~~~~~~~

We can now do:

::
    {% load django_nuages_tag %}
    
    {% compute_tag_cloud my_favourite_tools interest font_size 10 100 lin %}

compute\_tag\_cloud will add a ``font_size`` attribute to each element
in ``my_favourite_tools`` that is contained between 10 and 100 and is
representative of the value of ``interest``. The last parameter
(``lin``) asks to use a linear formula to compute this tag cloud.
Another option is to use a logarithmic formula (use the ``log``
parameter). You should test both options, but ``log`` will probably give
you better results if there is a large variation in the values you want
to compute. NOTE: 0 and negative values will be computed to 0 (with both formulas).

Our source data now looks like:

::

    my_favourite_tools = [{'name': 'Python', 'interest': 30, 'font_size': 43.75},
                          {'name': 'Django', 'interest': 70, 'font_size': 100},
                          {'name': 'Ruby', 'interest': 6, 'font_size': 10}]

3. Render the tag cloud
~~~~~~~~~~~~~~~~~~~~~~~

This can be done very easily with the ``for`` tag and basic HTML/CSS.
For example:

::

    {% for tool in my_favourite_tools %}
      <span style="font-size: {{ tool.font_size }}px;"> {{ tool.name }} </span>
    {% endfor %}

Notes
-----

-  ``compute_tag_cloud`` can be called multiple times in a row to
   generate multiple values. We can for example compute the font size
   (between 10 and 55), but also the margin (between 5 and 28) and the
   opacity (between 0.7 and 1) of the text with something like:

   ::
       {% load django_nuages_tag %}

       {% compute_tag_cloud my_favourite_tools interest font_size 10 55 lin %}
       {% compute_tag_cloud my_favourite_tools interest margin 5 28 lin %}
       {% compute_tag_cloud my_favourite_tools interest opacity 0.7 1 lin %}

       {% for tool in my_favourite_tools %}
         <span style="font-size: {{ tool.font_size }}px; margin: {{ tool.margin }}px; opacity: {{ tool.opacity }}">{{ tool.name }}</span>
       {% endfor %}
       
- The ``counter`` parameter (``interest`` in our example) can be an attribute, a method to be called or a dictionary key.       
