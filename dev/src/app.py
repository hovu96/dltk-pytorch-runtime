import jupyterlab_server
import tornado.web
import os

# parameters: #https://github.com/jupyter/notebook/blob/master/notebook/notebookapp.py


class FitHandler(tornado.web.RequestHandler):
    def post(self):
        self.write("fit")


class ApplyHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("apply")


class PytorchApp(jupyterlab_server.LabServerApp):
    def start(self):
        self.web_app.add_handlers('.*$', [
            (r"/_dltk/fit", FitHandler),
            (r"/_dltk/apply", ApplyHandler),
        ])
        super().start()


if __name__ == "__main__":
    PytorchApp.launch_instance(
        port=os.getenv('PORT', 8888),
        open_browser=False,
        # notebook_dir="",
        allow_root=True,
        default_url="/",
        # base_url='/jupyterlab/',
        # debug=False,
        token="",
        # password=os.environ.get('HASHED_PWD'),
        ip="0.0.0.0",
    )
