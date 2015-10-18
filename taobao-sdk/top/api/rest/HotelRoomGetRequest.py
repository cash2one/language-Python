'''
Created by auto_sdk on 2015.06.04
'''
from top.api.base import RestApi
class HotelRoomGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.gid = None
		self.item_id = None
		self.need_hotel = None
		self.need_room_desc = None
		self.need_room_quotas = None
		self.need_room_type = None
		self.outer_id = None
		self.rid = None

	def getapiname(self):
		return 'taobao.hotel.room.get'
