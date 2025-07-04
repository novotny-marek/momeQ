from qgis.core import QgsProcessingProvider

from .shape import (
    FacadeRatio,
    FractalDimension,
    SquareCompactness,
    FormFactor,
    CircularCompactness,
    Convexity,
    Rectangularity,
    Corners,
    ShapeIndex,
    CourtyardIndex,
    Squareness,
    Linearity,
    Elongation,
    EquivalentRectangularIndex,
)
from .dimension import (
    CourtyardArea,
    LongestAxisLength,
    StreetProfile,
)
from .elements import (
    BufferedLimit,
    MorphologicalTessellation,
)


class MomepyProvider(QgsProcessingProvider):
    """The"""

    def id(self) -> str:
        """The id of the plugin used for identifying the provider."""
        return "momeq"

    def name(self) -> str:
        """Human friendly name of the plugin in Processing."""
        return self.tr("momeQ")

    def getAlgorithms(self):
        algorithms = [
            FacadeRatio(),
            FractalDimension(),
            SquareCompactness(),
            FormFactor(),
            CircularCompactness(),
            Convexity(),
            Rectangularity(),
            Corners(),
            ShapeIndex(),
            CourtyardIndex(),
            CourtyardArea(),
            LongestAxisLength(),
            StreetProfile(),
            Squareness(),
            Linearity(),
            Elongation(),
            EquivalentRectangularIndex(),
            BufferedLimit(),
            MorphologicalTessellation(),
        ]
        return algorithms

    def loadAlgorithms(self):
        """Load each algorithm into current provider."""
        self.algs = self.getAlgorithms()
        for a in self.algs:
            self.addAlgorithm(a)
