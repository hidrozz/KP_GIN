from burp import IBurpExtender, ITab, IHttpListener, IMessageEditorController
from java.awt import Component
from java.io import PrintWriter
from java.text import SimpleDateFormat
from java.util import ArrayList, Date
from javax.swing import JScrollPane, JSplitPane, JTabbedPane, JTable, JPanel, JTextField, JButton
from javax.swing.table import AbstractTableModel
from java.awt import FlowLayout
from threading import Lock
import time


class BurpExtender(IBurpExtender, ITab, IHttpListener, IMessageEditorController, AbstractTableModel):

    def __init__(self):
        self._filterPanel = FilterPanel(self)
    def registerExtenderCallbacks(self, callbacks):
        self._callbacks = callbacks
        self._helpers = callbacks.getHelpers()
        callbacks.setExtensionName("Custom logger")
        self._log = ArrayList()
        self._lock = Lock()
        self._table_counter = 1 
        self._splitpane = JSplitPane(JSplitPane.VERTICAL_SPLIT)
        logTable = Table(self)
        scrollPane = JScrollPane(logTable)
        self._splitpane.setLeftComponent(scrollPane)
        tabs = JTabbedPane()
        self._requestViewer = callbacks.createMessageEditor(self, False)
        self._responseViewer = callbacks.createMessageEditor(self, False)
        tabs.addTab("Request", self._requestViewer.getComponent())
        tabs.addTab("Response", self._responseViewer.getComponent())
        self._splitpane.setRightComponent(tabs)
        callbacks.customizeUiComponent(self._splitpane)
        callbacks.customizeUiComponent(logTable)
        callbacks.customizeUiComponent(scrollPane)
        callbacks.customizeUiComponent(tabs)
        callbacks.addSuiteTab(self)
        callbacks.registerHttpListener(self)
        return
    def getTabCaption(self):
        return "Logger"

    def getUiComponent(self):
        return self._splitpane

    def processHttpMessage(self, toolFlag, messageIsRequest, messageInfo):
        start_time = time.time()

        if messageIsRequest:
            return

        httpService = messageInfo.getHttpService()
        host = httpService.getHost()

        method = self._helpers.analyzeRequest(messageInfo).getMethod()

        url = self._helpers.analyzeRequest(messageInfo).getUrl()
        path = url.getPath()
        query_params = url.getQuery()

        response = messageInfo.getResponse()
        responseInfo = self._helpers.analyzeResponse(response)
        status_code = responseInfo.getStatusCode()
        headers = responseInfo.getHeaders()
        content_type = None

        for header in headers:
            if header.startswith("Content-Type: "):
                content_type = header[len("Content-Type: "):]
                break

        self._lock.acquire()
        row = self._log.size()
        self._log.add(LogEntry(self._table_counter, toolFlag, self._callbacks.saveBuffersToTempFiles(messageInfo),
                               url, host, start_time, None, status_code, content_type, "Incomplete", method, path,
                               query_params))
        self.fireTableRowsInserted(row, row)
        self._table_counter += 1  
        self._lock.release()

        self._lock.acquire()
        for i in range(self._log.size() - 1, -1, -1):
            logEntry = self._log.get(i)
            if logEntry._request_time is not None and logEntry._response_time is None:
                logEntry._response_time = start_time
                logEntry._complete = "Complete"
                break
        self._lock.release()

    def getRowCount(self):
        try:
            return self._log.size()
        except:
            return 0

    def getColumnCount(self):
        return 12

    def getColumnName(self, columnIndex):
        if columnIndex == 0:
            return "#"
        if columnIndex == 1:
            return "Tool"
        if columnIndex == 2:
            return "URL"
        if columnIndex == 3:
            return "Host"
        if columnIndex == 4:
            return "Request Time"
        if columnIndex == 5:
            return "Response Time"
        if columnIndex == 6:
            return "Status Code"
        if columnIndex == 7:
            return "Status"
        if columnIndex == 8:
            return "Method"
        if columnIndex == 9:
            return "Content Type"
        if columnIndex == 10:
            return "Path Component"
        if columnIndex == 11:
            return "Query Parameters"
        return ""

    def getValueAt(self, rowIndex, columnIndex):
        logEntry = self._log.get(rowIndex)
        if columnIndex == 0:
            return logEntry._table_number
        if columnIndex == 1:
            return self._callbacks.getToolName(logEntry._tool)
        if columnIndex == 2:
            return logEntry._url.toString()
        if columnIndex == 3:
            return logEntry._host
        if columnIndex == 4:
            if logEntry._request_time is not None:
                return self.format_time(logEntry._request_time)
            else:
                return ""
        if columnIndex == 5:
            if logEntry._response_time is not None:
                return self.format_time(logEntry._response_time)
            else:
                return ""
        if columnIndex == 6:
            return logEntry._status_code if logEntry._status_code is not None else ""
        if columnIndex == 7:
            return "Incomplete" if logEntry._complete == "Incomplete" else "Complete"
        if columnIndex == 8:
            return logEntry._method
        if columnIndex == 9:
            return logEntry._content_type if logEntry._content_type is not None else ""
        if columnIndex == 10:
            return logEntry._path
        if columnIndex == 11:
            return logEntry._query_params
        return ""

    def format_time(self, timestamp):
        date_format = SimpleDateFormat("yyyy-MM-dd HH:mm:ss")
        date = Date(long(timestamp * 1000))
        return date_format.format(date)

    def getHttpService(self):
        return self._currentlyDisplayedItem.getHttpService()

    def getRequest(self):
        return self._currentlyDisplayedItem.getRequest()

    def getResponse(self):
        return self._currentlyDisplayedItem.getResponse()

