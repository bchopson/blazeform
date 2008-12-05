import unittest
import datetime
import warnings
from formencode.validators import Int

from pysform import Form
from pysform.element import TextElement
from pysform.util import NotGiven

class CommonTest(unittest.TestCase):

    def test_render(self):
        html = '<input class="text" id="f-username" name="username" type="text" />'
        form = Form('f')
        form.add_element('text', 'username', 'User Name')
        self.assertEqual(html, str(form.username.render()))
        
    def test_implicit_render(self):
        html = '<input class="text" id="f-username" name="username" type="text" />'
        form = Form('f')
        form.add_element('text', 'username', 'User Name')
        self.assertEqual(html, str(form.username()))
        
    def test_attr_render(self):
        html = '<input baz="bar" class="text foo bar" id="f-username" name="username" type="text" />'
        form = Form('f')
        form.add_element('text', 'username', 'User Name')
        self.assertEqual(html, str(form.username(class_='text foo bar', baz='bar')))

    def test_text_with_default(self):
        html = '<input class="text" id="f-username" name="username" type="text" value="bar" />'
        form = Form('f')
        form.add_element('text', 'username', 'User Name', defaultval='bar')
        self.assertEqual(html, str(form.username.render()))
    
    def test_text_with_default2(self):
        html = '<input class="text" id="f-username" name="username" type="text" value="bar" />'
        form = Form('f')
        form.add_element('text', 'username', 'User Name')
        form.set_defaults({'username':'bar'})
        self.assertEqual(html, str(form.username.render()))
    
    def test_text_submit(self):
        # make sure the submit value shows up in the form
        html = '<input class="text" id="f-username" name="username" type="text" value="bar" />'
        form = Form('f')
        form.add_element('text', 'username', 'User Name')
        form.set_submitted({'username':'bar'})
        self.assertEqual(html, str(form.username.render()))
    
    def test_submit_default(self):
        # submitted should take precidence over default
        html = '<input class="text" id="f-username" name="username" type="text" value="bar" />'
        form = Form('f')
        form.add_element('text', 'username', 'User Name')
        form.set_defaults({'username':'foo'})
        form.set_submitted({'username':'bar'})
        self.assertEqual(html, str(form.username.render()))
    
    def test_default_value(self):
        # default values do not show up in .value, they only show up when
        # rendering
        form = Form('f')
        form.add_element('text', 'username', 'User Name')
        form.set_defaults({'username':'foo'})
        self.assertEqual(None, form.username.value)
    
    def test_submitted_value(self):
        form = Form('f')
        form.add_element('text', 'username', 'User Name')
        form.set_defaults({'username':'foo'})
        form.set_submitted({'username':'bar'})
        self.assertEqual('bar', form.username.value)
        
    def test_notgiven(self):
        # test that NotGiven == None and is what we get when nothing
        # submitted
        form = Form('f')
        form.add_element('text', 'username', 'User Name')
        self.assertEqual(None, form.username.value)
        
        # make sure the value we get really is NotGiven
        f = Form('f')
        el = f.add_text('f', 'f')
        assert el.value is NotGiven
        
        # default shouldn't affect this
        f = Form('f')
        el = f.add_text('f', 'f', defaultval='test')
        assert el.value is NotGiven
    
    def test_if_missing(self):        
        f = Form('f')
        el = f.add_text('f', 'f', if_missing='foo')
        assert el.value is 'foo'
        
        # doesn't affect anything if the field is submitted
        f = Form('f')
        el = f.add_text('f', 'f', if_missing='foo')
        el.submittedval = None
        assert el.value is None
    
    def test_if_empty(self):
        # if empty works like if_missing when the field isn't submitted
        f = Form('f')
        el = f.add_text('f', 'f', if_empty='foo')
        assert el.value is 'foo'
        
        # if_empty also covers empty submit values
        f = Form('f')
        el = f.add_text('f', 'f', if_empty='foo')
        el.submittedval = None
        assert el.value == 'foo'
        
        # an "empty" if_empty should not get converted to None
        f = Form('f')
        el = f.add_text('f', 'f', if_empty='')
        assert el.value == ''
        
        # same as previous, but making sure a submitted empty value doesn't
        #change it
        f = Form('f')
        el = f.add_text('f', 'f', if_empty='')
        el.submittedval = None
        assert el.value == ''        
    
    def test_strip(self):
        # strip is on by default
        el = Form('f').add_text('f', 'f')
        el.submittedval = '   '
        assert el.value == None
        
        # turn strip off
        el = Form('f').add_text('f', 'f', strip=False)
        el.submittedval = '   '
        assert el.value == '   '
        
        # strip happens before if_empty
        el = Form('f').add_text('f', 'f', if_empty='test')
        el.submittedval = '   '
        assert el.value == 'test'

    def test_invalid(self):
        el = Form('f').add_text('f', 'f', required=True)
        el.submittedval = None
        assert el.is_valid() == False
        
        el = Form('f').add_text('f', 'f', required=True, if_invalid='foo')
        el.submittedval = None
        self.assertEqual(el.value, 'foo')
        
    def test_blank_submit_value(self):
        form = Form('f')
        form.add_element('text', 'username', 'User Name')
        form.set_submitted({'username':''})
        self.assertEqual(None, form.username.value)
        
        form = Form('f')
        form.add_element('text', 'username', 'User Name', if_empty='')
        form.set_submitted({'username':''})
        self.assertEqual('', form.username.value)
    
    def test_is_submitted(self):
        form = Form('f')
        form.add_element('text', 'username', 'User Name')
        form.set_defaults({'username':'foo'})
        self.assertEqual(False, form.username.is_submitted())
        
        form.set_submitted({'username':''})
        self.assertEqual(True, form.username.is_submitted())
    
    def test_required(self):
        form = Form('f')
        el = form.add_element('text', 'username', 'User Name', required=True)
        self.assertEqual(True, el.required)
        self.assertEqual(False, form.username.is_valid())
        
        # setting submitted should reset _valid to None, which causes the
        # processing to happen again
        self.assertEqual(False, form.username._valid)
        el.submittedval = ''
        self.assertEqual(None, form.username._valid)
        
        el.submittedval = 'foo'
        self.assertEqual(True, form.username.is_valid())
    
    def test_invalid_value(self):
        form = Form('f')
        el = form.add_element('text', 'username', 'User Name', required=True)
        try:
            v = el.value
            self.fail('expected exception when trying to use .value when element is invalid')
        except Exception, e:
            if str(e) != 'element value is not valid':
                raise
        
        el.submittedval = ''
        try:
            v = el.value
            self.fail('expected exception when trying to use .value when element is invalid')
        except Exception, e:
            if str(e) != 'element value is not valid':
                raise
        
        el.submittedval = None
        try:
            v = el.value
            self.fail('expected exception when trying to use .value when element is invalid')
        except Exception, e:
            if str(e) != 'element value is not valid':
                raise
        
        el.submittedval = '0'
        self.assertEqual('0', el.value)
        
        el.submittedval = 0
        self.assertEqual(0, el.value)
        
        el.submittedval = False
        self.assertEqual(False, el.value)
    
    def test_double_processing(self):
        class validator(object):
            vcalled = 0
            
            def __call__(self, value):
                self.vcalled += 1
                return value
        
        v = validator()
        form = Form('f')
        el = form.add_element('text', 'username', 'User Name', if_empty='bar')
        el.add_processor(v)
        self.assertEqual(True, form.username.is_valid())
        self.assertEqual(1, v.vcalled)
        self.assertEqual(True, form.username.is_valid())
        self.assertEqual(1, v.vcalled)
        self.assertEqual('bar', form.username.value)
        self.assertEqual(1, v.vcalled)
        self.assertEqual('bar', form.username.value)
        self.assertEqual(1, v.vcalled)
        
        # setting submitted should reset _valid to None, which causes the
        # processing to happen again.  Make sure we don't use an empty value
        # b/c formencode seems to cache the results and our validator's method
        # won't be called again
        el.submittedval = 'foo'
        self.assertEqual('foo', form.username.value)
        self.assertEqual(2, v.vcalled)

    def test_error_messages(self):
        form = Form('f')
        el = form.add_element('text', 'username', 'User Name', required=True)
        self.assertEqual(False, form.username.is_valid())
        self.assertEqual(len(el.errors), 1)
        self.assertEqual('"User Name" is required', el.errors[0])
        
        # formencode message
        form = Form('f')
        el = form.add_element('text', 'field', 'Field', if_empty='test')
        el.add_processor(Int)
        self.assertEqual(False, el.is_valid())
        self.assertEqual(len(el.errors), 1)
        self.assertEqual('Please enter an integer value', el.errors[0])
        
        # custom message
        form = Form('f')
        el = form.add_element('text', 'field', 'Field', if_empty='test')
        el.add_processor(Int, 'int required')
        self.assertEqual(False, el.is_valid())
        self.assertEqual(len(el.errors), 1)
        self.assertEqual('int required', el.errors[0])
        
        # errors should be reset on submission
        el.submittedval = 'five'
        self.assertEqual(False, el.is_valid())
        self.assertEqual(len(el.errors), 1)
        
        el.submittedval = 5
        self.assertEqual(True, el.is_valid())
        self.assertEqual(len(el.errors), 0)
        
    def test_notes(self):
        form = Form('f')
        el = form.add_element('text', 'field', 'Field')
        el.add_note('test note')
        self.assertEqual(el.notes[0], 'test note')
    
    def test_handlers(self):
        form = Form('f')
        el = form.add_element('text', 'field', 'Field')
        el.add_handler('text exception', 'test error msg')
        assert el.handle_exception(Exception('text exception'))
        self.assertEqual(el.errors[0], 'test error msg')
        
        # make sure second exception works too
        form = Form('f')
        el = form.add_element('text', 'field', 'Field')
        el.add_handler('not it', '')
        el.add_handler('text exception', 'test error msg')
        assert el.handle_exception(Exception('text exception'))
        self.assertEqual(el.errors[0], 'test error msg')
        
        # specifying exception type
        form = Form('f')
        el = form.add_element('text', 'field', 'Field')
        el.add_handler('text exception', 'test error msg', Exception)
        assert el.handle_exception(Exception('text exception'))
        self.assertEqual(el.errors[0], 'test error msg')
        
        # right message, wrong type
        form = Form('f')
        el = form.add_element('text', 'field', 'Field')
        el.add_handler('text exception', 'test error msg', ValueError)
        assert not el.handle_exception(Exception('text exception'))
        self.assertEqual(len(el.errors), 0)
        
        # wrong message
        form = Form('f')
        el = form.add_element('text', 'field', 'Field')
        el.add_handler('text exception', 'test error msg', Exception)
        assert not el.handle_exception(Exception('text'))
        self.assertEqual(len(el.errors), 0)
        
    def test_conversion(self):
        # without form submission, we get empty value
        form = Form('f')
        el = form.add_element('text', 'field', 'Field', 'bool')
        self.assertEqual( el.value, None)
        
        # default values do not get processed, they are for display only
        form = Form('f')
        el = form.add_element('text', 'field', 'Field', 'bool', '1')
        self.assertEqual( el.value, None)
        
        # submission gets converted
        form = Form('f')
        el = form.add_element('text', 'field', 'Field', 'bool')
        el.submittedval = '1'
        self.assertEqual( el.value, True)
        
        # conversion turned off
        form = Form('f')
        el = form.add_element('text', 'field', 'Field')
        el.submittedval = '1'
        self.assertEqual( el.value, '1')
        
        # conversion with if_empty
        form = Form('f')
        el = form.add_element('text', 'field', 'Field', 'bool', if_empty=False)
        el.submittedval = '1'
        self.assertEqual( el.value, True)
        
        # conversion with if_empty
        form = Form('f')
        el = form.add_element('text', 'field', 'Field', 'bool', if_empty=False)
        el.submittedval = None
        self.assertEqual( el.value, False)
        
        # conversion with if_empty
        form = Form('f')
        el = form.add_element('text', 'field', 'Field', 'bool', if_empty=True)
        el.submittedval = False
        self.assertEqual( el.value, False)
        
        # conversion with if_empty
        form = Form('f')
        el = form.add_element('text', 'field', 'Field', 'bool', if_empty='1')
        self.assertEqual( el.value, True)
        
    def test_type_strings(self):

        form = Form('f')
        form.add_element('text', 'f1', 'Field', 'bool', if_empty='1.25')
        self.assertEqual(form.f1.value, True)
        form.add_element('text', 'f2', 'Field', 'boolean', if_empty='1.25')
        self.assertEqual(form.f2.value, True)
        form.add_element('text', 'f3', 'Field', 'int', if_empty='1')
        self.assertEqual(form.f3.value, 1)
        form.add_element('text', 'f4', 'Field', 'integer', if_empty='1')
        self.assertEqual(form.f4.value, 1)
        form.add_element('text', 'f5', 'Field', 'num', if_empty='1.25')
        self.assertEqual(form.f5.value, 1.25)
        form.add_element('text', 'f6', 'Field', 'number', if_empty='1.25')
        self.assertEqual(form.f6.value, 1.25)
        form.add_element('text', 'f7', 'Field', 'float', if_empty='1.25')
        self.assertEqual(form.f7.value, 1.25)
        form.add_element('text', 'f8', 'Field', 'str', if_empty='1.25')
        self.assertEqual(form.f8.value, '1.25')
        form.add_element('text', 'f9', 'Field', 'string', if_empty='1.25')
        self.assertEqual(form.f9.value, '1.25')
        form.add_element('text', 'f10', 'Field', 'uni', if_empty='1.25')
        self.assertEqual(form.f10.value, u'1.25')
        form.add_element('text', 'f11', 'Field', 'unicode', if_empty='1.25')
        self.assertEqual(form.f11.value, u'1.25')
        form.add_element('text', 'f12', 'Field', 'bool', if_empty='false')
        self.assertEqual(form.f12.value, False)
        
        # test invalid vtype
        form = Form('f')
        try:
            form.add_text('f1', 'Field', 'badvtype')
        except ValueError, e:
            self.assertEqual('invalid vtype "badvtype"', str(e))
            
        # test wrong type of vtype
        try:
            form.add_text('f2', 'Field', ())
        except TypeError, e:
            self.assertEqual('vtype should have been a string, got <type \'tuple\'> instead', str(e))

    
