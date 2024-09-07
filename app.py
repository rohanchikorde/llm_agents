"""
This module sets up a Flask web application with routes for rendering the index page
and processing POST requests to generate ice breakers.

Routes:
- /: Renders the index.html template.
- /process: Processes POST requests to generate ice breakers.
"""

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request

from ice_breaker import ice_break_with

load_dotenv()


app = Flask(__name__)


@app.route("/")
def index():
    """
    Renders the index page.

    Returns:
        Response: The rendered HTML of the index page.
    """
    return render_template("index.html")


@app.route("/process", methods=["POST"])
def process():
    """
    Processes POST requests to generate ice breakers.

    Returns:
        Response: A JSON response containing the generated ice breaker.
    """
    name = request.form["name"]
    summary_and_facts, profile_pic_url = ice_break_with(
        name=name
    )
    return jsonify(
        {
            "summary_and_facts": summary_and_facts,
            "picture_url": profile_pic_url,
        }
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