class Table(JTable):
    def __init__(self, extender):
        self._extender = extender
        self.setModel(extender)
        self._filteredLog = [] 

    def filterByKeyword(self, keyword):
        self._filteredLog.clear()

        for logEntry in self._extender._log:
            if keyword.lower() in logEntry._url.toString().lower() \
                    or keyword.lower() in logEntry._host.lower() \
                    or keyword.lower() in str(logEntry._request_time).lower() \
                    or keyword.lower() in str(logEntry._response_time).lower() \
                    or keyword.lower() in str(logEntry._status_code).lower() \
                    or keyword.lower() in logEntry._complete.lower() \
                    or keyword.lower() in logEntry._method.lower() \
                    or keyword.lower() in logEntry._content_type.lower() \
                    or keyword.lower() in logEntry._path.lower() \
                    or keyword.lower() in logEntry._query_params.lower():
                self._filteredLog.append(logEntry)
        self._extender.fireTableDataChanged()

    def changeSelection(self, row, col, toggle, extend):
        logEntry = self._extender._log.get(row)
        self._extender._requestViewer.setMessage(logEntry._requestResponse.getRequest(), True)
        self._extender._responseViewer.setMessage(logEntry._requestResponse.getResponse(), False)
        self._extender._currentlyDisplayedItem = logEntry._requestResponse

        JTable.changeSelection(self, row, col, toggle, extend)

class LogEntry:
    def __init__(self, table_number, tool, requestResponse, url, host, request_time, response_time, status_code,
                 content_type, complete, method, path, query_params):
        self._table_number = table_number
        self._tool = tool
        self._requestResponse = requestResponse
        self._url = url
        self._host = host
        self._request_time = request_time
        self._response_time = response_time
        self._status_code = status_code
        self._content_type = content_type
        self._complete = complete
        self._method = method
        self._path = path
        self._query_params = query_params

class FilterPanel(JPanel):
    def __init__(self, table):
        JPanel.__init__(self)
        self._table = table
        self.setLayout(FlowLayout(FlowLayout.LEFT))
        self._searchTextField = JTextField(20)
        self.add(self._searchTextField)
        self._searchButton = JButton("Search")
        self._searchButton.addActionListener(self.searchButtonClicked)
        self.add(self._searchButton)

    def searchButtonClicked(self, event):
        keyword = self._searchTextField.getText()
        self._table.filterByKeyword(keyword)

