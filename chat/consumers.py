# consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
from .utils import create_word_set
import json

word_set = create_word_set()
connected_users = {}
user_scores = {}
start_word = '안녕하세요'

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.nickname = self.scope['user'].nickname
        self.room_group_name = 'chat_%s' % self.room_name

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

        connected_users.setdefault(self.room_group_name, []).append(self.nickname)
        user_scores.setdefault(self.room_group_name, []).append({'nickname': self.nickname, 'score': 0})

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'user_list',
                'users': connected_users[self.room_group_name],
                'user_scores': user_scores[self.room_group_name],
            }
        )

    async def disconnect(self, close_code):
        if self.room_group_name in connected_users:
            if self.nickname in connected_users[self.room_group_name]:
                connected_users[self.room_group_name].remove(self.nickname)
                for user_score in user_scores[self.room_group_name]:
                    if user_score['nickname'] == self.nickname:
                        user_scores[self.room_group_name].remove(user_score)
                if not connected_users[self.room_group_name]:
                    del connected_users[self.room_group_name]

            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

            if self.room_group_name in connected_users:
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'user_list',
                        'users': connected_users.get(self.room_group_name, []),
                        'user_scores': user_scores.get(self.room_group_name, []),
                    }
                )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'nickname' : self.nickname,
            }
        )
        
    async def user_list(self, event):
        # Send user list to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'user_list',
            'users': event['users'],
            'user_scores': event['user_scores'],
        }))

    async def score_update(self, event):
        # Send user scores to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'score_update',
            'user_scores': event['user_scores'],
        }))

    async def chat_message(self, event):
        global start_word

        message = event['message']
        nickname = event['nickname']
        
        # print(user_scores[self.room_group_name])

        await self.send(text_data=json.dumps({
            'message': message,
            'nickname' : nickname,
        }))

        if (message[0] == start_word[len(start_word)-1]) and (message in word_set):
            start_word = message

            for user_score in user_scores[self.room_group_name]:
                if user_score['nickname'] == nickname:
                    user_score['score'] += 1

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'score_update',
                    'user_scores': user_scores[self.room_group_name],
                }
            )
            await self.send(text_data=json.dumps({
                'message': "정답입니다!",
            }))
