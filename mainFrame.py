import wx
import info
from menuPanel import *


class MainFrame(wx.Frame):
	def __init__(self):
		super().__init__(None, -1, f"장스월드 {info.version}")
		self.panelList = []
		self.panelList.append(MenuPanel(self))
		
		self.Show()
		
		