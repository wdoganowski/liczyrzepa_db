# API Access Methods

| #   | Method                              | Description                                       |
|-----|-------------------------------------|---------------------------------------------------|
| 1.  | GET /country                        | Returns countries 
| 2.  | GET /country/{country}              | Returns country
| 3.  | GET /country/{country}/regions      | Returns regions of country
| 4.  | GET /region/{region}                | Returns region
| 5.  | GET /region/{region}/ranges         | Returns mointain ranges of region
| 6.  | GET /range/{range}                  | Returns mountain range
| 7.  | GET /range/{range}/shelters         | Returns shelters in the range
| 8.  | GET /shelter/{shelter}              | Returns shelter
| 9.  | GET /shelter/{shelter}/picures      | Returns shelter pictures
| 10. | GET /shelter/{shelter}/opinions     | Returns shelter opinions
| 11. | GET /shelter/bby_elevationby_elevation/{min}/{max}?country={country} or region={region} or range={range}                                     |  Returns shelters between min and max elevation with optional filters for country, region and range (widest filter is applied only)
| 12. | GET /range/{range}/mounts           | Returns mountains in the range
| 13. | GET /mount/{mountain}               | Returns mountain
| 14. | GET /mount/{mountain}/picures       | Returns mountain pictures
| 15. | GET /mount/{mountain}/opinions      | Returns mountain opinions
| 16. | GET /mount/by_elevation/{min}/{max}?country={country} or region={region} or range={range}                                     | Returns mountains between min and max elevation with optional filters for country, region and range (widest filter is applied only)

# Entity chart

| Entity     | PK                    | SK                 | Covered methods |
|------------|-----------------------|--------------------|-----------------|
| country    | CNTRY#{country}       | CNTRY#{country}    | 2               |
| region     | REGIO#{region}        | REGIO#{region}     | 3               |
| range      | RANGE#{range}         | RANGE#{range}      | 5               |
| shelter    | SHLTR{range}          | SHLTR#{shelter}    | 7               |
| s_picture  | SHLTR#{shelter}       | PICTR#{picture}    | 9               |
| s_opinion  | SHLTR#{shelter}       | OPINN#{picture}    | 10              |
| mountain   | MOUNT#{mountain}      | MOUNT#{mountain}   | 12              |
| m_picture  | MOUNT#{mountain}      | PICTR#{picture}    | 14              |
| m_opinion  | MOUNT#{mountain}      | OPINN#{picture}    | 15              |
|------------|-----------------------|--------------------|-----------------|
| Entity     | GSI1PK                | GSI1SK             | Covered methods |
|------------|-----------------------|--------------------|-----------------|
| country    | CNTRY                 | CNTRY#{country}    | 1               |
| region     | CNTRY#{country}       | REGIO#{elevation}  | 4               |
| range      | CNTRY#{country}       | RANGE#{range}      | 6               |
| shelter    | CNTRY#{country}       | SHLTR#{shelter}    | 8              |
| mountain   | CNTRY#{country}       | MOUNT#{mountain}   | 13              |
|------------|-----------------------|--------------------|-----------------|
| Entity     | GSI2PK                | GSI2SK             | Covered methods |
|------------|-----------------------|--------------------|-----------------|
| range      | REGIO#{region}        | RANGE#{range}      |                 |
| shelter    | REGIO#{region}        | SHLTR#{shelter}    |                 |
| mountain   | REGIO#{region}        | MOUNT#{mountain}   |                 |
|------------|-----------------------|--------------------|-----------------|
| Entity     | GSI3PK                | GSI3SK             | Covered methods |
|------------|-----------------------|--------------------|-----------------|
| shelter    | RANGE#{region}        | SHLTR#{shelter}    |                 |
| mountain   | RANGE#{region}        | MOUNT#{mountain}   |                 |
|------------|-----------------------|--------------------|-----------------|
| Entity     | GSI4PK                | GSI4SK             | Covered methods |
|------------|-----------------------|--------------------|-----------------|
| shelter    | CNTRY#{country}       | SHELV#{elevation}  | 11              |
| mountain   | CNTRY#{country}       | MTELV#{elevation}  | 16              |
|------------|-----------------------|--------------------|-----------------|
| Entity     | GSI5PK                | GSI5SK             | Covered methods |
|------------|-----------------------|--------------------|-----------------|
| shelter    | REGIO#{region}        | SHELV#{elevation}  | 11              |
| mountain   | REGIO#{region}        | MTELV#{elevation}  | 16              |
|------------|-----------------------|--------------------|-----------------|
| Entity     | GSI6PK                | GSI6SK             | Covered methods |
|------------|-----------------------|--------------------|-----------------|
| shelter    | RANGE#{range}         | SHELV#{elevation}  | 11              |
| mountain   | RANGE#{range}         | MTELV#{elevation}  | 16              |


The id are constracted by *slugifying* the names

# Debugging 

[Debug information is here](Debug.md)