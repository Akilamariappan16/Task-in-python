import base64
from docx import Document
from flask import Flask, jsonify,render_template,request
from werkzeug.utils import secure_filename
from pdf2docx import Converter
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/base64_convert',methods=['POST'])
def base64_convert():
    txt_files=request.files.getlist('txt_files')
    temp_folder = os.path.join(app.config['UPLOAD_FOLDER'],'temp')
    os.makedirs(temp_folder,exist_ok=True)
    
    docx_files=[]
    
    for txt_file in txt_files:
        if txt_file in txt_files:
            filename = secure_filename(txt_file.filename)
            txt_path = os.path.join(temp_folder,filename)
            txt_file.save(txt_path)
            
            docx_path = os.path.join(temp_folder,os.path.splitext(filename)[0]+".docx")
           
    
            with open(txt_path, "r") as file:
                content=file.read()
                encoded_bytes = base64.b64encode(content.encode('utf-8'))
                encoded_string = encoded_bytes.decode('utf-8') 
        
                doc = Document()
                doc.add_paragraph(encoded_string)
                doc.save(docx_path)
                
    
            # with open(docx_path, 'w') as file:
            #     file.writelines(docs)
        
    
            # converter = Converter(txt_path)
            # converter.convert(docx_path)
            # converter.close()
            
        docx_files.append(docx_path)
            
    return jsonify("File successfully converted",docx_files)

    
if __name__ == "__main__":
    app.run(debug=True)
