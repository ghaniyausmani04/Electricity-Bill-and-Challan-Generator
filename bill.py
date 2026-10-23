Fixed_Charges = 200.0
TV_FEE = 35.0
GST_RATE = 0.17
SURCHARGE_RATE = 0.10
DUE_DATE = "2026-10-15"

Slabs = [(100, 10), (200, 15), (300, 22), (700, 30), (None, 35)]

def units(prev, current):
    """Return units consumed, or none if reading is impossible"""
    if current < prev:
        return None
    return current - prev

def energycost(u):
    """cumulative slab cost: each band charged at its own rate"""
    cost = 0.0
    lower = 0
    remaining = u
    for upper, rate in Slabs:
        if remaining <= 0:
            break
        band = remaining if upper is None else min(remaining, upper - lower)
        cost += band * rate
        remaining -= band
        if upper is not None:
            lower = upper
    return cost
        
def makechallan(c):
    line = "-" * 40
    return (
        "Bijli Bill \n"
        f"consumer : {c['name']:<16} Ref: {c['ref']}\n"
        f"reading : {c['prev']} -> {c['current']}\n"
        f"units consumed {c['units']:>14}\n"
        f"{line}\n"
        f"energy cost(slabs) Rs {c['energy']:>10.2f}\n"
        f"fixed/meter charges Rs {Fixed_Charges:10.2f}\n"
        f"TV licence fee Rs {TV_FEE:>10.2f}\n"
        f"GST (17% of energy) Rs {c['gst']:>10.2f}\n"
        f"{line}\n"
        f"payable within due date Rs {c['within']:>10.2f}\n"
        f"payable after due date Rs {c['after']:>10.2f}\n"
        f"due date:{DUE_DATE}\n"
        
    )

def read_int(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("invalid input - pls enter a whole num")

def main():
    consumers = []
    while True:
        print()
        name = input("consumer name: ").strip()
        ref = input("reference number: ").strip()
        prev = read_int("previous reading: ")
        current = read_int("current reading: ")
        
        u = units(prev, current)
        if u is None:
            print("error: current reading is less than previous. entry skipped")
            continue
            
        energy = energycost(u)
        gst = energy * GST_RATE
        within = energy + Fixed_Charges + TV_FEE + gst
        after = within * (1 + SURCHARGE_RATE)
        
        c = {
            "name": name, "ref": ref, "prev": prev, "current": current,
            "units": u, "energy": energy, "gst": gst, "within": within, "after": after
        }
        consumers.append(c)
        
        challan = makechallan(c)
        print()
        print(challan)
        
        try:
            with open("bills.txt", "a") as f:
                f.write(challan + "\n")
        except OSError as e:
            print("could not save to billstxt:", e)
            
        again = input("bill another consumer? (y/n): ").strip().lower()
        if again != "y":
            break
            
    total_units = sum(c["units"] for c in consumers)
    total_revenue = sum(c["within"] for c in consumers)
    print("\n=======SUMMARY=========")
    print(f"consumers billed: {len(consumers)}")
    print(f"total units   : {total_units}")
    print(f"total revenue  : Rs {total_revenue:.2f}")

if __name__ == "__main__":
    main()
