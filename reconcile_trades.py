import json
import argparse
import csv
import datetime
import os

trades1=[]
trades2=[]

script_path = os.path.realpath(__file__)
path=os.path.dirname(script_path)
timestamp = datetime.datetime.now().strftime("%Y-%m-%d")
# print(timestamp, path)
file1 = path + '/system1/'+ 'system1_trades_' + timestamp + '.json'
file2 = path + '/system2/'+ 'system2_trades_' + timestamp + '.json'

# print(file1, file2)

if not (file1):
    file1 = path + '/system1/'+ f'system1_trades_' + timestamp + '.csv'
    if not (file1):
        print("Remember you'r file input name must be", path + 'system1/'+ f'system1_trades_' + timestamp + '.json', "or", path + 'system1/'+ f'system1_trades_' + timestamp + '.csv')
        exit(1)
if not (file2):
    file2 = path + '/system2/'+ f'system2_trades_' + timestamp + '.csv'
    if not (file2):
        print("Remember you'r file input name must be", path + 'system2/'+ f'system2_trades_' + timestamp + '.json', "or", path + 'system2/'+ f'system2_trades_' + timestamp + '.csv')
        exit(1)

# print(file1, file2)
with open(file1, 'r') as file:
    trades1 = json.load(file)
with open(file2, 'r') as file:
    trades2 = json.load(file)


mismatch_report = []
with open(path+'mismatch_report.json', 'w') as file:
    for key in trades1:
        trade1 = trades1[key]
        trade2 = trades2[key]
        if trade1['price'] != trade2['price']:
            mismatch_report.append({
                'trade_id': key
            })
        elif trade1['quantity'] != trade2['quantity']:
            mismatch_report.append({
                'trade_id': key
            })
    file.write(json.dumps(mismatch_report, indent=4))


with open(path + "mismatch_report.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=[
        "trade_id",
        "issue",
        "price_system1", "price_system2",
        "quantity_system1", "quantity_system2",
        "mode_system1", "mode_system2"
    ])
    writer.writeheader()

    for item in mismatch_report:
        tid = item["trade_id"]
        trade1 = trades1[tid]
        trade2 = trades2[tid]

        writer.writerow({
            "trade_id": tid,
            "issue": item.get("issue", "Mismatch"),
            "price_system1": trade1["price"],
            "price_system2": trade2["price"],
            "quantity_system1": trade1["quantity"],
            "quantity_system2": trade2["quantity"],
            "mode_system1": trade1["mode"],
            "mode_system2": trade2["mode"]
        })


parser = argparse.ArgumentParser(description="Trade Reconciliation Tool")

parser.add_argument("--summary-only", action="store_true", help="Show only total mismatches")
parser.add_argument("--json-output", action="store_true", help="Output file for mismatches")
parser.add_argument("--csv-output", action="store_true", help="Output file for mismatches")


args = parser.parse_args()



if args.summary_only:
    print(f"Total mismatches: {len(mismatch_report)}")
    sum = 0
    max = 0
    id = 0
    for item in mismatch_report:
        cnt = abs(trades1[item['trade_id']]['amount'] - trades2[item['trade_id']]['amount'])
        sum+= cnt
        if cnt > max:
            max = cnt
            id = item['trade_id']
        # print(cnt)
    print(f"Maximum absolute amount mismatch of one trade: {max}")
    print(f"Trade ID with maximum mismatch: {id}")
    print(f"Total maximum absolute amount mismatch: {sum}")
elif args.json_output:
    print("Full mismatch report:")
    for item in mismatch_report:
        print(json.dumps(trades1[item['trade_id']], indent=4))
        print(json.dumps(trades2[item['trade_id']], indent=4))
elif args.csv_output:
    print("Full mismatch report:")
    # for item in mismatch_report:
    print("trade_id,issue,price_system1,price_system2,quantity_system1,quantity_system2,mode_system1,mode_system2")
    for item in mismatch_report:
        tid = item["trade_id"]
        trade1 = trades1[tid]
        trade2 = trades2[tid]
        row = f'{tid},{item.get("issue", "Mismatch")},{trade1["price"]},{trade2["price"]},{trade1["quantity"]},{trade2["quantity"]},{trade1["mode"]},{trade2["mode"]}'
        print(row)

    #     print((trades1[item['trade_id']]))
    #     print((trades2[item['trade_id']]))
    #     print (csv)
else:
    print("specify Options(--summary-only or --json-output or --csv-output)") 

# with open('/home/konsol/Work Folder/Python/exercises/4/mismatch_report.json', 'r') as file:
#     mismatch_report = json.load(file)
#     print("Mismatch Report:")
#     for report in mismatch_report:
#         print(json.dumps(trades1[report['trade_id']], indent=4))
#         print(json.dumps(trades2[report['trade_id']], indent=4))
#         # print(trades2[report['trade_id']])