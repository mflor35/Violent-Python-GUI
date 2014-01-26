import wx
import wx.lib.scrolledpanel as scrolled
from socket import *
from threading import *
screenLock = Semaphore(value=1)

class PortPanel(scrolled.ScrolledPanel):
    
    #---------------------------------------------------------------------------
    def __init__(self, parent):
        scrolled.ScrolledPanel.__init__(self, parent)
        self.SetBackgroundColour("RED")
        self.__createSizer()
        
        self.SetSizer(self.main_sizer)
        self.SetAutoLayout(True)
        self.SetupScrolling()
        
    #---------------------------------------------------------------------------
    def __createSizer(self):
        """ Create Main Sizer """
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)

    #---------------------------------------------------------------------------
    def addPortInfo(self, port):
        """ Display info and add to sizer """
        print 'sup', port, type(port)
        port_text = wx.StaticText(self, -1, port)
        #self.main_sizer.Add(port_text, 0, wx.ALL|wx.ALIGN_CENTER, 5)
        wx.CallAfter(self.main_sizer.Add, port_text, 0, wx.ALL|wx.ALIGN_CENTER, 5)

class PSPanel(wx.Panel):
    
    #---------------------------------------------------------------------------
    def __init__(self, parent):
        """ Constructor """
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour('WHITE')
        
        self.__createSizer()
        self.__createTexts()
        self.__createButtons()
        self.__createScrollPanel()
        
        self.SetSizer(self.main_sizer)
        
    #---------------------------------------------------------------------------
    def __createSizer(self):
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        
    #---------------------------------------------------------------------------
    def __createTexts(self):
        """ Create Static Texts and Text Controls """
        # Create Static Texts
        target_text = wx.StaticText(self, -1, "Enter IP/HostName:")
        port_text = wx.StaticText(self, -1, "Enter Ports to scan:")
        
        # Create Text Ctrls
        self.target_input = wx.TextCtrl(self)
        self.port_input = wx.TextCtrl(self)
        
        # Create and set up tool tips
        target_tip = wx.ToolTip("Enter a IP Address or Hostname ex: www.example.com")
        port_tip = wx.ToolTip("Enter Multiple ports with commas ex:25, 35, 56")
        self.target_input.SetToolTip(target_tip)
        self.port_input.SetToolTip(port_tip)
        
        # Create temp sizer to hold widgets
        tmp_sizer1 = wx.BoxSizer(wx.VERTICAL)
        tmp_sizer2 = wx.BoxSizer(wx.VERTICAL)
        
        # Add widgets to tmp sizers
        tmp_sizer1.Add(target_text, 0, wx.ALL|wx.ALIGN_LEFT, 10)
        tmp_sizer1.Add(port_text, 0, wx.ALL|wx.ALIGN_LEFT, 10)
        
        tmp_sizer2.Add(self.target_input, 0, wx.ALL|wx.EXPAND, 5)
        tmp_sizer2.Add(self.port_input, 0, wx.ALL|wx.EXPAND, 5)
        
        tmp_sizer3 = wx.BoxSizer(wx.HORIZONTAL)
        tmp_sizer3.Add(tmp_sizer1)
        tmp_sizer3.Add(tmp_sizer2, 1, wx.EXPAND)
        
        # Add tmp sizers to main sizer
        self.main_sizer.Add(tmp_sizer3, 0, wx.EXPAND)

    #---------------------------------------------------------------------------
    def __createButtons(self):
        """ Create 'Scan Button' """
        scan_btn = wx.Button(self, -1, "Start Scan")
        
        # Bind button to event
        self.Bind(wx.EVT_BUTTON, self.onScan, scan_btn)
        
        self.main_sizer.Add(scan_btn, 0, wx.ALL|wx.ALIGN_CENTER, 5)
    
    #---------------------------------------------------------------------------
    def __createScrollPanel(self):
        self.scroll_panel = PortPanel(self)
        
        self.main_sizer.Add(self.scroll_panel, 1, wx.ALL|wx.EXPAND, 10)

    #---------------------------------------------------------------------------
    def onScan(self, e):
        """ Called when scan_btn in pressed """
        # Check if all fields are filled out
        if self.target_input.GetValue() == "":
            wx.MessageBox("Please Enter IP Address or Hostname",
                          "Missing Information")
            return
        if self.port_input.GetValue() == "":
            wx.MessageBox("Please Enter ports to be scanned",
                          "Missing Information")
            return
        
        tgtHost = self.target_input.GetValue()
        tgtPorts = self.port_input.GetValue().split(',')
        # Check if it's a real host
        try:
            tgtIP = gethostbyname(tgtHost)
        except:
            # Tell unresolvable 
            wx.MessageBox("Cannot resolve  '%s': Unkown Host" % tgtHost,
                          "Error")
            return
        
        # Try to get address
        try:
            tgtName = gethostbyaddr(tgtIP)
            print "[+] Scan results for: " + tgtName[0]
        except:
            print "[+] Scan results for: " + tgtIP
        setdefaulttimeout(1)
        for tgtPort in tgtPorts:
            t = Thread(target=self.connScan, args=(tgtHost, int(tgtPort)))
            t.start()
            
    #---------------------------------------------------------------------------
    def connScan(self, tgtHost, tgtPort):
        try:
            connSkt = socket(AF_INET, SOCK_STREAM)
            connSkt.connect((tgtHost, tgtPort))
            connSkt.send('Some text here\r\n')
            results = connSkt.recv(100)
            screenLock.acquire()
            port_info = "[+] %d /tcp Open" % tgtPort
            port_info += "\n[+] " + results
        except:
            screenLock.acquire()
            port_info = "[-] %d /tcp closed" % tgtPort
        finally:
            self.scroll_panel.addPortInfo(port_info)
            screenLock.release()
            connSkt.close()

class PortScanner(wx.Frame):
    
    #---------------------------------------------------------------------------
    def __init__(self, parent=None):
        """ Constructor """
        wx.Frame.__init__(self, parent, -1, "Port Scanner", size=(400,450))
        self.Center()
        
        self.__createSizer()
        self.__createPanels()
        
        self.SetSizer(self.main_sizer)
    #---------------------------------------------------------------------------
    def __createSizer(self):
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        
    def __createPanels(self):
        self.main_panel = PSPanel(self)
        
        self.main_sizer.Add(self.main_panel, 1, wx.EXPAND)

if __name__ == "__main__":
    app = wx.App(False)
    f = PortScanner()
    f.Show()
    app.MainLoop()