class InputElementsTest(unittest.TestCase):
    
    def test_el_button(self):
        html = '<input class="button" id="f-field" name="field" type="button" />'
        el = Form('f').add_button('field', 'Field')
        assert el() == html
        
    def test_el_checkbox(self):
        not_checked = '<input class="checkbox" id="f-f" name="f" type="checkbox" />'
        checked = '<input checked="checked" class="checkbox" id="f-f" name="f" type="checkbox" />'
        
        # no default
        f = Form('f')
        el = f.add_checkbox('f', 'f')
        self.assertEqual(str(el()), not_checked)
        
        # default from defaultval (True)
        el = Form('f').add_checkbox('f', 'f', defaultval=True)
        self.assertEqual(str(el()), checked)
        el = Form('f').add_checkbox('f', 'f', defaultval='checked')
        self.assertEqual(str(el()), checked)
        el = Form('f').add_checkbox('f', 'f', defaultval=1)
        self.assertEqual(str(el()), checked)
        
        # default from defaultval (False)
        el = Form('f').add_checkbox('f', 'f', defaultval=False)
        self.assertEqual(str(el()), not_checked)
        el = Form('f').add_checkbox('f', 'f', defaultval=None)
        self.assertEqual(str(el()), not_checked)
        el = Form('f').add_checkbox('f', 'f', defaultval=0)
        self.assertEqual(str(el()), not_checked)
        
        # default from checked (True)
        el = Form('f').add_checkbox('f', 'f', checked=True)
        self.assertEqual(str(el()), checked)
        el = Form('f').add_checkbox('f', 'f', checked='checked')
        self.assertEqual(str(el()), checked)
        el = Form('f').add_checkbox('f', 'f', checked=1)
        self.assertEqual(str(el()), checked)
        
        # default from checked (False)
        el = Form('f').add_checkbox('f', 'f', checked=False)
        self.assertEqual(str(el()), not_checked)
        el = Form('f').add_checkbox('f', 'f', checked=None)
        self.assertEqual(str(el()), not_checked)
        el = Form('f').add_checkbox('f', 'f', checked=0)
        self.assertEqual(str(el()), not_checked)
        
        # default takes precidence over checked
        el = Form('f').add_checkbox('f', 'f', defaultval=True, checked=False)
        self.assertEqual(str(el()), checked)
        el = Form('f').add_checkbox('f', 'f', defaultval=False, checked=True)
        self.assertEqual(str(el()), not_checked)
        
        # default should not affect value
        el = Form('f').add_checkbox('f', 'f', defaultval=True)
        self.assertEqual(el.value, False)
        
        # true submit values
        el = Form('f').add_checkbox('f', 'f')
        el.submittedval = True
        self.assertEqual(el.value, True)
        el = Form('f').add_checkbox('f', 'f')
        el.submittedval = 1
        self.assertEqual(el.value, True)
        el = Form('f').add_checkbox('f', 'f')
        el.submittedval = 'checked'
        self.assertEqual(el.value, True)
        
        # false submit values
        el = Form('f').add_checkbox('f', 'f')
        el.submittedval = False
        self.assertEqual(el.value, False)
        el = Form('f').add_checkbox('f', 'f')
        el.submittedval = 0
        self.assertEqual(el.value, False)
        el = Form('f').add_checkbox('f', 'f')
        self.assertEqual(el.value, False)
        
        # converted values int (true)
        el = Form('f').add_checkbox('f', 'f', 'int')
        el.submittedval = True
        self.assertEqual(el.value, 1)
        el = Form('f').add_checkbox('f', 'f', 'int')
        el.submittedval = 1
        self.assertEqual(el.value, 1)
        el = Form('f').add_checkbox('f', 'f', 'int')
        el.submittedval = 'checked'
        self.assertEqual(el.value, 1)
        
        # converted values int (false)
        el = Form('f').add_checkbox('f', 'f', 'int')
        el.submittedval = False
        self.assertEqual(el.value, 0)
        el = Form('f').add_checkbox('f', 'f', 'int')
        el.submittedval = 0
        self.assertEqual(el.value, 0)
        el = Form('f').add_checkbox('f', 'f', 'int')
        self.assertEqual(el.value, 0)

    def test_el_hidden(self):
        html = '<input class="hidden" id="f-field" name="field" type="hidden" />'
        el = Form('f').add_hidden('field', 'Field')
        self.assertEqual(str(el()), html)

    def test_el_image(self):
        html = '<input class="image" id="f-field" name="field" type="image" />'
        el = Form('f').add_image('field', 'Field')
        self.assertEqual(str(el()), html)

    def test_el_reset(self):
        html = '<input class="reset" id="f-field" name="field" type="reset" />'
        el = Form('f').add_reset('field', 'Field')
        self.assertEqual(str(el()), html)

    def test_el_submit(self):
        html = '<input class="submit" id="f-field" name="field" type="submit" />'
        el = Form('f').add_submit('field', 'Field')
        self.assertEqual(str(el()), html)

    def test_el_cancel(self):
        html = '<input class="submit" id="f-field" name="field" type="submit" />'
        el = Form('f').add_cancel('field', 'Field')
        self.assertEqual(str(el()), html)

    def test_el_text(self):
        html = '<input class="text" id="f-field" name="field" type="text" />'
        form = Form('f')
        el = form.add_element('text', 'field', 'Field')
        self.assertEqual(str(el()), html)
        
        html = '<input class="text" id="f-field" maxlength="1" name="field" type="text" />'
        form = Form('f')
        el = form.add_element('text', 'field', 'Field', maxlength=1)
        self.assertEqual(str(el()), html)
        el.submittedval = '1'
        self.assertEqual( el.value, '1')
        
        # too long
        el.submittedval = '12'
        self.assertEqual( el.is_valid(), False)
        
        # no validator
        form = Form('f')
        el = form.add_element('text', 'field', 'Field')        
        el.submittedval = '12'
        self.assertEqual( el.value, '12')

    def test_el_date(self):
        html = '<input class="text" id="f-field" name="field" type="text" />'
        el = Form('f').add_date('field', 'Field')
        self.assertEqual(str(el()), html)
        
        # our date-time object should get converted to the appropriate format
        html = '<input class="text" id="f-field" name="field" type="text" value="12/03/2009" />'
        el = Form('f').add_date('field', 'Field', defaultval=datetime.date(2009, 12, 3))
        self.assertEqual(str(el()), html)
        el.submittedval = '1/5/09'
        assert el.value == datetime.date(2009, 1, 5)
        el.submittedval = '2-30-04'
        assert not el.is_valid()
        
        # european style dates
        html = '<input class="text" id="f-field" name="field" type="text" value="03/12/2009" />'
        el = Form('f').add_date('field', 'Field', defaultval=datetime.date(2009, 12, 3), month_style='dd/mm/yyyy')
        self.assertEqual(str(el()), html)
        el.submittedval = '1/5/09'
        assert el.value == datetime.date(2009, 5, 1)
        el.submittedval = '2-30-04'
        assert not el.is_valid()
        
        # no-day dates
        html = '<input class="text" id="f-field" name="field" type="text" value="12/2009" />'
        el = Form('f').add_date('field', 'Field', defaultval=datetime.date(2009, 12, 3), accept_day=False)
        self.assertEqual(str(el()), html)
        el.submittedval = '5/09'
        assert el.value == datetime.date(2009, 5, 1)
        el.submittedval = '5/1/09'
        assert not el.is_valid()

    def test_el_email(self):
        html = '<input class="text" id="f-field" name="field" type="text" />'
        el = Form('f').add_email('field', 'Field')
        self.assertEqual(str(el()), html)
        el.submittedval = 'bob@example.com'
        assert el.value == 'bob@example.com'
        el.submittedval = 'bob'
        assert not el.is_valid()
        
        try:
            el = Form('f').add_email('field', 'Field', resolve_domain=True)
            el.submittedval = 'bob@ireallyhopethisdontexistontheweb.com'
            assert not el.is_valid()
        except ImportError:
            warnings.warn('skipping test b/c pyDNS not installed')
        
    def test_el_password(self):
        html = '<input class="password" id="f-f" name="f" type="password" />'
        el = Form('f').add_password('f')
        self.assertEqual(str(el()), html)
        
        # default vals don't show up
        el = Form('f').add_password('f', defaultval='test')
        self.assertEqual(str(el()), html)
        
        # submitted vals don't show up
        el = Form('f').add_password('f')
        el.submittedval = 'test'
        self.assertEqual(str(el()), html)
        
        # default vals w/ default_ok
        html = '<input class="password" id="f-f" name="f" type="password" value="test" />'
        el = Form('f').add_password('f', defaultval='test', default_ok=True)
        self.assertEqual(str(el()), html)
        
        # submitted vals w/ default_ok
        el = Form('f').add_password('f', default_ok=True)
        el.submittedval = 'test'
        self.assertEqual(str(el()), html)

    def test_el_time(self):
        html = '<input class="text" id="f-f" name="f" type="text" />'
        el = Form('f').add_date('f')
        self.assertEqual(str(el()), html)
        
        # defaults
        html = '<input class="text" id="f-field" name="field" type="text" value="13:00:00" />'
        el = Form('f').add_time('field', 'Field', defaultval=(13, 0))
        self.assertEqual(str(el()), html)
        el.submittedval = '20:30'
        assert el.value == (20,30)
        
        # some validator options
        html = '<input class="text" id="f-field" name="field" type="text" value="1:00pm" />'
        el = Form('f').add_time('field', 'Field', defaultval=(13, 0), use_ampm=True, use_seconds=False)
        self.assertEqual(str(el()), html)
        el.submittedval = '8:30pm'
        assert el.value == (20,30)

    def test_el_url(self):
        html = '<input class="text" id="f-f" name="f" type="text" />'
        el = Form('f').add_url('f')
        self.assertEqual(str(el()), html)
        
        html = '<input class="text" id="f-f" name="f" type="text" value="example.org" />'
        el = Form('f').add_url('f', defaultval="example.org", add_http=True)
        self.assertEqual(str(el()), html)
        el.submittedval = 'foo.com'
        self.assertEqual(el.value, 'http://foo.com')
        el.submittedval = 'foo'
        assert not el.is_valid()
        

# adding element of same name twice
# from_python validation problems

# run the tests if module called directly
if __name__ == "__main__":
    unittest.main()