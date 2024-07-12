from channels.generic.websocket import WebsocketConsumer

from asgiref.sync import async_to_sync


searhing_buffer = []


class DataTransfer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)

        self.nickname = None
        self.companion = None
        self.is_connected = False

    def connect(self):
        # print('[ + ] Socket connected!')
        self.accept()

    def disconnect(self, close_code):
        if self.is_connected:
            async_to_sync(self.channel_layer.group_send)(
                self.companion,
                {
                    'type': 'new_data',
                    'data': {
                        'text': 'quit'
                    }
                }
            )
        else:
            for search in searhing_buffer:
                if search[0] == self.nickname:
                    searhing_buffer.remove(search)

    def receive(self, text_data):
        # print(f'[ ~ ] new data... {text_data}')
        if not self.is_connected:
            self.nickname, self.companion = text_data.split(';')

            async_to_sync(self.channel_layer.group_add)(
                self.nickname,
                self.channel_name
            )

            for search in searhing_buffer:
                if search[0] == self.companion and search[1] == self.nickname:
                    self.is_connected = True
                    searhing_buffer.remove(search)

                    async_to_sync(self.channel_layer.group_send)(
                        self.companion,
                        {
                            'type': 'new_data',
                            'data': {
                                'text': 'found'
                            }
                        }
                    )
                    self.send('found')

            if not self.is_connected:
                searhing_buffer.append((self.nickname, self.companion))

        else:
            async_to_sync(self.channel_layer.group_send)(
                self.companion,
                {
                    'type': 'new_data',
                    'data': {
                        'text': text_data
                    }
                }
            )

    def new_data(self, event):
        if event['data']['text'] == 'found':
            self.is_connected = True
        self.send(text_data=event['data']['text'])
