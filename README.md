# 🧾 Trade Reconciliation Tool

A daily automated trade reconciliation utility that logs every run and maintains historical records.
A CLI-based automated trade reconciliation utility built with Bash and Python. It compares two systems' trade records daily, stores detailed logs, and can be scheduled via `cron`.



## 🚀 Features

- Automatically creates input placeholders if missing
- Executes `reconcile_trades.py` with logging
- Appends timestamped logs to `Logs/YYYY-MM-DD.txt`
- Supports `--time` (`-t`) flag to schedule cron execution
- Fully cron-compatible (no interactive prompts during automated runs)

## 🔧 Setup

[📦 Download TradeReconciler.zip](https://raw.githubusercontent.com/Nikhil-687/trade-reconciliation/main/TradeReconciler.zip)

```bash
sudo dpkg -i traderecon_1.0.deb
```

## OR

```bash
git clone https://github.com/Nikhil-687/trade-reconciliation
cd trade-reconciliation
```


## RUN

navigate to the project and do 

```bash
chmod +x ./run.sh
./run.sh [OPTIONS] [--time/-t/' ']
```
[OPTION] : "--summary-only", "--json-output", "--csv-output"
--time/-t => set crontab timings
' ' => default timing 7 am 


## output 
trade-reconciliation/Logs/YYYY-MM-DD.txt

## input 
'trade-reconciliation/system1/system1_trades_' + YYYY-MM-DD + '.csv/.json'
'trade-reconciliation/system2/system2_trades_' + YYYY-MM-DD + '.csv/.json'