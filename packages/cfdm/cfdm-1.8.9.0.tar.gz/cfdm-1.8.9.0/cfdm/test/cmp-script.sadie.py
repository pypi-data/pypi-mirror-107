import cfdm
from itertools import product


"""
0
[<DimensionCoordinate: latitude(5) degrees_north>,
<DimensionCoordinate: longitude(8) degrees_east>,
<DimensionCoordinate: time(1) days since 2018-12-01 >]

1
[<AuxiliaryCoordinate: latitude(10, 9) degrees_N>,
<AuxiliaryCoordinate: longitude(9, 10) degrees_E>,
<AuxiliaryCoordinate: long_name=Grid latitude name(10) >,
<DimensionCoordinate: atmosphere_hybrid_height_coordinate(1) >,
<DimensionCoordinate: grid_latitude(10) degrees>,
<DimensionCoordinate: grid_longitude(9) degrees>,
<DimensionCoordinate: time(1) days since 2018-12-01 >]

2
[<DimensionCoordinate: time(36) days since 1959-01-01 >,
<DimensionCoordinate: latitude(5) degrees_north>,
<DimensionCoordinate: longitude(8) degrees_east>,
<DimensionCoordinate: air_pressure(1) hPa>]

3
[<AuxiliaryCoordinate: time(4, 9) days since 1970-01-01 00:00:00 >,
<AuxiliaryCoordinate: latitude(4) degrees_north>,
<AuxiliaryCoordinate: longitude(4) degrees_east>,
<AuxiliaryCoordinate: height(4) m>,
<AuxiliaryCoordinate: cf_role=timeseries_id(4) >,
<AuxiliaryCoordinate: long_name=station information(4) >]

4
[<AuxiliaryCoordinate: time(3, 26) days since 1970-01-01 00:00:00 >,
<AuxiliaryCoordinate: latitude(3) degrees_north>,
<AuxiliaryCoordinate: longitude(3) degrees_east>,
<AuxiliaryCoordinate: height(3) m>,
<AuxiliaryCoordinate: altitude(3, 26, 4) km>,
<AuxiliaryCoordinate: cf_role=timeseries_id(3) >,
<AuxiliaryCoordinate: long_name=station information(3) >,
<AuxiliaryCoordinate: cf_role=profile_id(3, 26) >]

5
[<DimensionCoordinate: time(118) days since 1959-01-01 >,
<DimensionCoordinate: latitude(5) degrees_north>,
<DimensionCoordinate: longitude(8) degrees_east>,
<DimensionCoordinate: air_pressure(1) hPa>]

6
[<AuxiliaryCoordinate: latitude(2) degrees_north>,
<AuxiliaryCoordinate: longitude(2) degrees_east>,
<AuxiliaryCoordinate: cf_role=timeseries_id(2) >,
<AuxiliaryCoordinate: ncvar%z m>,
<DimensionCoordinate: time(4) days since 2000-01-01 >]

7
[<AuxiliaryCoordinate: latitude(4, 5) degrees_north>,
<AuxiliaryCoordinate: longitude(4, 5) degrees_east>,
<DimensionCoordinate: time(3) days since 1979-1-1 gregorian>,
<DimensionCoordinate: air_pressure(1) hPa>,
<DimensionCoordinate: grid_latitude(4) degrees>,
<DimensionCoordinate: grid_longitude(5) degrees>]

"""

# 0.
def get_coors(field):
    coors = []
    for coor in field.coordinates():
        coors.append(field.get_construct(coor))
    return coors


# 1.
def get_sets_coors(fields):
    set_of_coors = []
    for f in fields:
        set_of_coors.append(set(get_coors(f)))
    return set_of_coors

c = get_sets_coors(cfdm.example_fields())


# 2. ???
compare_coors = [(a, b) for (a, b) in product(c, c)]


# 3. Find the coors which are the same
def get_shared(coor_sets_to_compare):
    results = {}
    for index, coor_set in enumerate(coor_sets_to_compare):
        a, b = coor_set
        if a == b:
            results[index] = "all, same field"
        else:
            shared = [a.equals(b) for (a, b) in product(a, b)]
            # Serious weirdness is going on with the '-0' below...
            shared_indices = [
                (i % len(a)) + 0 for i, s in enumerate(shared) if s is True]
            if not shared_indices:
                shared_indices = None
            results[index] = shared_indices
    return results

sh1 = get_shared(compare_coors)

# 4. Get mapping indices applied by itertools.product to indicate fields cmp
sh2 = list(product(range(8), range(8)))


