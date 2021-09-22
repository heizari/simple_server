class simple_post:
    def post(self, params):
        print(params)
        return f"""\
            <html>
                <body>
                    <div style="width: 100%; font-size: 40px; font-weight: bold; text-align: center;">
                    <a href=index>back to home</a>
                    </div>
                    <div>
                        first:{params['first']}<br>
                        second:{params['second']}<br>
                    </div>
                </body>
            </html>
        """

    def index(self, params):
        return f"""\
            <html>
            <body>
                <div style="width: 100%; font-size: 40px; font-weight: bold; text-align: center;">
                <a href=index>back to home</a>
                </div>
                <h3>get test</h3>
                <form action=simple_get method=get>
                first:<input type=text name=get value=''><br>
                second:<input type=text name=getsec value=''><br>
                <input type=submit value=send />
                </form>

                <h3>post test</h3>
                <form action=simple_post method=post>
                    first:<input type=text name='first' /><br>
                    second:<input type=text name='second'/>
                    <input type=submit value=send />
                </form>
            </body>
            </html>
            """

    def get(self, params):
        print(params)
        return f"""\
            <html>
                <body>
                    <div style="width: 100%; font-size: 40px; font-weight: bold; text-align: center;">
                    <a href=index>back to home</a>
                    </div>
                    <div>
                        first:{params['get']}<br>
                        second:{params['getsec']}<br>
                    </div>
                </body>
            </html>
        """
