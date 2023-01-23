# API Access Methods

1. GET /country                         Returns countries
2. GET /country/{country}               Returns country
3. GET /country/{country}/regions       Returns regions of country
4. GET /region/{region}                 Returns region
5. GET /region/{region}/ranges          Returns mointain ranges of region
6. GET /range/{range}                   Returns mountain range
7. GET /range/{range}/shelters          Returns shelters in the range
8. GET /shelter/{shelter}               Returns shelter
9. GET /shelter/{shelter}/picures       Returns shelter pictures
10. GET /shelter/{shelter}/opinions     Returns shelter opinions
11. GET /shelters_by_elevation/{min}/{max}?country={country} or region={region} or range={range}
                                        Returns shelters between min and max elevation with optional filters for country, region and range (widest filter is applied only)
12. GET /range/{range}/mountains        Returns mountains in the range
13. GET /mountain/{mountain}            Returns mountain
14. GET /mountain/{mountain}/picures    Returns mountain pictures
15. GET /mountain/{mountain}/opinions   Returns mountain opinions
16. GET /mountains_by_elevation/{min}/{max}?country={country} or region={region} or range={range}
                                        Returns mountains between min and max elevation with optional filters for country, region and range (widest filter is applied only)

# Entity chart

| Entity     | PK                    | SK                 | Covered methods |
|------------|-----------------------|--------------------|-----------------|
| country    | CNTRY#{country}       | CNTRY#{country}    | 2               |
| region     | CNTRY#{country}       | REGIO#{region}     | 3, 4            |
| range      | REGIO#{region}        | RANGE#{range}      | 5, 6            |
| shelter    | RANGE{range}          | SHLTR#{shelter}    | 7, 8            |
| s_picture  | SHLTR#{shelter}       | PICTR#{picture}    | 9               |
| s_opinion  | SHLTR#{shelter}       | OPINN#{picture}    | 10              |
| mountain   | RANGE#{range}         | MOUNT#{mountain}   | 12, 13          |
| m_picture  | MOUNT#{mountain}      | PICTR#{picture}    | 14              |
| m_opinion  | MOUNT#{mountain}      | OPINN#{picture}    | 15              |

| Entity     | GSI1PK                | GSI1SK             | Covered methods |
|------------|-----------------------|--------------------|-----------------|
| country    | CNTRY                 | CNTRY#{country}    | 1               |
| shelter    | CNTRY#{country}       | SHLTR#{elevation}  | 11              |
| mountain   | CNTRY#{country}       | MOUNT#{elevation}  | 16              |

| Entity     | GSI2PK                | GSI2SK             | Covered methods |
|------------|-----------------------|--------------------|-----------------|
| shelter    | REGIO#{region}        | SHLTR#{elevation}  | 11              |
| mountain   | REGIO#{region}        | MOUNT#{elevation}  | 16              |

| Entity     | GSI3PK                | GSI3SK             | Covered methods |
|------------|-----------------------|--------------------|-----------------|
| shelter    | RANGE#{range}         | SHLTR#{elevation}  | 11              |
| mountain   | RANGE#{range}         | MOUNT#{elevation}  | 16              |

The id are constracted by *slugifying* the names