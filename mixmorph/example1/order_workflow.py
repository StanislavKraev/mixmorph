from mixmorph.example1.data.order import OrderInfo
from mixmorph.example1.order_service import OrderService


class OrderWorkflow:

    def __init__(self, order_service: OrderService, mix: Mixmorph):
        self._order_service = order_service
        self._mix = mix

    def create_order(self, order_info: OrderInfo):
        self._order_service.make_order(order_info)
        self._mix.create('order_workflow')
