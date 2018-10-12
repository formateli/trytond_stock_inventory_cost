# This file is part of trytond-stock_inventory_cost module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

from trytond.pool import Pool
from .inventory import *

def register():
    Pool.register(
        Inventory,
        InventoryLine,
        module='stock_inventory_cost', type_='model')
