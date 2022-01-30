from flask import current_app
from flask_appbuilder import BaseView, expose, has_access

from . import app_builder


class MyView(BaseView):

    default_view = "method1"

    @expose("/method1/")
    @has_access
    def method1(self):
        # do something with param1
        # and return to previous page or index
        return "Hello"

    @expose("/method2/<string:param1>")
    @has_access
    def method2(self, param1):
        # do something with param1
        # and render template with param
        param1 = "Goodbye %s" % (param1)
        return param1

    @expose("/method3/<string:param1>")
    @has_access
    def method3(self, param1):
        # do something with param1
        # and render template with param
        param1 = "Goodbye %s" % (param1)
        return self.render_template("method3.html", param1=param1)


app_builder.add_view(MyView(), "Method1", category="My View")
app_builder.add_link("Method2", href="/myview/method2/jonh", category="My View")
app_builder.add_link("Method3", href="/myview/method3/jonh", category="My View")
app_builder.add_link("Dashboard", href="/dashapp/", category="My View")
