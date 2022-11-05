from flask import *
import PyPDF2

# initialise flask application
app = Flask(__name__)

#POST is used because rotate is kind of an update operation on an exixsting resource
@app.route('/rotate', methods=['POST'])
def rotatePDF():
    #Getting parameters
    data = request.get_json()
    print(data)
    file_path = data['file_path']
    angle_of_rotation = data["angle_of_rotation"]
    page_number = data["page_number"]

    # To save output file in same folder
    output_path = file_path[:file_path.rfind('/')] + '/rotated.pdf'

    pdf_in = open(file_path, 'rb')
    pdf_reader = PyPDF2.PdfFileReader(pdf_in)
    pdf_writer = PyPDF2.PdfFileWriter()

    for pagenum in range(pdf_reader.numPages):
        page = pdf_reader.getPage(pagenum)
        if pagenum+1 == page_number:    # +1 because numbering starts from 1
            page.rotateClockwise(angle_of_rotation)
        pdf_writer.addPage(page)

    pdf_out = open(output_path, 'wb')
    pdf_writer.write(pdf_out)
    pdf_out.close()
    pdf_in.close()

    return jsonify({ 'path': output_path })



if __name__ == '__main__':
    app.run(host="127.0.0.1")