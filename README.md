# Django-Report-Generating
A really basic proof of concept for generating a report from a template, and editing it in browser before rendering it to a pdf.

# To use
clone the repo. Install the requirements. run the server. 

go to /reports/generate/TEMPLATE_NAME/MESSAGE. This will render a template in the djangoreports/templates folder with your message.
Currently availble templates are "test-template" and "test-template2". Make sure your message doesn't have any whitespace or special characters.

The app will render the template with your message. You can then edit the message in browser, and click submit to render it to a PDF.
