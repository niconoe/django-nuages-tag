What is it ?
============

A simple Django TemplateTag (named compute\_tag\_cloud) to help in the creation of tag clouds.

Tiny tutorial
=============

Install the app in your Django project
--------------------------------------

This should be as simple as copying the 'django\_nuages\_tag' directory in your project and adding 'django\_nuages\_tag' to your `INSTALLED_APPS` settings.
Pip deployment will follow soon.

Example usage
-------------

Given that we have a my\_favourite\_tools variable defined like this:
    
    my_favourite_tools = [{'name': 'Python', 'interest': 30},
                            {'name': 'Django', 'interest': 70},
                            {'name': 'PHP', 'interest': 6},
                            {'name': 'Ruby', 'interest': 15}]
                            
We can do:                        

    {% compute_tag_cloud my_favourite_tools interest font_size 10 55 lin %}
    
compute\_tag\_cloud will add a `font_size` attribute to each element in `my_favourite_tools` that is contained between 10 and 55 and is representative of the value of `interest`. The last parameter (`lin`) asks to use a linear formula to compute this tag cloud. Another option is to use a logarithmic formula (use the `log` parameter). You should test both options, but `log` will probably give you better results if there is a large variation in the values you want to compute.    

The rendering of the tag cloud can be done very simply with something in the lines of:
    
    {% for tool in my_favourite_tools %}
      <span style="font-size: {{ tool.font_size }}px;> {{ tool.name }} </span>
    {% endfor %}
    
Notes
-----

* The source data (first parameter, `my_favourite_tools` in the example above) can be a Python List or a Django QuerySet.
* `compute_tag_cloud` can be called multiple times in a row to generate multiple values. We can for example compute the font size, but also the margin and the opacity of the text with something like:

        {% compute_tag_cloud my_favourite_tools interest font_size 10 55 lin %}
        {% compute_tag_cloud my_favourite_tools interest margin 5 28 lin %}
        {% compute_tag_cloud my_favourite_tools interest opacity 0.7 1 lin %}
    
        {% for tool in my_favourite_tools %}
          <span style="font-size: {{ tool.font_size }}px; margin: {{ tool.margin }}px; opacity: {{ tool.opacity }}">{{ tool.name }}</span>
        {% endfor %}     
