# import json
#
# from asgiref.sync import sync_to_async, async_to_sync
# from channels.consumer import AsyncConsumer, SyncConsumer
# from channels.generic.websocket import AsyncWebsocketConsumer
#
# from events.models import Event
#
#
# class EventConsumer(AsyncConsumer):
#
#     async def websocket_connect(self, event):
#         await self.send({
#              'type': "websocket.accept"
#         })
#         chat_room = 'post_room'
#         print('websocket_connect')
#         self.chat_room = chat_room
#         await self.channel_layer.group_add(
#             self.chat_room,
#             self.channel_name
#         )
#
#     async def websocket_receive(self, event):
#         front_msg_text = event.get('text', None)
#         if front_msg_text is not None:
#             dict_data = json.loads(front_msg_text)
#             event_id = dict_data.get('id')
#             print('event_id', event_id)
#             user_info = self.scope['user']
#             msg_data = {}
#             if event_id is not None:
#                 event = Event.objects.get(id=event_id)
#                 msg_data['charge_users'] = list(event.get_charge_users())
#
#             await self.send({
#                 "type": "websocket.send",
#                 "text": "From receive..."
#             })
#             # await self.channel_layer.group_send(
#             #     self.chat_room,
#             #     {
#             #     "type": "event_message",
#             #     "text": json.dumps(msg_data),
#             #      }
#             #  )
#
#     async def event_message(self, event):
#         print('event_message')
#         await self.send({
#             "type": "websocket.send",
#             "text": event['text'],
#         })
#
#     async def websocket_disconnect(self, event):
#         print('disconnect', event)
#



