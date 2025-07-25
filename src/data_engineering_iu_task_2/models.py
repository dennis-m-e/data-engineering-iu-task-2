from pydantic import BaseModel, Field


class AirQualityPollutionData(BaseModel):
    """Model for air quality data."""

    timestamp: float | None = Field(
        default=None, description="Timestamp of the data point in seconds since epoch"
    )
    temperature: float = Field(
        ..., description="Average temperature of the region in degrees Celsius"
    )
    humidity: float = Field(
        ..., description="Relative humidity recorded in the region in percentage"
    )
    pm_2_5: float = Field(
        ..., description="Fine particulate matter levels in micrograms per cubic meter"
    )
    pm_10: float = Field(
        ...,
        description="Coarse particulate matter levels in micrograms per cubic meter",
    )
    no_2: float = Field(..., description="Nitrogen dioxide levels in parts per billion")
    so_2: float = Field(..., description="Sulfur dioxide levels in parts per billion")
    co: float = Field(..., description="Carbon monoxide levels in parts per billion")
    proximity_to_industrial_areas: float = Field(
        ..., description="Distance to the nearest industrial zone"
    )
    population_density: int = Field(
        ...,
        description="Number of people per square kilometer in the region in people per square kilometer",
    )
    air_quality: str = Field(
        ..., description="Air quality index category (e.g., Good, Moderate, Poor)"
    )
