from django.db import models
from django.utils import unittest
from django.template import Template, Context, TemplateSyntaxError

# This model is usedul only for testing
class Article(models.Model):
    title = models.CharField(max_length=128)
    count_attribute = models.IntegerField()
    
    # This will be used to test that the 'count' parameter can be either an attribute or a method to call
    def count_method(self):
        return self.count_attribute * 1

class TemplateTagsTestCase(unittest.TestCase):
    
    # Run before each test
    def setUp(self):
        # Create a dict (will be used as a datasource)
        self.TEST_DATA_DICT = [{'name': 'Python', 'interest': 30},
                               {'name': 'Django', 'interest': 70},
                               {'name': 'PHP', 'interest': 6}]
        
        # Idem, but one of the tag has the '0' value                       
        self.TEST_DATA_DICT_ZERO = [{'name': 'Python', 'interest': 30},
                                    {'name': 'Django', 'interest': 70},
                                    {'name': 'PHP', 'interest': 0}]
        
        self.TEST_DATA_DICT_NEG = [{'name': 'Python', 'interest': 30},
                                    {'name': 'Django', 'interest': 70},
                                    {'name': 'PHP', 'interest': -1.5}]                                              
        
        # Create a few Articles (another datasource)
        Article.objects.all().delete()
        Article.objects.create(title="Anthribidae", count_attribute=3)
        Article.objects.create(title="Brentidae", count_attribute=3)
        Article.objects.create(title="Buprestidae", count_attribute=290)
        Article.objects.create(title="Carabidae", count_attribute=151)
        Article.objects.create(title="Cerambycidae", count_attribute=967)                                

    # This test is the only one testing that the count argument can be a method
    # All other tests assume it's an attribute or a key (of dict)
    def test_with_count_method(self):
        all_articles = Article.objects.order_by('title')
        
        t = Template('{% load django_nuages_tag %}'
                     '{% compute_tag_cloud articles count_method font_size 10 55 log %}')             
                     
        c = Context({'articles': all_articles})
        t.render(c)
        
        # We check an attribute has been added (and its value!)
        self.assertAlmostEqual(c['articles'][0].font_size, 17.1917552312)
        self.assertAlmostEqual(c['articles'][1].font_size, 17.1917552312)
        self.assertAlmostEqual(c['articles'][2].font_size, 47.1162749669)
        self.assertAlmostEqual(c['articles'][3].font_size, 42.8442061727)
        self.assertAlmostEqual(c['articles'][4].font_size, 55)

    # We use a QuerySet as a datasource (instead of simple List)
    def test_with_queryset(self):
        all_articles = Article.objects.order_by('title')
        
        t = Template('{% load django_nuages_tag %}'
                     '{% compute_tag_cloud articles count_attribute font_size 10 55 log %}')             
                     
        c = Context({'articles': all_articles})
        t.render(c)
        
        # We check an attribute has been added (and its value!)
        self.assertAlmostEqual(c['articles'][0].font_size, 17.1917552312)
        self.assertAlmostEqual(c['articles'][1].font_size, 17.1917552312)
        self.assertAlmostEqual(c['articles'][2].font_size, 47.1162749669)
        self.assertAlmostEqual(c['articles'][3].font_size, 42.8442061727)
        self.assertAlmostEqual(c['articles'][4].font_size, 55)
        

    # Test the tag complains if we don't provide the mandatory arguments.
    def test_compute_tag_cloud_requires_arguments(self):
        with self.assertRaises(TemplateSyntaxError):
            t = Template('{% load django_nuages_tag %}'
                         '{% compute_tag_cloud %}')
            c = Context({})
            t.render(c)
            
    # Test the tag does not raise a TemplateSyntaxError if we provide it the correct arguments        
    def test_correct_arguments(self):        
        try:
            t = Template('{% load django_nuages_tag %}'
                         '{% compute_tag_cloud my_test_data interest font-size 10 100 lin %}')             
                         
            c = Context({'my_test_data': self.TEST_DATA_DICT})
            t.render(c)
        except TemplateSyntaxError:
            self.fail("compute_tag_cloud raised TemplateSyntaxError while it received valid arguments.")
    
    # Global test that chek the template tag is working fine with a dict as a data source        
    def test_results_lin_from_dict(self):
        t = Template('{% load django_nuages_tag %}'
                     '{% compute_tag_cloud my_test_data interest font-size 10 100 lin %}')             
                     
        c = Context({'my_test_data': self.TEST_DATA_DICT})
        t.render(c)
        
        # Values checked manually
        self.assertAlmostEqual(self.TEST_DATA_DICT[0]['font-size'], 43.75) # Python
        self.assertAlmostEqual(self.TEST_DATA_DICT[1]['font-size'], 100) # Django
        self.assertAlmostEqual(self.TEST_DATA_DICT[2]['font-size'], 10) # PHP
            
    def test_results_log_from_dict(self):
        t = Template('{% load django_nuages_tag %}'
                     '{% compute_tag_cloud my_test_data interest font-size 10 100 log %}')             

        c = Context({'my_test_data': self.TEST_DATA_DICT})
        t.render(c)

        # Values checked manually
        self.assertAlmostEqual(self.TEST_DATA_DICT[0]['font-size'], 82.0508666974) # Python
        self.assertAlmostEqual(self.TEST_DATA_DICT[1]['font-size'], 100) # Django
        self.assertAlmostEqual(self.TEST_DATA_DICT[2]['font-size'], 47.9565806346) # PHP    
    
    # Next 4 tests: 0 (or less) should have size 0
    def test_with_zero_log(self):
        t = Template('{% load django_nuages_tag %}'
                     '{% compute_tag_cloud my_test_data interest font-size 10 100 log %}')             

        c = Context({'my_test_data': self.TEST_DATA_DICT_ZERO})
        t.render(c)
        
        self.assertAlmostEqual(self.TEST_DATA_DICT_ZERO[2]['font-size'], 0) # PHP
    
    def test_with_zero_lin(self):
        t = Template('{% load django_nuages_tag %}'
                     '{% compute_tag_cloud my_test_data interest font-size 10 100 lin %}')             

        c = Context({'my_test_data': self.TEST_DATA_DICT_ZERO})
        t.render(c)

        self.assertAlmostEqual(self.TEST_DATA_DICT_ZERO[2]['font-size'], 0) # PHP     
    
    def test_with_neg_log(self):
        t = Template('{% load django_nuages_tag %}'
                     '{% compute_tag_cloud my_test_data interest font-size 10 100 log %}')             

        c = Context({'my_test_data': self.TEST_DATA_DICT_NEG})
        t.render(c)

        self.assertAlmostEqual(self.TEST_DATA_DICT_NEG[2]['font-size'], 0) # PHP

    def test_with_neg_lin(self):
        t = Template('{% load django_nuages_tag %}'
                         '{% compute_tag_cloud my_test_data interest font-size 10 100 lin %}')             

        c = Context({'my_test_data': self.TEST_DATA_DICT_NEG})
        t.render(c)

        self.assertAlmostEqual(self.TEST_DATA_DICT_NEG[2]['font-size'], 0) # PHP
        
    
    # TODO: test that the bounds (10-100) are taken into account... hmm only for lin ? is it normal ?
                    
            
    # TODO: Test working with a queryset

    # TODO: test multiple run with different variables
    # TODO: test "count" can be an attribute or a function                     
        