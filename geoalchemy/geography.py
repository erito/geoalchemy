import warnings

from sqlalchemy import Column, Table, exc
from sqlalchemy.orm import column_property
from sqlalchemy.orm.interfaces import AttributeExtension
from sqlalchemy.sql.expression import Alias
from sqlalchemy.sql import expression
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.dialects.postgresql.base import PGDialect

from geoalchemy.base import GeographyBase, _to_gis, SpatialComparator
from geoalchemy.dialect import DialectManager
from geoalchemy.functions import functions

class Geography(GeographyBase):
    """Geography column type.  Identical to Geography column type,
    but exists for syntatic convenience, as well as to specify a difference
    when creating Columns using DDL.  

    Geography fields aren't considered geometry, so it is necessary to
    use the types withinclass within in this module to specify the geography 
    type.

    """

#Doing this for consistency only, PostGIS is only one supported anyway.
    def result_processor(self, dialect, coltype=None):
        def process(value):
            if value is not None:
                return DialectManager.get_spatial_dialect(dialect).process_result(value, self)
            else:
                return value
        return process

class Point(Geography):
    name = 'POINT'
    
class Curve(Geography):
    name = 'CURVE'
    
class LineString(Curve):
    name = 'LINESTRING'

class Polygon(Geography):
    name = 'POLYGON'

class MultiPoint(Geography):
    name = 'MULTIPOINT'

class MultiLineString(Geography):
    name = 'MULTILINESTRING'

class MultiPolygon(Geography):
    name = 'MULTIPOLYGON'

class GeographyCollection(Geography):
    name = 'GEOMETRYCOLLECTION'
