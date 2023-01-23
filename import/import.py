import json, csv
from slugify import slugify

input_file = 'liczyrzepa.csv'
output_file = 'liczyrzepa_db.csv'
db_header = [
  'PK', 'SK', 'GSI1PK', 'GSI1SK', 'GSI2PK', 'GSI2SK', 'GSI3PK', 'GSI3SK', 'CountryName', 'RegionName', 'RangeName', 'MountainName', 'Elevation', 'GeoCoordinates', 'Latitude', 'Longitude', 'Attributes']

def country_row(country: str):
  slug_country = slugify(country)
  return [f'CNTRY#{slug_country}', f'CNTRY#{slug_country}', 'CNTRY', f'CNTRY#{slug_country}', '', '', '', '', country]

def region_row(country: str, region: str):
  slug_country = slugify(country)
  slug_region = slugify(region)
  return [f'CNTRY#{slug_country}', f'REGIO#{slug_region}', '', '', '', '', '', '', country, region]

def range_row(country: str, region: str, range: str):
  slug_country = slugify(country)
  slug_region = slugify(region)
  slug_range = slugify(range)
  return [f'REGIO#{slug_region}', f'RANGE#{slug_range}', '', '', '', '', '', '', country, region, range]

def mountain_row(country: str, region: str, range: str, mountain: str, elevation: int, geo: str, lat: str, long: str, attributes: dict):
  slug_country = slugify(country)
  slug_region = slugify(region)
  slug_range = slugify(range)
  slug_mountain = slugify(mountain)
  slug_elevation = str(f'{elevation:05d}')
  return [
    f'RANGE#{slug_range}', f'MOUNT#{slug_mountain}', f'CNTRY#{slug_country}', f'MOUNT#{slug_elevation}', f'REGIO#{slug_region}', f'MOUNT#{slug_elevation}', f'RANGE#{slug_range}', f'MOUNT#{slug_elevation}', 
    country, region, range, mountain, elevation, geo, lat, long, attributes]

def bool_or_none(value: str):
  return bool(value) if value!='' else None

with open(input_file) as csv_input_file:
  with open(output_file, 'w') as csv_output_file:
    csv_reader = csv.reader(csv_input_file, delimiter=',')
    csv_writer = csv.writer(csv_output_file, delimiter=',')
    line_count = 0
    
    for row in csv_reader:
      if line_count == 0:
        print(db_header)
        csv_writer.writerow(db_header)
        line_count += 1
        # Add country row for Poland
        csv_writer.writerow(country_row('Polska'))
      else:
        print(f'{row} -> ')
        # Row for region, range and mountain
        # MountainName,Elevation,RangeName,RegionName,GeoCoordinates,Latitude,Longitude,KGP,Diadem,KGS,KS,KNSSP,TZK,KBW,KMSL,DogFriendly
        csv_writer.writerow(region_row('Polska', row[3]))
        csv_writer.writerow(range_row('Polska', row[3], row[2]))
        csv_writer.writerow(mountain_row(
            'Polska', row[3], row[2], row[0], int(row[1]), row[4], row[5], row[6], 
            {
              'KGP': bool_or_none(row[7]),
              'Diadem': bool_or_none(row[8]),
              'KGS': bool_or_none(row[9]),
              'KS': bool_or_none(row[10]),
              'KNSSP': bool_or_none(row[11]),
              'TZK': bool_or_none(row[12]),
              'KBW': bool_or_none(row[13]),
              'KMSL': bool_or_none(row[14]),
              'DogFriendly': bool_or_none(row[15])
            }
          ))
        line_count += 1

    print(f'Processed {line_count} lines.')