from collections import defaultdict


class Product:
    def __init__(self, name, sku):
        self.name = name
        self.sku = sku


class Warehouse:  # warehouse with infinity capacity
    def __init__(self, warehouse_id):
        self.warehouse_id = warehouse_id
        self.stock = defaultdict(int)

    def add_product(self, sku, quantity):
        self.stock[sku] += quantity

    def remove_product(self, sku, quantity):
        if sku not in self.stock:
            print("ERROR UNSTOCKING PRODUCT WITH SKU %s NOT IN WAREHOUSE" % sku)
            return
        self.stock[sku] -= min(quantity, self.stock[sku])
        if self.stock.get(sku, None) == 0:
            self.stock.pop(sku)

    def list_product(self):
        return list(self.stock.items())


class WarehouseWithLimit:
    def __init__(self, warehouse_id, limit):
        self.warehouse_id = warehouse_id
        self.limit = int(limit)
        self.stock = defaultdict(int)
        self.current_quantity = 0

    def add_product(self, sku, quantity):
        self.stock[sku] += min(self.limit - self.current_quantity, quantity)
        self.current_quantity = min(
            self.current_quantity + quantity, self.limit)

    def remove_product(self, sku, quantity):
        if sku not in self.stock:
            print("ERROR UNSTOCKING PRODUCT WITH SKU %s NOT IN WAREHOUSE" % sku)
            return
        self.stock[sku] -= min(quantity, self.stock[sku])
        self.current_quantity -= min(quantity, self.stock[sku])
        if self.stock.get(sku, None) == 0:
            self.stock.pop(sku)

    def list_product(self):
        return list(self.stock.items())


class Company:
    def __init__(self):
        self.warehouses = {}
        self.product_catalog = {}

    def add_warehouse(self, new_warehouse, limit=None):
        if new_warehouse in self.warehouses:
            print(
                "ERROR ADDING WAREHOUSE WAREHOUSE with ID %s ALREADY EXISTS" % new_warehouse)
        if limit:
            self.warehouses[new_warehouse] = WarehouseWithLimit(
                new_warehouse, limit)
        else:
            self.warehouses[new_warehouse] = Warehouse(new_warehouse)

    def add_product(self, product_name, sku):
        if sku in self.product_catalog:
            print("ERROR ADDING PRODUCT PRODUCT with SKU %s ALREADY EXISTS" % sku)
        else:
            self.product_catalog[sku] = Product(product_name, sku)

    def stock(self, sku, warehouse_id, quantity):
        if sku not in self.product_catalog:
            print("ERROR STOCKING PRODUCT with SKU %s DOES NOT EXIST" % sku)
            return
        if warehouse_id not in self.warehouses:
            print("ERROR STOCKING INVALID WAREHOUSE ID %s" % warehouse_id)
            return
        self.warehouses[warehouse_id].add_product(sku, int(quantity))

    def unstock(self, sku, warehouse_id, quantity):
        if sku not in self.product_catalog:
            print("ERROR UNSTOCKING PRODUCT with SKU %s DOES NOT EXIST" % sku)
            return
        if warehouse_id not in self.warehouses:
            print("ERROR UNSTOCKING INVALID WAREHOUSE ID %s" % warehouse_id)
            return
        self.warehouses[warehouse_id].remove_product(sku, int(quantity))

    def list_products(self):
        for product in self.product_catalog.values():
            print(product.name, product.sku)

    def list_warehouses(self):
        print("WAREHOUSES")
        for w_id in self.warehouses:
            print(w_id)

    def list_warehouse(self, warehouse_id):
        if warehouse_id not in self.warehouses:
            print("ERROR UNSTOCKING INVALID WAREHOUSE ID %s" % warehouse_id)
            return
        products = [(self.product_catalog[sku].name, sku, qty)
                    for sku, qty in self.warehouses[warehouse_id].list_product()]
        len_name = max([len(i) for i, _, _ in products])
        len_sku = len(products[0][1])
        print("ITEM_NAME".ljust(len_name),
              "ITEM_SKU".ljust(len_sku), "QTY", sep="\t")
        for name, sku, quantity in products:
            print(name.ljust(len_name), sku.ljust(len_sku), quantity, sep="\t")


def run_command(company, command):
    command = command.split(" ")
    if command[0] == "STOCK":
        company.stock(*command[1:])
    elif command[0] == "UNSTOCK":
        company.unstock(*command[1:])
    elif command[0] == "LIST":
        if command[1] == "PRODUCTS":
            company.list_products()
        elif command[1] == "WAREHOUSES":
            company.list_warehouses()
        else:
            company.list_warehouse(command[2])
    else:  # "ADD"
        if command[1] == "WAREHOUSE":
            company.add_warehouse(*command[2:])
        else:
            sku = command[-1]
            product_name = " ".join(command[2:-1])[1:-1]
            company.add_product(product_name, sku)


def main(log_file="log.txt"):
    company = Company()
    print("""Welcome to warehose management system.
To quit use Ctrl-D(*nix)/Ctrl-Z&Enter(Windows)""")
    with open(log_file, "w") as f:
        history = []
        while True:
            try:
                command = input()
            except EOFError:
                break
            if command == "" or command[0] == "#":
                continue
            history.append(command + "\n")
            if len(history) == 2:
                f.write(history[0])
                f.write(history[1])
                history.clear()
            # print("running: ", command)
            run_command(company, command)


if __name__ == "__main__":
    main("log.txt")
