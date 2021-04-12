from flask import Flask, request
from middleware.query_engine.proxy import Proxy


def create_app():
    app = Flask(__name__)
    proxy = Proxy()

    @app.route('/api/raw-report', methods=["GET"])
    def raw_report():
        res = request.json

        try:
            report = proxy.retrieve_raw_reports(res)
            return report["report"].json
        except Exception as e:
            print(e)
            return {"error": "file not found"}

    @app.route('/api/generate-report', methods=["GET", "POST"])
    def generate_report():
        res = request.json

        try:
            report = proxy.generate_new_report(res)
            return report["report"].json
        except Exception as e:
            print(e)
            return {"error": "file not found"}

    return app


if __name__ == '__main__':
    create_app().run()