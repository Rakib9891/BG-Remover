
from flask import Flask, render_template, request, send_file
from rembg import remove
from PIL import Image
import os , io
import base64

app = Flask(__name__)

# Route 1 : Homepage (GET) - Shows the form
@app.route('/', methods=['GET'])
def home():
    return render_template("index.html")  #html file

#Route 2: Process Image (POST) - Handless the upload
@app.route('/remove-bg', methods=['POST'])
def remove_bg():
    if 'image' not in request.files:
        return "No file uploaded", 400
    
    file = request.files['image']
    if file.filename == '':
        return "Empty file", 400
    if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        return "Invalid file type", 400


    input_image = Image.open(file.stream)

    try:
        output_image = remove(input_image)
    except Exception as e:
        return f"Error: {str(e)}", 500

    
    if not os.path.exists('static/results'):
        os.makedirs('static/results')
    input_image = 'static/results/cleaned.png'
    output_image.save(input_image)






    #step 4: Save or return the result
    buffered = io.BytesIO()
    output_image.save(buffered, format='PNG')
    img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')

    
    return render_template("result.html", image_data=img_base64)

if __name__ == '__main__':
    app.run(debug=True)
    

