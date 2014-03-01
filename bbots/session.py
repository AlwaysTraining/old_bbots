from bbot.App import App

class Session:
    def query(prompt):
        raise Exception("Need value provided for: %s" % prompt)

    def query_secret(prompt):
        raise Exception("Need secret value provided for: %s" % prompt)

    def __init__(self, rec):
        self.rec = rec
        self.app = App.App(rec, self.query, self.query_secret)
        app.run()


