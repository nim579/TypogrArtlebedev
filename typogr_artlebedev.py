import sublime, sublime_plugin
import socket

class RemoteTypograf:

    _entityType = 4
    _useBr = 1
    _useP = 1
    _maxNobr = 3
    _encoding = 'UTF-8'

    def __init__(self, settings):
        if 'encoding' in settings:
            self._encoding   = settings['encoding']

        if 'entities' in settings:
            self._entityType = settings['entities']

        if 'useBr' in settings:
            self._useBr      = settings['useBr']

        if 'useP' in settings:
            self._useP       = settings['useP']

        if 'maxNobr' in settings:
            self._maxNobr    = settings['maxNobr']

    def processText(self, text):
        PY3 = sys.version.startswith('3.')

        text = text.replace('&', '&amp;')
        text = text.replace('<', '&lt;')
        text = text.replace ('>', '&gt;')

        SOAPBody  = '<?xml version="1.0" encoding="%s"?>\n' % self._encoding
        SOAPBody += '<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">\n'
        SOAPBody += '<soap:Body>\n'
        SOAPBody += ' <ProcessText xmlns="http://typograf.artlebedev.ru/webservices/">\n'
        SOAPBody += '  <text>%s</text>\n' % text
        SOAPBody += '     <entityType>%s</entityType>\n' % self._entityType
        SOAPBody += '     <useBr>%s</useBr>\n' % self._useBr
        SOAPBody += '     <useP>%s</useP>\n' % self._useP
        SOAPBody += '     <maxNobr>%s</maxNobr>\n' % self._maxNobr
        SOAPBody += '   </ProcessText>\n'
        SOAPBody += ' </soap:Body>\n'
        SOAPBody += '</soap:Envelope>\n'

        host = 'typograf.artlebedev.ru';
        SOAPRequest  = 'POST /webservices/typograf.asmx HTTP/1.1\n'
        SOAPRequest += 'Host: typograf.artlebedev.ru\n'
        SOAPRequest += 'Content-Type: text/xml\n'
        SOAPRequest += 'Content-Length: %d\n' % len(SOAPBody)
        SOAPRequest += 'SOAPAction: "http://typograf.artlebedev.ru/webservices/ProcessText"\n\n'

        SOAPRequest += SOAPBody

        if PY3:
            SOAPRequest = SOAPRequest.encode('utf-8')

        remoteTypograf = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        remoteTypograf.connect((host, 80))
        remoteTypograf.send(SOAPRequest)

        typografResponse = ''
        while 1:
            buf = remoteTypograf.recv(8192)
            if len(buf)==0: break

            if PY3:
                buf = buf.decode()

            typografResponse += buf

        remoteTypograf.close()

        startsAt = typografResponse.find('<ProcessTextResult>') + 19
        endsAt = typografResponse.find('</ProcessTextResult>')
        typografResponse = typografResponse[startsAt:endsAt]

        typografResponse = typografResponse.replace('&amp;', '&' )
        typografResponse = typografResponse.replace('&lt;', '<')
        typografResponse = typografResponse.replace ('&gt;', '>')

        return  typografResponse


class TypogrArtlebedevCommand(sublime_plugin.TextCommand):
    def run(self, edit, **args):
        v = self.view
        settings = sublime.load_settings('TypogrArtlebedev.sublime-settings')

        settingsObject = {
            'encoding': settings.get('text_encoding'),
            'entities': settings.get('entity_type'),
            'useBr':    settings.get('use_br'),
            'useP':     settings.get('use_p'),
            'maxNobr':  settings.get('max_nobr')
        }

        if 'encoding' in args:
            settingsObject['encoding'] = args['encoding']

        if 'entities' in args:
            settingsObject['entities'] = args['entities']

        if 'use_br' in args:
            settingsObject['useBr'] = args['use_br']

        if 'use_p' in args:
            settingsObject['useP'] = args['use_p']

        if 'max_nobr' in args:
            settingsObject['maxNobr'] = args['max_nobr']

        text = v.substr(v.sel()[0])

        rt = RemoteTypograf(settingsObject)
        typogrText = rt.processText(text)
        print(typogrText)
        v.replace(edit, v.sel()[0], typogrText)
