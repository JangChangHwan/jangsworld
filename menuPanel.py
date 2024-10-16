import sys
import os
from os.path import *
from collections import namedtuple
import wx

MenuElement = namedtuple('MenuElement', 'code name kind parent data')

class MenuPanel(wx.Panel):
	def __init__(self, frame):
		super().__init__(frame, -1, size=(800, 600))
		# 메뉴 목록컨트롤
		self.menu = self.loadMenuData()
		self.curMenuCode = 'top'
		self.lcMenu = wx.ListCtrl(self, -1, (10, 20), (780, 580), style=wx.LC_REPORT|wx.LC_SINGLE_SEL)
		self.lcMenu.InsertColumn(0, '메뉴', width=600)
		self.lcMenu.InsertColumn(1, '코드', width=200)
		self.lcMenu.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.onEnter)
		self.openMenu(self.curMenuCode)
		# 히든 버튼 생성 + 단축키 지정
		accelList = []
		for keyName, accelKeys in (
			#('Enter', ((wx.ACCEL_NORMAL, wx.WXK_RETURN), (wx.ACCEL_NORMAL, wx.WXK_NUMPAD_ENTER))), 
			('Back', ((wx.ACCEL_NORMAL, wx.WXK_BACK), (wx.MOD_ALT, wx.WXK_LEFT))),
			):
			button = wx.Button(self, -1, keyName)
			button.Hide()
			button.Bind(wx.EVT_BUTTON, getattr(self, f"on{keyName}"))
			for modKeys, mainKey in accelKeys:
				accelList.append((modKeys, mainKey, button.GetId()))
		self.SetAcceleratorTable(wx.AcceleratorTable(accelList))
		
	def loadMenuData(self):
		menu = {}
		try:
			menuFilePath = join(dirname(__file__), 'menu.txt')
			with open(menuFilePath, 'r', encoding='utf8') as f:
				menuList = [line.split('\t') 
					for line in f.readlines() 
					if not line.startswith('#') and line.count('\t') == 4]
				menu = {code.strip(): MenuElement(code=code.strip(), name=name, kind=kind, parent=parent, data=data.strip())
					for code, name, kind, parent, data in menuList}
		except:
			pass
		return menu


	def openMenu(self, menuCode):
		try:
			self.lcMenu.DeleteAllItems()
			info = self.menu[menuCode]
			if info.kind == 'menu':
				childrenCodeList = info.data.split('|')
				for code in childrenCodeList:
					child = self.menu[code]
					index = self.lcMenu.InsertItem(sys.maxsize, child.name)
					self.lcMenu.SetItem(index, 1, child.code)
				self.curMenuCode = menuCode
				if self.lcMenu.ItemCount:
					self.lcMenu.Select(0)
					self.lcMenu.Focus(0)
		except Exception as e:
			errMsg = '\n'.join(e.args)
			wx.MessageBox(f'메뉴를 열지 못했습니다.\n{errMsg}', '오류', parent=self)

	def onEnter(self, evt):
		index = self.lcMenu.GetFocusedItem()
		if index == -1:
			return
		selMenuCode = self.lcMenu.GetItemText(index, 1)
		self.openMenu(selMenuCode)
		
	def onBack(self, evt):
		info = self.menu[self.curMenuCode]
		parentMenuCode = info.parent
		if not parentMenuCode:
			return
		self.openMenu(parentMenuCode)

