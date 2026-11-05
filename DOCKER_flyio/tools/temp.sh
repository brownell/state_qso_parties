curl -s https://txqp.fly.dev/health > /dev/null
sleep 3 
flyctl ssh console << EOF
sleep 2
exit
EOF

echo "AWAKE!"

echo "============================="
flyctl ssh console << EOF
echo "📦 DELETING some remote files: DB, final reports, temp files"
rm /data/final_reports/final_report_2026.html
rm /data/database/txqp.db
EOF
read -rsp $'DELETED some remote files.....Press any key to continue...\n' -n1

echo "============================="
echo "📤 Uploading to Fly.io... DB and some final reports"
flyctl ssh sftp put ../txqp_data/final_reports/final_report_2026.html /data/final_reports/final_report_2026.html
flyctl ssh sftp put ../txqp_data/database/txqp.db /data/database/txqp.db
read -rsp $'Uploaded files.....Press any key to continue...\n' -n1