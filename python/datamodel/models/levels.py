

from enum import IntEnum
from typing import Union, List
from ..io.loaders import read_yaml, get_yaml_files
from .base import CoreModel, BaseList
from pydantic import model_validator, Field, RootModel, model_serializer


class Variant(CoreModel):
    x: int
    y: int
    name: str
    level: int
    description: str

class Variants(BaseList, RootModel[List[Variant]]):
    """ Pydantic model representing a list of Variants """
    pass

# construct the SDSS variant
variants = Variants.model_validate(read_yaml(get_yaml_files('variants'))['variants'])


class X(IntEnum):
    """ Product Type """
    raw = 0
    intermediate = 1
    final = 2
    vac = 3


class Y(IntEnum):
    """ Product Subtype"""
    image = 1
    spectra = 2
    catalog = 3
    datacube = 4
    targeting = 5


class Z(IntEnum):
    none = 0


level_descriptions = {
    X.raw.name: "Raw product, before any data processing",
    X.intermediate.name: "Intermediate or ancillary pipeline product output during data processing",
    X.final.name: "Final science data product from a reduction or analysis pipeline",
    X.vac.name: "A data product produced from a value-added catalog",
    Y.image.name: "A 2d image data product, or set of images",
    Y.spectra.name: "A 1d or 2d spectral data product, or a set of spectral data",
    Y.catalog.name: "A catalog or table of derived parameters and metadata",
    Y.datacube.name: "A 3d IFU data cube of 2 spatial and 1 spectral dimensions",
    Y.targeting.name: "A targeting file different from a standard catalog",
    Z.none.name: "No product variant",
}


# Dynamically create Z enum and update level descriptions
Z_values = {}
for variant in variants:
    key = f"{variant.x}.{variant.y}"
    if key not in Z_values:
        Z_values[key] = {}
    Z_values[key][variant.level] = variant.name
    level_descriptions[f"{variant.x}.{variant.y}.{variant.level}"] = variant.description



class DataLevel(CoreModel):
    x: X = Field(..., description='product type; high level category of pipeline product')
    y: Y = Field(..., description='product subtype; type of data product')
    z: Union[Z, int, None] = Field(Z.none, description='product variant; fine-grained flexible label of specific information', union_model='left_to_right')

    def __str__(self):
        return f"{self.x.value}.{self.y.value}" + (f".{self.z}" if self.z is not None else "")

    @model_validator(mode='before')
    def parse_string(cls, values):
        """ Deserialize from a string """
        if isinstance(values, str):
            parts = values.split('.')
            values = {
                'x': int(parts[0]),
                'y': int(parts[1]),
                'z': int(parts[2]) if len(parts) > 2 else Z.none
            }
        return values

    @model_serializer()
    def serialize_model(self) -> str:
        """ Serialize the object as a string """
        return f"{self.x.value}.{self.y.value}.{self.z}"

    def describe(self):
        """ Provide a description of the data level """

        key = f"{self.x.value}.{self.y.value}"
        if isinstance(self.z, IntEnum):
            z_name = self.z.name
            z_desc = level_descriptions[self.z.name]
        elif self.z == 0:
            z_name = "none"
            z_desc = "No product variant"
        elif key in Z_values:
            z_name = Z_values[key].get(self.z, "unknown")
            z_desc = level_descriptions.get(f"{key}.{self.z}", "unknown variant level")

        return {"product_type": f"{self.x.name}: {level_descriptions[self.x.name]}",
                "product_subtype": f"{self.y.name}: {level_descriptions[self.y.name]}",
                "product_variant": f"{z_name}: {z_desc}"
                }
