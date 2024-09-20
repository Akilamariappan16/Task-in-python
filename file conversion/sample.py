import os
from flask import Flask, jsonify,render_template,request
from werkzeug.utils import secure_filename
from pdf2docx import Converter
from docx import Document


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert',methods=['POST'])
def convert():
    txt_files=request.files.getlist('txt_files')
    temp_folder = os.path.join(app.config['UPLOAD_FOLDER'],'temp')
    os.makedirs(temp_folder,exist_ok=True)
    
    pdf_files=[]
    
    for txt_file in txt_files:
        if txt_file in txt_files:
            filename = secure_filename(txt_file.filename)
            txt_path = os.path.join(temp_folder,filename)
            txt_file.save(txt_path)
            
            pdf_path = os.path.join(temp_folder,os.path.splitext(filename)[0]+".pdf")
            
            
            with open(txt_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()
            
                
            converter = Converter(txt_path)
            converter.convert(pdf_path)
            converter.close()
            
            pdf_files.append(pdf_path)
            
        return jsonify("File successfully converted",pdf_files)




@app.route('/converting_txt',methods=['POST'])
def converting_txt():
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
           
            document = Document()
            with open(txt_path, 'rb') as file:
                 lines = file.read()
                 for line in lines:
                      document.add_paragraph(line) 
            
           
            converter = Converter(txt_path)
            converter.convert(docx_path)
            converter.close()
            
            docx_files.append(docx_path)
            
        return jsonify("File successfully converted",docx_files)


@app.route('/converting_py',methods=['POST'])
def converting_py():
    txt_files=request.files.getlist('txt_files')
    temp_folder = os.path.join(app.config['UPLOAD_FOLDER'],'temp')
    os.makedirs(temp_folder,exist_ok=True)
    
    py_files=[]
    
    for txt_file in txt_files:
        if txt_file in txt_files:
            filename = secure_filename(txt_file.filename)
            txt_path = os.path.join(temp_folder,filename)
            txt_file.save(txt_path)
            
            py_path = os.path.join(temp_folder,os.path.splitext(filename)[0]+".py")
           
            with open(txt_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()
            with open(py_path, 'w', encoding='utf-8') as file:
                file.writelines(lines)
                
            converter=Converter(txt_path)
            converter.convert(py_path)
            converter.close()
              
            py_files.append(py_path)
        return jsonify("File successfully converted",py_files)




if __name__ == "__main__":
    app.run(debug=True)