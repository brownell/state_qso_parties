#!/bin/bash
# Upload all log files to Fly.io

curl -s https://laqp.fly.dev/health > /dev/null
sleep 3 
flyctl ssh console << EOF
sleep 3
exit
EOF

echo "should be back at local prompt"
YEAR=$1
echo "year is $YEAR"
LOCAL_DIR="../laqp_data/batch_input/$YEAR"
REMOTE_DIR="/data/batch_input/$YEAR"
echo "local $LOCAL_DIR, remote $REMOTE_DIR"

echo "============================="
echo "📦 Creating archive... for year: $YEAR"
tar -czf temp/contest_logs.tar.gz -C $LOCAL_DIR .

echo "============================="
echo "📤 Uploading to Fly.io... for year $YEAR"
flyctl ssh sftp shell << EOF
put temp/contest_logs.tar.gz app/temp/contest_logs.tar.gz
ls  /app/temp
exit
EOF

echo "============================="
flyctl ssh console << EOF
echo "YEAR is $YEAR"
echo "📂 Extracting on Fly.io...$YEAR"
cd $REMOTE_DIR
ls $REMOTE_DIR
tar -xzf /app/temp/contest_logs.tar.gz
rm /app/temp/contest_logs.tar.gz
echo "✅ Extracted files:"
ls
exit
EOF

echo "🧹 Cleaning up local archive..."
rm temp/contest_logs.tar.gz

echo "✅ Upload complete!"