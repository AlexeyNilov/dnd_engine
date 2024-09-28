from pydantic import Field
from pydantic.types import StringConstraints
from typing_extensions import Annotated


GEZeroInt = Annotated[int, Field(ge=0)]
ConstrainedStr = Annotated[
    str, StringConstraints(min_length=1, to_lower=True, strip_whitespace=True)
]
