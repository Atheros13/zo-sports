
class ContactFormChoice():

    ''' An object that contains the button_text, description and form for a Form choice 
    on a Contact page. '''

    def __init__(self, title, description, form):

        self.title = title
        self.description = description
        self.form = form

    def process_contact(self, request_data):

        pass
