import logging
from logging.handlers import TimedRotatingFileHandler
from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
from app import process_pdf_files
import os
from datetime import datetime

app = Flask(__name__)
scheduler = BackgroundScheduler(timezone="Asia/Kolkata")
scheduler.start()

# Configure logging
log_dir = r'C:\Users\tudip\OneDrive\Desktop\RegexPDF_DATA'
current_date = datetime.now().strftime("%Y-%m-%d")
log_file = os.path.join(log_dir, f'application_{current_date}.log')

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

handler = TimedRotatingFileHandler(log_file, when='midnight', interval=1, backupCount=30)
handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger.addHandler(handler)

# Function to trigger PDF processing
def trigger_pdf_processing():
    try:
        pdf_files = process_pdf_files()
        if len(pdf_files) > 0:
            logger.info("Data inserted successfully.")
        else:
            logger.info("All PDFs data are already extracted.")
    except Exception as e:
        logger.error(f"Error processing PDFs: {str(e)}")

job = scheduler.add_job(trigger_pdf_processing, 'interval', minutes=15)

# Run the Flask app
if __name__ == '__main__':
    trigger_pdf_processing()
    while True:
        try:
            app.run()
        except Exception as e:
            logger.error(f"Error running Flask app: {str(e)}")
