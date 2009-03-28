import datetime
from pysform import Form

class TestForm(Form):
    def __init__(self):
        Form.__init__(self, 'testform')

        el = self.add_header('input-els', 'Optional Elements')
        el = self.add_button('button', 'Button', defaultval='PushMe')
        el = self.add_checkbox('checkbox', 'Checkbox')
        el = self.add_file('file', 'File')
        el = self.add_hidden('hidden', defaultval='my hidden val')
        el = self.add_image('image', 'Image', defaultval='my image val', src='images/icons/b_edit.png')
        el = self.add_text('text', 'Text')
        el.add_note('a note')
        el.add_note('an <strong>HTML</strong> note', False)
        el = self.add_text('nolabel', defaultval='No Label')
        el.add_note('a note')
        el = self.add_password('password', 'Password')
        el = self.add_confirm('confirm', 'Confirm Password', match='password')
        el.add_note('confirm characters for password field are automatically masked')
        el = self.add_date('date', 'Date', defaultval=datetime.date(2009, 12, 3))
        el.add_note('note the automatic conversion from datetime object')
        emel = self.add_email('email', 'Email')
        el = self.add_confirm('confirmeml', 'Confirm Email', match=emel)
        el.add_note('note you can confirm with the name of the field or the element object')
        el.add_note('when not confirming password field, characters are not masked')
        el = self.add_time('time', 'Time')
        el = self.add_url('url', 'URL')
        options = [('1', 'one'), ('2','two')]
        el = self.add_select('select', options, 'Select')
        el = self.add_mselect('mselect', options, 'Multi Select')
        el = self.add_textarea('textarea', 'Text Area')
        el = self.add_fixed('fixed', 'Fixed', 'fixed val')
        el = self.add_fixed('fixed-no-label', defaultval = 'fixed no label')
        el = self.add_static('static', 'Static', 'static val')
        el = self.add_static('static-no-label', defaultval='static val no label')

        # want a header for div wrapping only, header element should not actually render
        el = self.add_header('header-for-div-wrap-only')
        el = self.add_text('hfdwo-t1', 'Text1')
        el = self.add_text('hfdwo-t2', 'Text2')
        
        # test header with blank text
        el = self.add_header('header-blank-text', '')
        el = self.add_text('hbt-t1', 'Text1')
        el = self.add_text('hbt-t2', 'Text2')