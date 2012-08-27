import wx, glob, serial, sys
from obrazky import *
from move import *

status = 'Disconnected'
s = None

def scan():
    """scan for available ports. return a list of tuples (num, name)"""
    if sys.platform == 'linux2':
        return list(glob.glob('/dev/ttyUSB*'))
    else:
        available = []
        for i in range(256):
            try:
                s = serial.Serial("COM" + str(i))
                available.append( s.portstr)
                s.close() # explicit close 'cause of delayed GC in java
            except serial.SerialException:
                pass
        return available

class Arrows(wx.Frame):
    def __init__(self, parent, id, title, port):
        wx.Frame.__init__(self, parent, id, title, size=(720, 730),
                          style=wx.CLOSE_BOX | wx.CAPTION | wx.SYSTEM_MENU |
                                  wx.RESIZE_BORDER | wx.MINIMIZE_BOX)

        self.port = port
        self.s = serial.Serial(self.port, 115200, timeout=1)
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetStatusText(status)

        
        Arrows = arrowsPanel(self, -1, self.port)
        irPlotter = IrPlotter(self, -1, self.port)        
        
        #self.SetMinSize((230, 340))
        #self.SetMaxSize((230, 340))
        self.Centre()
        self.Show()

class Choose(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(310, 30))

        self.port = None
        self.s = None

        self.InitUI()
        self.Show()
        self.Centre()

    def OnConnect(self, event):
        if self.port is not None:
            self.Destroy()
            Arrows(None, -1, "SimpleBT", self.port)
        else:
            return
    
    def OnCombo(self, event):
        self.port = self.availablePorts.GetValue()

    def InitUI(self):
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        sc = scan()
        self.portText = wx.StaticText(self, -1, 'Port:')
        self.availablePorts = wx.ComboBox(self, -1, choices=sc, 
					style=wx.CB_READONLY)
        self.connectBtn = wx.Button(self, -1, 'Connect', style=wx.EXPAND )

        self.Bind(wx.EVT_BUTTON, self.OnConnect, self.connectBtn)
        self.Bind(wx.EVT_COMBOBOX, self.OnCombo, self.availablePorts)
    
        hbox.Add(self.portText)
        hbox.Add(self.availablePorts)
        hbox.Add(self.connectBtn)

        self.SetSizer(hbox) 
 
if __name__ == "__main__":
    app = wx.App()
    Choose(None, -1, 'Choose port - SimpleBT')
    app.MainLoop()
