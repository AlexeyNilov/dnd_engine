from pydantic import Field
from typing_extensions import Annotated


GEZeroInt = Annotated[int, Field(ge=0)]
