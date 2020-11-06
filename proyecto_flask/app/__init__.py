from flask import Flask
from products.views import test

app = Flask(__name__)

@app.route('/product/<name>', methods=['GET'])
def product_info(name):
    return 'El nombre del prodcuto es: {}'.format(name)
app.register_blueprint(test)
if __name__ == "__main__":
    app.run(debug=True)

