from flask import Flask, request, jsonify,render_template,send_file
from LoadAndRun import run
import io
from PIL import Image

app = Flask(__name__,static_url_path='/static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST','GET'])
def calculate():
    data = request.get_json()
    place = data.get('place')
    latitude = float(data.get('latitude'))
    longitude = float(data.get('longitude'))
    print(place,latitude,longitude)
    run(place, latitude, longitude)
    x =  render_template('./result.html')
    print(x)
    return x

@app.route('/result.html', methods=['POST','GET'])
def returnResultPage():
    return render_template('./result.html')

@app.route('/downlod.png', methods=['POST','GET'])
def loadUnprocessedImage():
    return send_file("downlod.png", mimetype='image/png')

@app.route('/finalOutput.png', methods=['POST','GET'])
def loadprocessedImage():
    return send_file("finalOutput.png", mimetype='image/png')

@app.route('/About.html')
def about():
    return render_template('About.html')

@app.route('/How.html')
def how():
    return render_template('How.html')

if __name__ == '__main__':
    app.run(debug=True)