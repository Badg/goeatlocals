import dataclasses

import trio


_data_path = trio.Path(__file__).parent / 'data'
_template_path = _data_path / 'map_style_template.json'
FONTS_STATIC_PATH = _data_path / 'fonts'


@dataclasses.dataclass
class Mapstyle:
    noshow_color: str
    font_family: str
    background_color: str
    ice_color: str
    glacier_color: str
    pier_color: str
    bridge_footprint_color: str
    grass_color: str
    woods_color: str
    water_color: str
    sand_color: str
    national_park_color: str
    pathway_color: str
    road_major_color: str
    road_trunk_color: str
    road_secondary_color: str
    road_minor_color: str
    railway_color: str
    aeroway_color: str
    administrative_border_color: str
    building_color: str
    building_border_color_zoomin: str
    building_border_color_zoomout: str
    label_color: str
    label_halo_color: str

    async def render(self):
        template = await _template_path.read_text()

        for field_name, value in dataclasses.asdict(self).items():
            sub_text = f'__{field_name}__'
            template = template.replace(sub_text, value)

        return template


# TODO: get colors from a colors enum somewhere that's our single source of
# truth on colors
eatlocals_light = Mapstyle(
    noshow_color='hsla(31, 100%, 90%, 1)',
    font_family='Roboto Regular',

    background_color='hsla(31, 100%, 90%, 1)',
    ice_color='hsla(31, 100%, 97%, 1)',
    glacier_color='hsla(31, 100%, 97%, 1)',
    pier_color='hsla(31, 100%, 90%, 1)',
    bridge_footprint_color='hsla(31, 100%, 90%, 1)',
    grass_color='hsla(128, 61%, 53%, 1)',
    woods_color='hsla(128, 61%, 53%, 1)',
    water_color='hsla(194, 61%, 53%, 1)',
    sand_color='hsla(13, 100%, 26%, 1)',
    national_park_color='hsla(128, 61%, 53%, 1)',
    pathway_color='hsla(31, 100%, 82%, 1)',
    road_major_color='hsla(31, 100%, 97%, 1)',
    road_trunk_color='hsla(31, 100%, 97%, 1)',
    road_secondary_color='hsla(31, 100%, 97%, 0.8)',
    road_minor_color='hsla(31, 100%, 97%, 0.8)',
    railway_color='hsla(31, 100%, 82%, 1)',
    aeroway_color='hsla(31, 100%, 82%, 1)',
    administrative_border_color='hsla(31, 60%, 25%, 1)',
    building_color='hsla(31, 100%, 82%, 1)',
    building_border_color_zoomin='hsla(31, 60%, 25%, 0.5)',
    building_border_color_zoomout='hsla(31, 60%, 25%, 0)',
    label_color='hsla(31, 58%, 9%, 1)',
    label_halo_color='hsla(31, 100%, 97%, 1)',
)


MAPSTYLES = {
    'eatlocals_light': eatlocals_light
}
