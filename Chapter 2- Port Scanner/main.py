import wx, pprint
import wx.lib.scrolledpanel as scrolled

class PortPanel(scrolled.ScrolledPanel):
    
    #---------------------------------------------------------------------------
    def __init__(self, parent):
        scrolled.ScrolledPanel.__init__(self, parent)


class PSPanel(wx.Panel):
    
    #---------------------------------------------------------------------------
    def __init__(self, parent):
        """ Constructor """
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour('WHITE')
        
        self.__createSizer()
        self.__createTexts()
        self.__createButtons()
        
        self.SetSizer(self.main_sizer)
        
    #---------------------------------------------------------------------------
    def __createSizer(self):
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        
    #---------------------------------------------------------------------------
    def __createTexts(self):
        """ Create Static Texts and Text Controls """
        # Create Widgets
        static_text = wx.StaticText(self, -1, "Enter IP address/HostName:")
        self.input_ctrl = wx.TextCtrl(self)
        
        # Create and set up Tool tip for input ctrl
        tip = wx.ToolTip("Enter a IP Address or Hostname ex: www.example.com")
        self.input_ctrl.SetToolTip(tip)
        
        # Create temp sizer to hold widgets
        tmp_sizer = wx.BoxSizer(wx.HORIZONTAL)
        tmp_sizer.Add(static_text, 0, wx.ALL, 5)
        tmp_sizer.Add(self.input_ctrl,1, wx.ALL, 5)
        
        # Add temp sizer to main sizer
        self.main_sizer.Add(tmp_sizer, 0, wx.ALL|wx.EXPAND, 5)

    #---------------------------------------------------------------------------
    def __createButtons(self):
        """ Create 'Scan Button' """
        scan_btn = wx.Button(self, -1, "Start Scan")
        
        # Bind button to event
        self.Bind(wx.EVT_BUTTON, self.onScan, scan_btn)
        
        self.main_sizer.Add(scan_btn, 0, wx.ALL|wx.ALIGN_CENTER, 5)

    #---------------------------------------------------------------------------
    def onScan(self, e):
        """ Called when scan_btn in pressed """
        if self.input_ctrl.GetValue() == "":
            wx.MessageBox("Please Enter IP Address or Hostname",
                          "Missing Information")
            return

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