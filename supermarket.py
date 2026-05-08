from datetime import datetime
import csv
import os

ITEMS_CSV = "new_items.csv"      # stores new items added by user
BILL_CSV  = "bill_history.csv"   # stores every purchased item

# Default items
items = {
    "rice": 20,
    "sugar": 30,
    "oil": 100,
    "paneer": 150,
    "salt": 10,
    "groundnut": 50
}

# Load previously saved new items from CSV
if os.path.exists(ITEMS_CSV):
    with open(ITEMS_CSV, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            items[row["item"].lower()] = float(row['price'])

lists = '''
rice      rs 20/kg
sugar     rs 30/kg
oil       rs 100/litre
paneer    rs 150/kg
salt      rs 10/kg
groundnut rs 50/kg
'''

name = input("What is your name? ")

totalprice = 0
finalprice = 0
gst = 0
ilist = []
qlist = []
plist = []

option = int(input("list of items press 1, start billing press 2: "))
if option == 1:
    print(lists)

# ── BILLING LOOP ───────────────────────────────────────
while True:
    inp1 = int(input("want to buy press 1 or 2 for exit: "))
    if inp1 == 2:
        break
    if inp1 == 1:
        item = input("enter the item name: ").strip().lower()
        quantity = int(input("enter your quantity: "))

        if item not in items:
            # Unknown item - ask price and save to new_items.csv
            print(f"'{item}' not found in list.")
            new_price = float(input(f"Enter price per unit for '{item}': rs "))
            file_exists = os.path.exists(ITEMS_CSV)
            with open(ITEMS_CSV, "a", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=["item", "price"])
                if not file_exists:
                    writer.writeheader()
                writer.writerow({"item": item, "price": new_price})
            items[item] = new_price
            print(f"'{item}' saved to {ITEMS_CSV}!")

        price = quantity * items[item]
        print(f"price of {item} is {price}")

        totalprice += price
        ilist.append(item)
        qlist.append(quantity)
        plist.append(price)
        gst = (totalprice * 5) / 100
        finalprice = totalprice + gst

# ── BILL PRINT ─────────────────────────────────────────
inp = input('can i bill the items yes or no: ')
if inp == 'yes' and finalprice != 0:
    date_now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    print(25 * "=", "saisupermarket", 25 * "=")
    print(" wanaparty")
    print("name:", name, "  Date:", date_now)
    print(75 * "-")
    print(f"{'sno':<6} {'item':<20} {'quantity':<12} {'price'}")
    print(75 * "-")
    for i in range(len(ilist)):
        print(f"{i+1:<6} {ilist[i]:<20} {qlist[i]:<12} {plist[i]}")
    print(75 * "-")
    print("total price is", totalprice)
    print("gst is", gst)
    print("final price is", finalprice)
    print(75 * "=")

    # ── SAVE BILL TO bill_history.csv ──────────────────
    file_exists = os.path.exists(BILL_CSV)
    with open(BILL_CSV, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["date", "name", "item", "quantity", "price", "total", "gst", "finalprice"])
        if not file_exists:
            writer.writeheader()
        for i in range(len(ilist)):
            writer.writerow({
                "date": date_now,
                "name": name,
                "item": ilist[i],
                "quantity": qlist[i],
                "price": plist[i],
                "total": totalprice,
                "gst": gst,
                "finalprice": finalprice
            })
    print(f"\n✔ Bill saved to '{BILL_CSV}' successfully!")

else:
    print("thank you for shopping with saisupermarket!")