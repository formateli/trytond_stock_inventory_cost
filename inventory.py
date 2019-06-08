# This file is part of trytond-stock_inventory_cost module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

from trytond.pool import PoolMeta
from trytond.model import fields
from decimal import Decimal
from trytond.modules.product import price_digits

__all__ = ['Inventory', 'InventoryLine']


class Inventory(metaclass=PoolMeta):
    __name__ = 'stock.inventory'

    total_cost = fields.Function(
        fields.Numeric('Total Cost', digits=price_digits),
            'get_total_cost')

    @fields.depends('lines')
    def on_change_lines(self):
        self.total_cost = self.get_total_cost()

    def get_total_cost(self, name=None):
        result = Decimal('0.0')
        for line in self.lines:
            if line.total_cost:
                result += line.total_cost
        return result

    @classmethod
    def complete_lines(cls, inventories, fill=True):
        super(Inventory, cls).complete_lines(inventories, fill)
        cls.set_cost_price(inventories)

    @classmethod
    def set_cost_price(cls, inventories):
        for inventory in inventories:
            for line in inventory.lines:
                line.cost_price = line.product.template.cost_price
                line.save()
            inventory.save()


class InventoryLine(metaclass=PoolMeta):
    __name__ = 'stock.inventory.line'

    cost_price = fields.Numeric(
            "Cost Price", readonly=True,
            digits=price_digits)
    total_cost = fields.Function(
        fields.Numeric('Total Cost', digits=price_digits),
            'get_total_cost')

    def on_change_product(self):
        super(InventoryLine, self).on_change_product()
        self.set_cost_price()

    @fields.depends('product')
    def on_change_quantity(self):
        super(InventoryLine, self).on_change_quantity()
        self.set_cost_price()

    def set_cost_price(self):
        self.cost_price = None
        self.total_cost = None
        if self.product:
            self.cost_price = self.product.template.cost_price
            self.total_cost = self.get_total_cost()

    def get_total_cost(self, name=None):
        if self.cost_price is None or \
                self.diff_quantity is None:
            return
        return Decimal(self.diff_quantity) * self.cost_price
