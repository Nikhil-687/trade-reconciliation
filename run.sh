#!/bin/bash
echo "Running reconciliation..."

SCRIPT_PATH="$(readlink -f "$0")"

PROJECT_DIR="$(dirname "$SCRIPT_PATH")"

path=$PROJECT_DIR

File=$(date +%Y-%m-%d)

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

options=$1



if [[ "$options" = "--time" || "$options" = "-t" ]]; 
then
    echo  "To define the time you can provide concrete values for"
    echo  "minute (m), hour (h), day of month (dom), month (mon),"
    echo  "and day of week (day) or use '*' in these fields (for 'any')."
    echo  
    echo  "Notice that tasks will be started based on the cron's system"
    echo  
    echo  "For example, you can run a backup of all your user accounts"
    echo  "at 5 a.m every week with:"
    echo  "updateTime 0 5 * * 1"
    echo  
    echo  "enter time as following formate"
    echo  ""
    echo "m h  dom mon day: "
    read -rp "" time
fi



cron_line="$time $SCRIPT_PATH --summary-only"
(crontab -l 2>/dev/null | grep -Fv "$SCRIPT_PATH"; echo "$cron_line") | crontab -



(python3 -u "$path/reconcile_trades.py" "$2") 2>&1 | tee "$path/Logs/${File}.txt"
