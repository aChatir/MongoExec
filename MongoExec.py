import sublime, sublime_plugin, tempfile, os, subprocess

connection = None
connectionName = ''
collection = ''
history = ['']

class Connection:
    def __init__(self, options):
        self.settings = sublime.load_settings(options.type + ".mongoexec").get('mongo_exec')
        self.command  = sublime.load_settings("MongoExec.sublime-settings").get('mongo_exec.commands')[options.type]
        self.options  = options

    def _buildCommand(self, query):
        global collection
        if 'find' in query:
            query = query + ".toArray()"
        query = query.replace('"', '\\"')
        query = query.replace('$', '\\$')
        return '"' + self.command + '" ' + self.options.host + ':' + self.options.port + '/' + collection + " --eval \"printjson(%s)\"" % query

    def _getCommand(self, queryN):
        command  = self._buildCommand(queryN)
        self.tmp = tempfile.NamedTemporaryFile(mode = 'w', delete = False, suffix='.mongo')
        self.tmp.write(queryN + "\n")
        self.tmp.close()

        cmd = '%s < "%s"' % (command, self.tmp.name)
        print(command)

        return Command(cmd)

    def _filterOutput(self, command):
        itemsList = []
        for result in command.run().splitlines():
            try:
                if '[' in result and ']' in result:
                    result = result.replace('[', '')
                    result = result.replace(']', '')
                    result = result.replace('"', '')
                    for res in result.split(','):
                        if "system.indexes" != res.strip():
                            itemsList.append(res.strip())
                else:
                    if '"' in result:
                        result = result.replace('"', '')
                        result = result.replace(',', '')
                        if "system.indexes" != result.strip():
                            itemsList.append(result.strip())

            except IndexError:
                pass

        os.unlink(self.tmp.name)
        print(itemsList)

        return itemsList

    def list(self):
        command = self._buildCommand('db.getMongo().getDBNames()')
        dbs = Command(command).list()
        return dbs

    def execute(self, query):
        command = self._getCommand(query)
        command.show()
        os.unlink(self.tmp.name)

    def desc(self):
        command = self._getCommand('db.getMongo().getDBNames()')
        return self._filterOutput(command)

    def descCollections(self):
        command = self._getCommand('db.getCollectionNames()')
        return self._filterOutput(command)

class Command:
    def __init__(self, text):
        self.text = text

    def _display(self, panelName, text):
        if not sublime.load_settings("MongoExec.sublime-settings").get('show_result_on_window'):
            panel = sublime.active_window().create_output_panel(panelName)
            sublime.active_window().run_command("show_panel", {"panel": "output." + panelName})
        else:
            panel = sublime.active_window().new_file()

        panel.set_read_only(False)
        panel.set_syntax_file('Packages/JavaScript/JSON.tmLanguage')
        panel.run_command('append', {'characters': text})
        panel.set_read_only(True)

    def _result(self, text):
        self._display('MongoExec', text)

    def _errors(self, text):
        self._display('MongoExec.errors', text)

    def run(self):
        sublime.status_message(' MongoExec: running Mongo command')
        results, errors = subprocess.Popen(self.text, stdout=subprocess.PIPE,stderr=subprocess.PIPE, shell=True).communicate()

        if not results and errors:
            self._errors(errors.decode('utf-8', 'replace').replace('\r', ''))

        return results.decode('utf-8', 'replace').replace('\r', '')

    def show(self):
        results = self.run()

        if results:
            self._result(results)

    def list(self):
        results = self.run()

        return results

class Selection:
    def __init__(self, view):
        self.view = view
    def getQueries(self):
        text = []
        if self.view.sel():
            for region in self.view.sel():
                if region.empty():
                    text.append(self.view.substr(self.view.line(region)))
                else:
                    text.append(self.view.substr(region))

        return text

class Options:
    def __init__(self, name):
        '''mongodb://[username:passwor)d@]host1[:port1][,host2[:port2],...[,hostN[:portN]]][/[database][?options]]'''
        self.name     = name
        connections   = sublime.load_settings("MongoExec.sublime-settings").get('connections')
        self.type     = connections[self.name]['type']
        self.host     = connections[self.name]['host']
        self.port     = connections[self.name]['port']
        self.username = connections[self.name]['username']
        self.password = connections[self.name]['password']
        self.databases = connections[self.name]['databases']
        if 'service' in connections[self.name]:
            self.service  = connections[self.name]['service']

    def __str__(self):
        return self.name

    @staticmethod
    def list():
        names = []
        connections = sublime.load_settings("MongoExec.sublime-settings").get('connections')
        for connection in connections:
            names.append(connection)
        names.sort()
        return names

    def listDatabases():
        global connection
        dbs = connection.desc()
        dbs.sort()
        return dbs

    def listCollections():
        global connection
        collectionList = connection.descCollections()
        collectionList.sort()
        return collectionList

def mongoChangeConnection(index):
    global connection, connectionName, collection
    names = Options.list()
    options = Options(names[index])
    connectionName = names[index]
    collection = names[index]
    connection = Connection(options)
    sublime.status_message(' MongoExec: switched to %s connection' % names[index])
    sublime.active_window().run_command("mongo_list_dbs", {})

def fetchCollection(index):
    global connection
    names = Options.listCollections()
    query = sublime.load_settings("mongo.mongoexec").get('mongo_exec')['queries']['show records']['query']
    connection.execute(query % names[index])

def mongoChangeDB(index):
    global collection
    names = Options.listDatabases()
    collection = names[index]
    sublime.status_message(' MongoExec: switched to %s collection' % names[index])

def executeHistoryQuery(index):
    global history
    if index > -1:
        executeQuery(history[index])

def executeQuery(query):
    global connection
    global history
    history.append(query)
    if connection != None:
        connection.execute(query)

class mongoHistory(sublime_plugin.WindowCommand):
    global history
    def run(self):
        sublime.active_window().show_quick_panel(history, executeHistoryQuery)

class mongoQuery(sublime_plugin.WindowCommand):
    def run(self):
        global connection
        global history
        if connection != None:
            sublime.active_window().show_input_panel('Enter query', history[-1], executeQuery, None, None)
        else:
            sublime.error_message('No active connection')

class mongoListConnection(sublime_plugin.WindowCommand):
    def run(self):
        sublime.active_window().show_quick_panel(Options.list(), mongoChangeConnection)

class mongoListDbs(sublime_plugin.WindowCommand):
    def run(self):
        sublime.set_timeout(lambda: sublime.active_window().show_quick_panel(Options.listDatabases(), mongoChangeDB), 10)

class mongoListCollection(sublime_plugin.WindowCommand):
    def run(self):
        sublime.active_window().show_quick_panel(Options.listCollections(), fetchCollection)

class mongoExecute(sublime_plugin.WindowCommand):
    def run(self):
        global connection
        if connection != None:
            selection = Selection(self.window.active_view())
            for query in selection.getQueries():
                connection.execute(query)
        else:
            sublime.error_message('No active connection')
