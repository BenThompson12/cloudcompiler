DEFAULT_FILE = "file"

def getInstructions(language, code):

    if (language == "python"):
        return getPythonInstructions(code)
    if (language == "java"):
        return getJavaInstructions(code)
    if (language == "javascript"):
        return getJavascriptInstructions(code)

    return None
    
def getPythonInstructions(code):
    return [
        {
            'action': 'createFile',
            'name'  : DEFAULT_FILE + '.py',
            'body'  : code,
        },
        {
            'action' : 'runCommand',
            'command': "python",
            'args'   : [DEFAULT_FILE + '.py']
        },
    ]

def getJavascriptInstructions(code):
    return [
        {
            'action': 'createFile',
            'name': DEFAULT_FILE + '.js',
            'body': code,
        },
        {
            'action': 'runCommand',
            'command': 'node',
            'args': [DEFAULT_FILE + '.js']
        },
    ]

def getJavaInstructions(code):
    return [
        {
            'action': 'createFile',
            'name'  : 'Main.java',
            'body'  : code,
        },
        {
            'action' : 'runCommand',
            'command': "javac",
            'args'   : ['Main.java']
        },
        {
            'action' : 'runCommand',
            'command': "java",
            'args'   : ['Main']
        },
    ]