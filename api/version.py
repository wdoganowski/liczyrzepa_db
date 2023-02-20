from datetime import datetime

# datetime object containing current date and time
now = datetime.now()

# YY-mm-ddTH:M:S
dt_string = now.strftime('%Y-%m-%dT%H:%M:%S UTC')

version_string = '0.2.1'

LiczyrzepaAPIVersion = f'V{version_string} Started {dt_string}'