from flask import Flask, render_template
from flask import Flask, request, jsonify, render_template, send_from_directory

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("about.html")

@app.route('/assets/<path:filename>')
def serve_static(filename):
    return send_from_directory('templates/assets', filename)




if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5005, debug=True)