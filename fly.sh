fly ssh console
rm /data/txqp*
rm /app/static/pdfs/final_report_2026.pdf

fly ssh sftp put ../tqp_data/database/tqp.db /data/txqp.db
fly ssh sftp put static/pdfs/final_report_2026.pdf /app/static/pdfs/final_report_2026.pdf