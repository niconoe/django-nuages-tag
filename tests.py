from django.utils import unittest
from django.template import Template, Context, TemplateSyntaxError

class TemplateTagsTestCase(unittest.TestCase):
    
    # Run before each test
    def setUp(self):
        self.TEST_DATA_DICT = [{'name': 'Python', 'interest': 30},
                          {'name': 'Django', 'interest': 70},
                          {'name': 'PHP', 'interest': 6}]               

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
    
    # TODO: test idem with the log formula
    
    # TODO: test that the bounds (10-100) are taken into account... hmm only for lin ? is it normal ?
                    
            
    # TODO: Test working with a queryset
    # TODO: test working with simple lists/dicts
    # TODO: test result of lin formula
    # TODO: test results of log formula
    # TODO: test multiple run with different variables
    # TODO: test "count" can be an attribute or a function                     
        