# 5. Combine the dicts to get example field pairs n=N and n=M as keys and the
# indices of any corresponding coordinates:
final = {}
for i, (key, value) in enumerate(sh1.items()):
    final[sh2[i]] = value

import pprint
pprint.pprint(final)

"""
RESULTS:

{(0, 0): 'all, same field',
 (0, 1): [2],
 (0, 2): [2, 2],
 (0, 3): None,
 (0, 4): None,
 (0, 5): [1, 1],
 (0, 6): None,
 (0, 7): None,
 (1, 0): [6],
 (1, 1): 'all, same field',
 (1, 2): None,
 (1, 3): None,
 (1, 4): None,
 (1, 5): None,
 (1, 6): None,
 (1, 7): None,
 (2, 0): [0, 2],
 (2, 1): None,
 (2, 2): 'all, same field',
 (2, 3): None,
 (2, 4): None,
 (2, 5): [3, 1, 2],
 (2, 6): None,
 (2, 7): None,
 (3, 0): None,
 (3, 1): None,
 (3, 2): None,
 (3, 3): 'all, same field',
 (3, 4): None,
 (3, 5): None,
 (3, 6): None,
 (3, 7): None,
 (4, 0): None,
 (4, 1): None,
 (4, 2): None,
 (4, 3): None,
 (4, 4): 'all, same field',
 (4, 5): None,
 (4, 6): None,
 (4, 7): None,
 (5, 0): [3, 2],
 (5, 1): None,
 (5, 2): [2, 3, 1],
 (5, 3): None,
 (5, 4): None,
 (5, 5): 'all, same field',
 (5, 6): None,
 (5, 7): None,
 (6, 0): None,
 (6, 1): None,
 (6, 2): None,
 (6, 3): None,
 (6, 4): None,
 (6, 5): None,
 (6, 6): 'all, same field',
 (6, 7): None,
 (7, 0): None,
 (7, 1): None,
 (7, 2): None,
 (7, 3): None,
 (7, 4): None,
 (7, 5): None,
 (7, 6): None,
 (7, 7): 'all, same field'}


=> fields with shared coors are:
* 0 and 1 (x1): <DimensionCoordinate: time(1) days since 2018-12-01 >
* 0 and 2 (x2):
    <DimensionCoordinate: latitude(5) degrees_north>,
    <DimensionCoordinate: longitude(8) degrees_east>,
* 0 and 5 (x2):
    <DimensionCoordinate: latitude(5) degrees_north>,
    <DimensionCoordinate: longitude(8) degrees_east>,
* 2 and 5 (x3):
<DimensionCoordinate: latitude(5) degrees_north>,
<DimensionCoordinate: longitude(8) degrees_east>,
<DimensionCoordinate: air_pressure(1) hPa>

=> set of shared coors in example fields is:

1. <DimensionCoordinate: time(1) days since 2018-12-01 > (fields 0 and 1)
2. <DimensionCoordinate: latitude(5) degrees_north> and
   <DimensionCoordinate: longitude(8) degrees_east> (fields 0, 2 and 5)
3. <DimensionCoordinate: air_pressure(1) hPa> (fields 2 and 5)
4. <AuxiliaryCoordinate: latitude(10, 9) degrees_N> and
   <AuxiliaryCoordinate: longitude(9, 10) degrees_E> and
   <DimensionCoordinate: atmosphere_hybrid_height_coordinate(1) > and
   <DimensionCoordinate: grid_latitude(10) degrees> and
   <DimensionCoordinate: grid_longitude(9) degrees> and finally
   <DimensionCoordinate: time(1) days since 2018-12-01 > (original field and 1)


and furthermore the original file, self.filename, has the 'g' field which
has the coors:

Constructs:
{'auxiliarycoordinate0': <AuxiliaryCoordinate: latitude(10, 9) degree_N>,
 'auxiliarycoordinate1': <AuxiliaryCoordinate: longitude(9, 10) degreeE>,
 'auxiliarycoordinate2': <AuxiliaryCoordinate: long_name=greek_letters(10) >,
 'dimensioncoordinate0': <DimensionCoordinate: atmosphere_hybrid_height_coordinate(1) >,
 'dimensioncoordinate1': <DimensionCoordinate: grid_latitude(10) degrees>,
 'dimensioncoordinate2': <DimensionCoordinate: grid_longitude(9) degrees>}

so shares 5 (of its 6) coors with example field 1.






"""
