from dataclasses import dataclass
import sys
import math
from typing import List

sys.setrecursionlimit(10**6)

@dataclass(frozen=True)
class GlobeRect:
    lo_lat: float
    hi_lat: float
    west_long: float
    east_long: float

@dataclass(frozen=True)
class Region:
    rect: GlobeRect
    name: str
    terrain: str # oceans, mountains, forest, other

@dataclass(frozen=True)
class RegionCondition:
    region: Region 
    year: int
    pop: int
    ghg_rate: float 

# --- Example Data ---
sf_rect = GlobeRect(37.70, 37.81, -122.52, -122.35)
SF = Region(sf_rect, "San Francisco", "other")
sf_condition = RegionCondition(SF, 2024, 827500, 4120000.0)

london_rect = GlobeRect(51.28, 51.70, -0.51, 0.33)
London = Region(london_rect, "London", "other")
london_condition = RegionCondition(London, 2024, 8900000, 29000000.0)

caribbean_rect = GlobeRect(9.0, 22.0, -89.0, -60.0)
Caribbean_Sea = Region(caribbean_rect, "Caribbean Sea", "ocean")
cs_condition = RegionCondition(Caribbean_Sea, 2024, 0, 0.0)

cal_poly_rect = GlobeRect(34.9, 36.0, -121.5, -120.2)
Central_Coast = Region(cal_poly_rect, "Central Coast CA", "other")
coast_condition = RegionCondition(Central_Coast, 2024, 280000, 1400000.0)

region_conditions = [sf_condition, london_condition, cs_condition, coast_condition]


def emissions_per_capita(rc: RegionCondition) -> float:
    # Type: RegionCondition -> float
    "Purpose: Calculate the GHG emissions per person in a RegionCondition."
    return rc.ghg_rate / rc.pop if rc.pop > 0 else 0.0


def area(rect: GlobeRect) -> float:
    # Type: GlobeRect -> float
    "Purpose: Calculate the surface area of a GlobeRect in km² using a spherical Earth model."
    R = 6378.1
    lat_diff = abs(math.sin(math.radians(rect.hi_lat)) - math.sin(math.radians(rect.lo_lat)))
    long_diff = math.radians((rect.east_long - rect.west_long) % 360)
    return R**2 * lat_diff * long_diff

def emissions_per_square_km(rc: RegionCondition) -> float:
    # Type: RegionCondition -> float
    "Purpose: Calculate the GHG emissions per square kilometer for a given RegionCondition."
    rect_area = area(rc.region.rect)
    return rc.ghg_rate / rect_area if rect_area > 0 else 0.0

def densest_rc(rc_list: List[RegionCondition]) -> RegionCondition:
    # Type: List[RegionCondition] -> RegionCondition
    "Purpose: Recursively find the RegionCondition with the highest population density."
    if len(rc_list) == 1:
        return rc_list[0]
    rest = densest_rc(rc_list[1:])
    current_area = area(rc_list[0].region.rect)
    rest_area = area(rest.region.rect)
    current_density = rc_list[0].pop / current_area if current_area > 0 else 0.0
    rest_density = rest.pop / rest_area if rest_area > 0 else 0.0
    if current_density >= rest_density:
        return rc_list[0]
    else:
        return rest

def densest(rc_list: List[RegionCondition]) -> str:
    # Type: List[RegionCondition] -> str
    "Purpose: Return the name of the region with the highest population density."
    return densest_rc(rc_list).region.name

def growth_rate(terrain: str) -> float:
    # Type: str -> float
    "Purpose: Return the annual growth rate associated with a specific terrain type."
    rates = {
        "ocean": 0.0001,
        "mountains": 0.0005,
        "forest": -0.00001,
        "other": 0.0003
    }
    return rates[terrain]

def project_condition(rc: RegionCondition, years: int) -> RegionCondition:
    # Type: RegionCondition, int -> RegionCondition
    "Purpose: Project a RegionCondition's population and emissions over a given number of years."
    rate = growth_rate(rc.region.terrain)
    new_pop = rc.pop * (1 + rate) ** years
    new_ghg = rc.ghg_rate * (new_pop / rc.pop) if rc.pop != 0 else rc.ghg_rate
    return RegionCondition(rc.region, rc.year + years, int(new_pop), new_ghg)