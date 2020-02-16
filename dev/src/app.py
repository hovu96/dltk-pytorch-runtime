import jupyterlab_server
import tornado.web
import os

# parameters: #https://github.com/jupyter/notebook/blob/master/notebook/notebookapp.py


notebook_name = "Algo.ipynb"
notebook_dir = os.getenv('NOTEBOOK_PATH', "/notebooks")
notebook_file = os.path.join(notebook_dir, notebook_name)


class FitHandler(tornado.web.RequestHandler):
    def post(self):
        self.write("fit")


class ApplyHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("apply")


class NotebookHandler(tornado.web.RequestHandler):
    def check_xsrf_cookie(self):
        pass

    def get(self):
        try:
            with open(notebook_file, 'r') as f:
                source = f.read()
            self.write(source)
        except FileNotFoundError:
            self.set_status(404)

    def put(self):
        source = self.request.body
        with open(notebook_file, "w") as f:
            f.write(source)


class PytorchApp(jupyterlab_server.LabServerApp):
    def start(self):
        self.web_app.add_handlers('.*$', [
            (r"/_dltk/fit", FitHandler),
            (r"/_dltk/apply", ApplyHandler),
            (r"/_dltk/notebook", NotebookHandler),
        ])
        super().start()


if __name__ == "__main__":
    PytorchApp.launch_instance(
        port=os.getenv('PORT', 8888),
        open_browser=False,
        notebook_dir=notebook_dir,
        allow_root=True,
        default_url="/notebooks/%s" % notebook_name,
        # base_url='/jupyterlab/',
        # debug=False,
        token="",
        # password=os.environ.get('HASHED_PWD'),
        ip="0.0.0.0",
        disable_check_xsrf=True,
    )
