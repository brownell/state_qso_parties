#!/bin/bash

# Upload result files (db, final_reports) to Fly.io

curl -s https://txqp.fly.dev/health > /dev/null
sleep 3 
flyctl ssh console << EOF
sleep 2
exit
EOF


echo "AWAKE!"

echo "============================="
echo "📦 DELETING remote files: DB, final report"
flyctl ssh console << EOF
rm -f /app/static/pdfs/final_report_2026.pdf
rm -rf /data/*
EOF
echo "DELETED remote files

echo "============================="
echo "📦 SENDING remote files: DB, final report"
flyctl ssh sftp shell << EOF
put static/pdfs/final_report_2026.pdf /app/static/pdfs/final_report_2026.pdf
cd /app/static/pdfs
ls

fly ssh sftp put ../tqp_data/database/tqp.db /data/txqp.db
cd /app/static/pdfs
ls
EOF

# echo "============================="
# echo "📦 DELETING all remote files: DB, final reports, temp files"
# flyctl ssh console << EOF
# rm -f /app/static/pdfs/final_report_2026.pdf
# rm -rf /data/*
# rm -rf /app/temp/*
# exit
# EOF
# read -rsp $'DELETED all remote files.....Press any key to continue...\n' -n1

# echo "============================="
# echo "📦 SEND  final report"
# read -rsp $'Created reports tar.....Press any key to continue...\n' -n1

# echo "============================="
# echo "📤 Uploading to Fly.io... for final reports"
# flyctl ssh sftp shell << EOF
# put temp/final_reports.tar.gz /app/temp/final_reports.tar.gz
# cd /app/temp
# ls
# EOF
# read -rsp $'Uploaded reports tar.....Press any key to continue...\n' -n1

# echo "============================="
# echo "Extracting reports tar"
# flyctl ssh console << EOF
# echo "📂 Extracting on Fly.io... final reports"
# cd /data/final_reports
# ls
# tar -xzf /app/temp/final_reports.tar.gz
# rm /app/temp/final_reports.tar.gz
# echo "✅ Extracted files:"
# ls
# exit
# EOF
# read -rsp $'Extracted reports tar on fly.io.....Press any key to continue...\n' -n1

# echo "============================="
# echo "📤 Uploading to Fly.io... for db"
# flyctl ssh sftp shell << EOF
# put ../txqp_data/database/tqp.db /data/txqp.db
# cd /app/temp
# EOF
# read -rsp $'Uploaded DB ....Press any key to continue...\n' -n1

# echo "============================="
# echo "🧹 Cleaning up local archive..."
# rm temp/final_reports.tar.gz
# echo "✅ Upload complete! **********"
