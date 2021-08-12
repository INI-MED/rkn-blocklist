# import urllib.parse
#
# from flask import Flask, request, redirect
#
# from storage import storage_instance
# from utils.swagger import swaggerui_blueprint, SWAGGER_URL
#
# server = Flask(__name__)
# server.register_blueprint(swaggerui_blueprint, urlprefix=SWAGGER_URL)
#
#
# @server.route("/")
# def url():
#     address = request.args.get("url")
#     if address is None:
#         return redirect("http://0.0.0.0:5000/swagger")
#
#     unquote_address = urllib.parse.unquote(address)
#     blocked = storage_instance.check(unquote_address)
#     return {"blocked_status": blocked}
#
#
# def start_server(*args):
#     server.run(host="0.0.0.0", port=5000)



