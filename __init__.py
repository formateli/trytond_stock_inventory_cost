# This file is part of trytond-stock_inventory_cost module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

from trytond.pool import Pool
from . import inventory

def register():
    Pool.register(
        inventory.Inventory,
        inventory.InventoryLine,
        module='stock_inventory_cost', type_='model')
