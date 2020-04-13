from django.contrib.gis.db import models
from pangea import settings

# Create your models here.

from django.core.files.storage import FileSystemStorage

fs = FileSystemStorage(location=settings.MEDIA_ROOT)


# class ImportedData(models.Model):
#     file_path = models.FileField(storage=fs)
#     table_name = models.CharField(max_length=200)
#     encoding = models.CharField(max_length=50, default='utf8')   
#     description = models.TextField(null=True, blank=True)
#     metadata_url = models.URLField(null=True, blank=True)
    
#     def __str__(self):
#         return self.table_name



# class ImportedGeographicData(ImportedData):
#     srid = models.IntegerField(null=True, blank=True)


# class ImportedTabularData(ImportedData):
#     compose_a_new_layer = models.BooleanField(default=True)
#     delimiter = models.CharField(max_length=1, default=',')
#     quotechar = models.CharField(max_length=1, null=True, blank=True)
#     decimal = models.CharField(max_length=1, default='.')









# class LayerMetadata(models.Model):
#     layer_name = models.CharField(max_length=200)
#     data_imported = models.ForeignKey(ImportedData, on_delete=models.CASCADE)
#     schema_name =  models.CharField(max_length=200)
#     table_name =  models.CharField(max_length=200)
#     geocod_column =  models.CharField(max_length=200)
#     dimension_column =  models.CharField(max_length=200)
#     topo_geom_column =  models.CharField(max_length=200)

#     is_a_composition_of = models.ForeignKey('self', on_delete=models.CASCADE)
#     composition_column = models.CharField(max_length=200)
#     zoom_min = models.ForeignKey(GeneralizationParams, on_delete=models.CASCADE, related_name='zoom_min')
#     zoom_max = models.ForeignKey(GeneralizationParams, on_delete=models.CASCADE, related_name='zoom_max')

class GeneralizationParams(models.Model):
    zoom_level = models.IntegerField(primary_key=True)
    factor = models.FloatField()


class Layer(models.Model):
    name = models.CharField(max_length=200, unique=True)    
    description = models.TextField(null=True, blank=True)
    metadata = models.URLField(null=True, blank=True)

    _file = models.FileField(storage=fs)
    schema_name = models.CharField(max_length=200, null=True, blank=True)
    table_name = models.CharField(max_length=200, null=True, blank=True)

    encoding = models.CharField(max_length=50, default='utf8', null=True, blank=True)   

    zoom_min = models.ForeignKey(GeneralizationParams, on_delete=models.CASCADE, related_name='zoom_min', null=True, blank=True)
    zoom_max = models.ForeignKey(GeneralizationParams, on_delete=models.CASCADE, related_name='zoom_max', null=True, blank=True)


class LayerStatus(models.Model):
    class Status(models.IntegerChoices):
        IMPORTED = 0
        TOPOLOGY_CREATED = 1
        LAYER_CREATED_WITHOUT_TOPOLOGY = 2
        LAYER_CREATED_WITH_TOPOLOGY = 3
        LAYER_PUBLISHED_WITHOUT_TOPOLOGY = 4
        LAYER_PUBLISHED_WITH_TOPOLOGY = 5
    layer = models.ForeignKey(Layer, on_delete=models.CASCADE)
    status = models.IntegerField(choices=Status.choices, default=0)
    date = models.DateTimeField(auto_now=True)


class TerritorialLevelLayer(Layer):
    geocod_column =  models.CharField(max_length=200, null=True, blank=True)


class BasicTerritorialLevelLayer(TerritorialLevelLayer):   
    srid = models.IntegerField()   
    dimension_column =  models.CharField(max_length=200, null=True, blank=True)
    geom_column =  models.CharField(max_length=200, null=True, blank=True)
    geom_type = models.CharField(max_length=200, null=True, blank=True)
    topology_name = models.CharField(max_length=200, null=True, blank=True)
    topology_layer_id = models.IntegerField(null=True, blank=True)
    topo_geom_column_name = models.CharField(max_length=200, null=True, blank=True)    

class Column(models.Model):
    layer = models.ForeignKey(Layer, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    alias = models.CharField(max_length=200)


'''
class ComposedTerritorialLevelLayer(TerritorialLevelLayer):
    is_a_composition_of = models.ForeignKey(TerritorialLevelLayer, on_delete=models.CASCADE)

    delimiter = models.CharField(max_length=1, default=',')
    quotechar = models.CharField(max_length=1, null=True, blank=True)
    decimal = models.CharField(max_length=1, default='.')

    composition_column = models.CharField(max_length=200)


class CartographicLayer(BasicTerritorialLevelLayer):
    pass


class ChoroplethLayer(Layer):
    delimiter = models.CharField(max_length=1, default=',')
    quotechar = models.CharField(max_length=1, null=True, blank=True)
    decimal = models.CharField(max_length=1, default='.')
'''