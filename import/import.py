import json, csv
from slugify import slugify

input_file = 'liczyrzepa.csv'
output_file = 'liczyrzepa_db.csv'
db_header = [
  'PK', 'SK', 
  'GSI1PK', 'GSI1SK', 'GSI2PK', 'GSI2SK', 'GSI3PK', 'GSI3SK', 
  'GSI4PK', 'GSI4SK', 'GSI5PK', 'GSI5SK', 'GSI6PK', 'GSI6SK', 
  'CountryName', 'RegionName', 'RangeName', 'MountainName', 
  'Elevation', 'GeoCoordinates', 'Latitude', 'Longitude', 'Attributes']

regions = {
  'fake_range': 'fake_region' 
}

def country_row(country: str):
  slug_country = slugify(country)
  return [
    f'CNTRY#{slug_country}', f'CNTRY#{slug_country}', 
    'CNTRY', f'CNTRY#{slug_country}', '', '', '', '', 
    '', '', '', '', '', '', 
    country
  ]

def region_row(country: str, region: str):
  slug_country = slugify(country)
  slug_region = slugify(region)
  return [
    f'REGIO#{slug_region}', f'REGIO#{slug_region}', 
    f'CNTRY#{slug_country}', f'REGIO#{slug_region}', '', '', '', '', 
    '', '', '', '', '', '', 
    '', region
  ]

def range_row(country: str, region: str, range: str):
  slug_country = slugify(country)
  slug_region = slugify(region)
  slug_range = slugify(range)
  return [
    f'RANGE#{slug_range}', f'RANGE#{slug_range}',
    f'CNTRY#{slug_country}', f'RANGE#{slug_range}', f'REGIO#{slug_region}', f'RANGE#{slug_range}', '', '',
    '', '', '', '', '', '',
    '', '', range
  ]

def mountain_row(country: str, region: str, range: str, mountain: str, elevation: int, geo: str, lat: str, long: str, attributes: dict):
  slug_country = slugify(country)
  slug_region = slugify(region)
  slug_range = slugify(range)
  slug_mountain = slugify(mountain)
  slug_elevation = str(f'{elevation:05d}')
  return [
    f'MOUNT#{slug_mountain}', f'MOUNT#{slug_mountain}', 
    f'CNTRY#{slug_country}', f'MOUNT#{slug_mountain}', f'REGIO#{slug_region}', f'MOUNT#{slug_mountain}', f'RANGE#{slug_range}', f'MOUNT#{slug_mountain}',
    f'CNTRY#{slug_country}', f'MTELV#{slug_elevation}', f'REGIO#{slug_region}', f'MTELV#{slug_elevation}', f'RANGE#{slug_range}', f'MTELV#{slug_elevation}',
    '', '', '', mountain, elevation, geo, lat, long, attributes
  ]

def bool_or_none(value: str):
  return bool(value) if value!='' else None

with open(input_file) as csv_input_file:
  with open(output_file, 'w') as csv_output_file:
    csv_reader = csv.reader(csv_input_file, delimiter=',')
    csv_writer = csv.writer(csv_output_file, delimiter=',')
    line_count = 0
    
    country = 'Polska'
    for row in csv_reader:
      if line_count == 0:
        print(db_header)
        csv_writer.writerow(db_header)
        line_count += 1
        # Add country row for Poland
        csv_writer.writerow(country_row(country))
      else:
        print(f'{row} -> ')
        # Row for region, range and mountain
        # MountainName,Elevation,RangeName,RegionName,GeoCoordinates,Latitude,Longitude,KGP,Diadem,KGS,KS,KNSSP,TZK,KBW,KMSL,DogFriendly
        region = row[3]
        range = row[2]
        mountain = row[0]
        
        # Regions not specified, try to find it in the past records
        if region == '': 
          try:
            region = regions[range]
          except KeyError:
            pass
        regions[region] = range

        csv_writer.writerow(region_row(country, region))
        csv_writer.writerow(range_row(country, region, range))
        csv_writer.writerow(mountain_row(
            country, region, range, mountain, int(row[1]), row[4], row[5], row[6], 
            {
              'kgp': bool_or_none(row[7]),    # Korona Gór Polskich
              'dpg': bool_or_none(row[8]),    # Diadem Polskich Gór
              'kgs': bool_or_none(row[9]),    # Korona Gór Stołowych
              'ks': bool_or_none(row[10]),    # Korona Sudetów
              'knssp': bool_or_none(row[11]), # Korona Najwybitniejszych Szczytów Sudetów Polskich
              'tzk': bool_or_none(row[12]),   # Tysięczniki Ziemi Kłodzkiej
              'kbw': bool_or_none(row[13]),   # Korona Beskidu Wyspowego
              'kmsl': bool_or_none(row[14]),  # Korona Masywu Ślęży
              'dogFriendly': bool_or_none(row[15])
            }
          ))
        line_count += 1

    print(f'Processed {line_count} lines.')