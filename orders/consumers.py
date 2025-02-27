import json
from channels.generic.websocket import AsyncWebsocketConsumer

class OrderStatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """Conecta o WebSocket a um pedido específico"""
        self.order_id = self.scope['url_route']['kwargs']['order_id']
        self.room_group_name = f"order_{self.order_id}"

        # Entra na sala do pedido
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        """Sai da sala ao desconectar"""
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def send_order_update(self, event):
        """Envia atualização do pedido para o WebSocket"""
        await self.send(text_data=json.dumps(event["message"]))
