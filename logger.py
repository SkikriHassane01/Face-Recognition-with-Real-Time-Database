import logging

# configure logging 

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
    ]
)

# create a logger object 
logger = logging.getLogger()