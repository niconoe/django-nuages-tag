# -*- coding: utf-8 -*-

from math import log10

from django import template

register = template.Library()

@register.tag
def compute_tag_cloud(parser, token):
    bits = token.split_contents()
    
    if len(bits) != 7:
        raise template.TemplateSyntaxError("%r tag requires 6 arguments:"
        " data, count_property, new_property, min_size, max_size and mode." 
        % token.contents.split()[0])
            
    (tag_name, data, count_property, new_property, min_size, max_size, 
    mode) = bits 
    
    # TODO: Check mode is 'log' or 'lin'
    
    return TagCloudNode(data, count_property, new_property, min_size, max_size, mode)
    
class TagCloudNode(template.Node):
    def __init__(self, data, count_property, new_property, min_size, 
                 max_size, mode):
        self.data = template.Variable(data)
        self.count_property = count_property
        self.new_property = new_property
        self.min_size = float(min_size)
        self.max_size = float(max_size)
        
        if mode == 'log':
            self.calculate = calculate_log
        elif mode == "lin":
            self.calculate = calculate_lin    
    
    def render(self, context):
        data = self.data.resolve(context)
        smallest_count, largest_count = find_min_max(data, self.count_property)
           
        for tag in data:
            current_count = get_attribute_or_method_or_key(tag, self.count_property)
            
            if current_count <= 0:
                size = 0
            else:
                size = self.calculate(current_count, smallest_count, largest_count, 
                                      self.max_size, self.min_size)
            set_attribute_or_key(tag, self.new_property, size)
            
        return '' # Template tags should always returns a string.    
        

# Utility functions
def calculate_lin(current_count, smallest_count, largest_count, max_size, min_size):
    """ Calculate ratio (linear version). """
    
    # Formula details: 
    # http://blog.16codes.com/2007/12/how-to-create-tag-cloud-with-formula.html
    return ( ((current_count-smallest_count) * (max_size-min_size)) / (largest_count
            -smallest_count) ) + min_size

def calculate_log(current_count, smallest_count, largest_count, max_size, min_size):
    """ Calculate ratio (logarithmic version). """
    
    return ((log10(current_count) / log10(largest_count)) * (max_size 
            -min_size) + min_size)

# To allows indifferent access to a Django QuerySet, a method call or to a Python dict
def get_attribute_or_method_or_key(obj, property_name):
    try:
        r = getattr(obj, property_name)
        if callable(r): # the attribute looks like a method
            r = r() 
    except AttributeError as e:
        r = obj[property_name]
    return r
    
def set_attribute_or_key(obj, property_name, property_value):
    try:
        setattr(obj, property_name, property_value)
    except AttributeError:
        obj[property_name] = property_value

def find_min_max(container, count_property):
    """ Returns a tuple containing the min. and max. values of the 'count_property' attribute/key of each element of container. """
    smallest_count = get_attribute_or_method_or_key(container[0], count_property)
    largest_count = get_attribute_or_method_or_key(container[0], count_property)
    
    for tag in container:
        current_count = get_attribute_or_method_or_key(tag, count_property)
        if current_count < smallest_count:
            smallest_count = current_count
        if current_count > largest_count:
            largest_count = current_count
            
    return (smallest_count, largest_count)                       
        
                