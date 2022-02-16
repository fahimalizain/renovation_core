#!/bin/bash

if [ ! -d "./apps" ] || [ ! -d "./sites" ]; then
    echo "ERROR: Please execute in bench-dir"
    exit 1
fi
BENCH_DIR=$(pwd)
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd $SCRIPT_DIR

echo " - Installing renovation_core"
pip install --quiet -e ./renovation_core
echo " - Installing school_app"
pip install --quiet -e ./school_app
echo " - Installing school_app_frappe"
pip install --quiet -e ./school_app_frappe

cd $BENCH_DIR

frappe_apps=( renovation_core school_app_frappe )
readarray -t installed_apps < ./sites/apps.txt
# echo "Initial Apps: ${installed_apps[*]}"

for app in "${frappe_apps[@]}"
do
    if [[ ! " ${installed_apps[*]} " =~ " ${app} " ]]; then
        # Array do not have value
        installed_apps+=($app)
    fi
done
# echo "Finall Apps: ${installed_apps[*]}"

echo -e " - Updated apps.txt"