#!/bin/bash
echo "Running reconciliation..."

#!/bin/bash
SCRIPT_PATH="$(readlink -f "$0")"

PROJECT_DIR="$(dirname "$SCRIPT_PATH")"

path=$PROJECT_DIR

File=$(date +%Y-%m-%d)

# echo $File
echo $path 2>&1 | tee $path'/Logs/2025-06-16.txt'



logFile=(${path}'/Logs/'${File}'.txt')
FILE1json=($path'/system1/system1_trades_'${File}'.json')
FILE1csv=($path'/system1/system1_trades_'${File}'.csv')
touch $path'/reconcile_trades.py' $path'/mismatch_report.json'
if [ ! -f "$FILE1json" ]; then
    if [ ! -f "$FILE1csv" ]; then
        touch "$FILE1json"
        echo "Input File 1 Created. Ensure writing content to it. And then re-run the execution." 2>&1 | tee "$path/Logs/${File}.txt"
        echo "{}" 2>&1 | tee $FILE1json
    fi
fi

FILE2json=($path'/system2/system2_trades_'${File}'.json')
FILE2csv=($path'/system2/system2_trades_'${File}'.csv')
if [ ! -f "$FILE2json" ]; then
    if [ ! -f "$FILE2csv" ]; then
        touch "$FILE2json"
        echo "Input File 2 Created. Ensure writing content to it. And then re-run the execution." 2>&1 | tee "$path/Logs/${File}.txt"
        echo "{}" 2>&1 | tee $FILE2json
    fi
fi


(python3 -u "$path/reconcile_trades.py" "$@") 2>&1 | tee "$path/Logs/${File}.txt"


cron_line="0 7 * * * $SCRIPT_PATH --summary-only"
(crontab -l 2>/dev/null | grep -Fv "$cron_line"; echo "$cron_line") | crontab -