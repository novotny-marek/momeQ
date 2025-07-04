import momepy

from .utils import qgs_to_gpd
from PyQt5.QtCore import QVariant
from qgis.core import (
    QgsField,
    QgsFeature,
    QgsProcessing,
    QgsFeatureSink,
    QgsProcessingAlgorithm,
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterFeatureSink,
    QgsProcessingParameterField,
    QgsProcessingParameterNumber,
    QgsProcessingParameterBoolean,
)


class FormFactor(QgsProcessingAlgorithm):
    INPUT = "INPUT"
    OUTPUT = "OUTPUT"
    HEIGHT_FIELD = "HEIGHT_FIELD"

    def name(self) -> str:
        return "form_factor"

    def displayName(self) -> str:
        return "Form factor"

    def group(self) -> str:
        return "Shape"

    def groupId(self) -> str:
        return "shape"

    def shortHelpString(self) -> str:
        return "Calculates the form factor of each object given its geometry and height"

    def initAlgorithm(self, configuration=None):
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT,
                "Input layer",
                [QgsProcessing.SourceType.VectorPolygon],
            )
        )

        self.addParameter(
            QgsProcessingParameterField(
                self.HEIGHT_FIELD,
                "Height field",
                parentLayerParameterName=self.INPUT,
                type=QgsProcessingParameterField.Numeric,
            )
        )

        self.addParameter(QgsProcessingParameterFeatureSink(self.OUTPUT, "Form factor"))

    def processAlgorithm(self, parameters, context, feedback):
        source = self.parameterAsSource(parameters, self.INPUT, context)
        height_field = self.parameterAsString(parameters, self.HEIGHT_FIELD, context)

        # Convert QGIS feature to GeoDataFrame and calculate form factor
        geometry_dataframe = qgs_to_gpd(source, attribute_fields=[height_field])
        height = geometry_dataframe[height_field]
        form_factor_series = momepy.form_factor(geometry_dataframe, height)
        form_factor_values = form_factor_series.to_list()

        # Create output fields (original fields + new form factor field)
        fields = source.fields()
        fields.append(QgsField("form_factor", QVariant.Double))

        # Create sink
        (sink, dest_id) = self.parameterAsSink(
            parameters,
            self.OUTPUT,
            context,
            fields,
            source.wkbType(),
            source.sourceCrs(),
        )

        # Get features from source
        features = source.getFeatures()
        total = 100.0 / source.featureCount() if source.featureCount() else 0

        # Process each feature directly
        for current, feature in enumerate(features):
            if feedback.isCanceled():
                break

            # Create output feature
            output_feature = QgsFeature(fields)
            output_feature.setGeometry(feature.geometry())

            # Copy attributes and add new form factor
            attributes = feature.attributes()
            attributes.append(form_factor_values[current])
            output_feature.setAttributes(attributes)

            # Add feature to sink
            sink.addFeature(output_feature, QgsFeatureSink.Flag.FastInsert)

            # Update progress
            feedback.setProgress(int(current * total))

        return {self.OUTPUT: dest_id}

    def createInstance(self):
        return self.__class__()


class FractalDimension(QgsProcessingAlgorithm):
    INPUT = "INPUT"
    OUTPUT = "OUTPUT"

    def name(self) -> str:
        return "fractal_dimension"

    def displayName(self) -> str:
        return "Fractal dimension"

    def group(self) -> str:
        return "Shape"

    def groupId(self) -> str:
        return "shape"

    def shortHelpString(self) -> str:
        return "Calculates fractal dimension based on area and perimeter"

    def initAlgorithm(self, configuration=None):
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT,
                "Input layer",
                [QgsProcessing.SourceType.VectorPolygon],
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSink(self.OUTPUT, "Fractal dimension")
        )

    def processAlgorithm(self, parameters, context, feedback):
        source = self.parameterAsSource(parameters, self.INPUT, context)

        # Convert QGIS source to GeoSeries and calculate fractal dimension
        geometry_series = qgs_to_gpd(source)
        fractal_dimension_series = momepy.fractal_dimension(geometry_series)
        fractal_dimension_values = fractal_dimension_series.to_list()

        # Create output fields (original fields + new ratio field)
        fields = source.fields()
        fields.append(QgsField("fractal_dimension", QVariant.Double))

        # Create sink
        (sink, dest_id) = self.parameterAsSink(
            parameters,
            self.OUTPUT,
            context,
            fields,
            source.wkbType(),
            source.sourceCrs(),
        )

        # Get features from source
        features = source.getFeatures()
        total = 100.0 / source.featureCount() if source.featureCount() else 0

        # Process each feature directly
        for current, feature in enumerate(features):
            if feedback.isCanceled():
                break

            # Create output feature
            output_feature = QgsFeature(fields)
            output_feature.setGeometry(feature.geometry())

            # Copy attributes and add new ratio
            attributes = feature.attributes()
            attributes.append(fractal_dimension_values[current])
            output_feature.setAttributes(attributes)

            # Add feature to sink
            sink.addFeature(output_feature, QgsFeatureSink.Flag.FastInsert)

            # Update progress
            feedback.setProgress(int(current * total))

        return {self.OUTPUT: dest_id}

    def createInstance(self):
        return self.__class__()


class FacadeRatio(QgsProcessingAlgorithm):
    INPUT = "INPUT"
    OUTPUT = "OUTPUT"

    def name(self) -> str:
        return "facade_ratio"

    def displayName(self) -> str:
        return "Facade ratio"

    def group(self) -> str:
        return "Shape"

    def groupId(self) -> str:
        return "shape"

    def shortHelpString(self) -> str:
        return "Calculates the facade ratio of each object given its geometry"

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT,
                "Input layer",
                [QgsProcessing.SourceType.VectorPolygon],
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSink(self.OUTPUT, "Facade ratio")
        )

    def processAlgorithm(self, parameters, context, feedback):
        source = self.parameterAsSource(parameters, self.INPUT, context)

        # Convert QGIS source to GeoSeries and calculate facade ratio
        geometry_series = qgs_to_gpd(source)
        facade_ratio_series = momepy.facade_ratio(geometry_series)
        facade_ratio_values = facade_ratio_series.to_list()

        # Create output fields (original fields + new ratio field)
        fields = source.fields()
        fields.append(QgsField("facade_ratio", QVariant.Double))

        # Create sink
        (sink, dest_id) = self.parameterAsSink(
            parameters,
            self.OUTPUT,
            context,
            fields,
            source.wkbType(),
            source.sourceCrs(),
        )

        # Get features from source
        features = source.getFeatures()
        total = 100.0 / source.featureCount() if source.featureCount() else 0

        # Process each feature directly
        for current, feature in enumerate(features):
            if feedback.isCanceled():
                break

            # Create output feature
            output_feature = QgsFeature(fields)
            output_feature.setGeometry(feature.geometry())

            # Copy attributes and add new ratio
            attributes = feature.attributes()
            attributes.append(facade_ratio_values[current])
            output_feature.setAttributes(attributes)

            # Add feature to sink
            sink.addFeature(output_feature, QgsFeatureSink.Flag.FastInsert)

            # Update progress
            feedback.setProgress(int(current * total))

        return {self.OUTPUT: dest_id}

    def createInstance(self):
        return self.__class__()


class CircularCompactness(QgsProcessingAlgorithm):
    INPUT = "INPUT"
    OUTPUT = "OUTPUT"

    def name(self) -> str:
        return "circular_compactness"

    def displayName(self) -> str:
        return "Circular compactness"

    def group(self) -> str:
        return "Shape"

    def groupId(self) -> str:
        return "shape"

    def shortHelpString(self) -> str:
        return "Calculates the circular compactness of each object given its geometry"

    def initAlgorithm(self, configuration=None):
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT,
                "Input layer",
                [QgsProcessing.SourceType.VectorPolygon],
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSink(self.OUTPUT, "Circular compactness")
        )

    def processAlgorithm(self, parameters, context, feedback):
        source = self.parameterAsSource(parameters, self.INPUT, context)

        # Convert QGIS feature to GeoSeries and calculate circular compactness
        geometry_series = qgs_to_gpd(source)
        circular_compactness_series = momepy.circular_compactness(geometry_series)
        circular_compactness_values = circular_compactness_series.to_list()

        # Create output fields (original fields + new circular compactness field)
        fields = source.fields()
        fields.append(QgsField("circular_compactness", QVariant.Double))

        # Create sink
        (sink, dest_id) = self.parameterAsSink(
            parameters,
            self.OUTPUT,
            context,
            fields,
            source.wkbType(),
            source.sourceCrs(),
        )

        # Get features from source
        features = source.getFeatures()
        total = 100.0 / source.featureCount() if source.featureCount() else 0

        # Process each feature directly
        for current, feature in enumerate(features):
            if feedback.isCanceled():
                break

            # Create output feature
            output_feature = QgsFeature(fields)
            output_feature.setGeometry(feature.geometry())

            # Copy attributes and add new circular compactness
            attributes = feature.attributes()
            attributes.append(circular_compactness_values[current])
            output_feature.setAttributes(attributes)

            # Add feature to sink
            sink.addFeature(output_feature, QgsFeatureSink.Flag.FastInsert)

            # Update progress
            feedback.setProgress(int(current * total))

        return {self.OUTPUT: dest_id}

    def createInstance(self):
        return self.__class__()


class SquareCompactness(QgsProcessingAlgorithm):
    INPUT = "INPUT"
    OUTPUT = "OUTPUT"

    def name(self) -> str:
        return "square_compactness"

    def displayName(self) -> str:
        return "Square compactness"

    def group(self) -> str:
        return "Shape"

    def groupId(self) -> str:
        return "shape"

    def shortHelpString(self) -> str:
        return "Calculates the square compactness of each object given its geometry"

    def initAlgorithm(self, configuration=None):
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT,
                "Input layer",
                [QgsProcessing.SourceType.VectorPolygon],
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSink(self.OUTPUT, "Square compactness")
        )

    def processAlgorithm(self, parameters, context, feedback):
        source = self.parameterAsSource(parameters, self.INPUT, context)

        # Convert QGIS source to GeoSeries and calculate square compactness
        geometry_series = qgs_to_gpd(source)
        square_compactness_series = momepy.square_compactness(geometry_series)
        square_compactness_values = square_compactness_series.to_list()

        # Create output fields (original fields + new ratio field)
        fields = source.fields()
        fields.append(QgsField("square_compactness", QVariant.Double))

        # Create sink
        (sink, dest_id) = self.parameterAsSink(
            parameters,
            self.OUTPUT,
            context,
            fields,
            source.wkbType(),
            source.sourceCrs(),
        )

        # Get features from source
        features = source.getFeatures()
        total = 100.0 / source.featureCount() if source.featureCount() else 0

        # Process each feature directly
        for current, feature in enumerate(features):
            if feedback.isCanceled():
                break

            # Create output feature
            output_feature = QgsFeature(fields)
            output_feature.setGeometry(feature.geometry())

            # Copy attributes and add new ratio
            attributes = feature.attributes()
            attributes.append(square_compactness_values[current])
            output_feature.setAttributes(attributes)

            # Add feature to sink
            sink.addFeature(output_feature, QgsFeatureSink.Flag.FastInsert)

            # Update progress
            feedback.setProgress(int(current * total))

        return {self.OUTPUT: dest_id}

    def createInstance(self):
        return self.__class__()


class Convexity(QgsProcessingAlgorithm):
    INPUT = "INPUT"
    OUTPUT = "OUTPUT"

    def name(self) -> str:
        return "convexity"

    def displayName(self) -> str:
        return "Convexity"

    def group(self) -> str:
        return "Shape"

    def groupId(self) -> str:
        return "shape"

    def shortHelpString(self) -> str:
        return "Calculates the convexity of each object given its geometry"

    def initAlgorithm(self, configuration=None):
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT,
                "Input Layer",
                [QgsProcessing.SourceType.VectorPolygon],
            )
        )

        self.addParameter(QgsProcessingParameterFeatureSink(self.OUTPUT, "Convexity"))

    def processAlgorithm(self, parameters, context, feedback):
        source = self.parameterAsSource(parameters, self.INPUT, context)

        # Convert QGIS feature to GeoSeries and calculate convexity
        geometry_series = qgs_to_gpd(source)
        convexity_series = momepy.convexity(geometry_series)
        convexity_values = convexity_series.to_list()

        fields = source.fields()
        fields.append(QgsField("convexity", QVariant.Double))

        # Create sink
        (sink, dest_id) = self.parameterAsSink(
            parameters,
            self.OUTPUT,
            context,
            fields,
            source.wkbType(),
            source.sourceCrs(),
        )

        # Get features from source
        features = source.getFeatures()
        total = 100.0 / source.featureCount() if source.featureCount() else 0

        # Process each feature directly
        for current, feature in enumerate(features):
            if feedback.isCanceled():
                break

            # Create output feature
            output_feature = QgsFeature(fields)
            output_feature.setGeometry(feature.geometry())

            # Copy attributes and add new convexity
            attributes = feature.attributes()
            attributes.append(convexity_values[current])
            output_feature.setAttributes(attributes)

            # Add feature to sink
            sink.addFeature(output_feature, QgsFeatureSink.Flag.FastInsert)

            # Update progress
            feedback.setProgress(int(current * total))

        return {self.OUTPUT: dest_id}

    def createInstance(self):
        return self.__class__()


class CourtyardIndex(QgsProcessingAlgorithm):
    INPUT = "INPUT"
    OUTPUT = "OUTPUT"
    COURTYARD_AREA_FIELD = "COURTYARD_AREA_FIELD"

    def name(self) -> str:
        return "courtyard_index"

    def displayName(self) -> str:
        return "Courtyard index"

    def group(self) -> str:
        return "Shape"

    def groupId(self) -> str:
        return "shape"

    def shortHelpString(self) -> str:
        return "Calculates the courtyard index of each object given its geometry."

    def initAlgorithm(self, configuration=None):
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT,
                "Input layer",
                [QgsProcessing.SourceType.VectorPolygon],
            )
        )

        self.addParameter(
            QgsProcessingParameterField(
                self.COURTYARD_AREA_FIELD,
                "Courtyard area field",
                parentLayerParameterName=self.INPUT,
                type=QgsProcessingParameterField.Numeric,
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSink(self.OUTPUT, "Courtyard index")
        )

    def processAlgorithm(self, parameters, context, feedback):
        source = self.parameterAsSource(parameters, self.INPUT, context)
        courtyard_area_field = self.parameterAsString(
            parameters, self.COURTYARD_AREA_FIELD, context
        )

        # Convert QGIS feature to GeoDataFrame and calculate courtyard index
        geometry_dataframe = qgs_to_gpd(source, attribute_fields=[courtyard_area_field])
        courtyard_area = geometry_dataframe[courtyard_area_field]
        courtyard_index_series = momepy.courtyard_index(
            geometry_dataframe, courtyard_area=courtyard_area
        )
        courtyard_index_values = courtyard_index_series.to_list()

        # Create output fields (original fields + new courtyard index field)
        fields = source.fields()
        fields.append(QgsField("courtyard_index", QVariant.Double))

        # Create sink
        (sink, dest_id) = self.parameterAsSink(
            parameters,
            self.OUTPUT,
            context,
            fields,
            source.wkbType(),
            source.sourceCrs(),
        )

        # Get features from source
        features = source.getFeatures()
        total = 100.0 / source.featureCount() if source.featureCount() else 0

        # Process each feature directly
        for current, feature in enumerate(features):
            if feedback.isCanceled():
                break

            # Create output feature
            output_feature = QgsFeature(fields)
            output_feature.setGeometry(feature.geometry())

            # Copy attributes and add new courtyard index
            attributes = feature.attributes()
            attributes.append(courtyard_index_values[current])
            output_feature.setAttributes(attributes)

            # Add feature to sink
            sink.addFeature(output_feature, QgsFeatureSink.Flag.FastInsert)

            # Update progress
            feedback.setProgress(int(current * total))

        return {self.OUTPUT: dest_id}

    def createInstance(self):
        return self.__class__()


class Rectangularity(QgsProcessingAlgorithm):
    INPUT = "INPUT"
    OUTPUT = "OUTPUT"

    def name(self) -> str:
        return "rectangularity"

    def displayName(self) -> str:
        return "Rectangularity"

    def group(self) -> str:
        return "Shape"

    def groupId(self) -> str:
        return "shape"

    def shortHelpString(self) -> str:
        return "Calculates the rectangularity of each object given its geometry"

    def initAlgorithm(self, configuration=None):
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT,
                "Input Layer",
                [QgsProcessing.SourceType.VectorPolygon],
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSink(self.OUTPUT, "Rectangularity")
        )

    def processAlgorithm(self, parameters, context, feedback):
        source = self.parameterAsSource(parameters, self.INPUT, context)

        # Convert QGIS feature to GeoSeries and calculate rectangularity
        geometry_series = qgs_to_gpd(source)
        rectangularity_series = momepy.rectangularity(geometry_series)
        rectangularity_values = rectangularity_series.to_list()

        fields = source.fields()
        fields.append(QgsField("rectangularity", QVariant.Double))

        # Create sink
        (sink, dest_id) = self.parameterAsSink(
            parameters,
            self.OUTPUT,
            context,
            fields,
            source.wkbType(),
            source.sourceCrs(),
        )

        # Get features from source
        features = source.getFeatures()
        total = 100.0 / source.featureCount() if source.featureCount() else 0

        # Process each feature directly
        for current, feature in enumerate(features):
            if feedback.isCanceled():
                break

            # Create output feature
            output_feature = QgsFeature(fields)
            output_feature.setGeometry(feature.geometry())

            # Copy attributes and add new rectangularity
            attributes = feature.attributes()
            attributes.append(rectangularity_values[current])
            output_feature.setAttributes(attributes)

            # Add feature to sink
            sink.addFeature(output_feature, QgsFeatureSink.Flag.FastInsert)

            # Update progress
            feedback.setProgress(int(current * total))

        return {self.OUTPUT: dest_id}

    def createInstance(self):
        return self.__class__()


class ShapeIndex(QgsProcessingAlgorithm):
    INPUT = "INPUT"
    OUTPUT = "OUTPUT"
    LONGEST_AXIS_FIELD = "LONGEST_AXIS_FIELD"

    def name(self) -> str:
        return "shape_index"

    def displayName(self) -> str:
        return "Shape index"

    def group(self) -> str:
        return "Shape"

    def groupId(self) -> str:
        return "shape"

    def shortHelpString(self) -> str:
        return "Calculates the shape index of each object given its geometry."

    def initAlgorithm(self, configuration=None):
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT,
                "Input layer",
                [QgsProcessing.SourceType.VectorPolygon],
            )
        )

        self.addParameter(
            QgsProcessingParameterField(
                self.LONGEST_AXIS_FIELD,
                "Longest axis length field",
                parentLayerParameterName=self.INPUT,
                type=QgsProcessingParameterField.Numeric,
            )
        )

        self.addParameter(QgsProcessingParameterFeatureSink(self.OUTPUT, "Shape index"))

    def processAlgorithm(self, parameters, context, feedback):
        source = self.parameterAsSource(parameters, self.INPUT, context)
        longest_axis_field = self.parameterAsString(
            parameters, self.LONGEST_AXIS_FIELD, context
        )

        # Convert QGIS feature to GeoDataFrame and calculate shape index
        geometry_dataframe = qgs_to_gpd(source, attribute_fields=[longest_axis_field])
        longest_axis = geometry_dataframe[longest_axis_field]
        shape_index_series = momepy.shape_index(
            geometry_dataframe, longest_axis_length=longest_axis
        )
        shape_index_values = shape_index_series.to_list()

        # Create output fields (original fields + new shape index field)
        fields = source.fields()
        fields.append(QgsField("shape_index", QVariant.Double))

        # Create sink
        (sink, dest_id) = self.parameterAsSink(
            parameters,
            self.OUTPUT,
            context,
            fields,
            source.wkbType(),
            source.sourceCrs(),
        )

        # Get features from source
        features = source.getFeatures()
        total = 100.0 / source.featureCount() if source.featureCount() else 0

        # Process each feature directly
        for current, feature in enumerate(features):
            if feedback.isCanceled():
                break

            # Create output feature
            output_feature = QgsFeature(fields)
            output_feature.setGeometry(feature.geometry())

            # Copy attributes and add new shape index
            attributes = feature.attributes()
            attributes.append(shape_index_values[current])
            output_feature.setAttributes(attributes)

            # Add feature to sink
            sink.addFeature(output_feature, QgsFeatureSink.Flag.FastInsert)

            # Update progress
            feedback.setProgress(int(current * total))

        return {self.OUTPUT: dest_id}

    def createInstance(self):
        return self.__class__()


class Corners(QgsProcessingAlgorithm):
    INPUT = "INPUT"
    OUTPUT = "OUTPUT"
    EPS_FIELD = "EPS_FIELD"
    INTERIORS_FIELD = "INTERIORS_FIELD"

    def name(self) -> str:
        return "corners"

    def displayName(self) -> str:
        return "Corners"

    def group(self) -> str:
        return "Shape"

    def groupId(self) -> str:
        return "shape"

    def shortHelpString(self) -> str:
        return "Calculates the number of corners of each object given its geometry"

    def initAlgorithm(self, configuration=None):
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT,
                "Input Layer",
                [QgsProcessing.SourceType.VectorPolygon],
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.EPS_FIELD,
                "Deviation from 180 degrees to consider a corner, by default 10",
                type=QgsProcessingParameterNumber.Double,
                defaultValue=10.0,
                optional=True,
            )
        )

        self.addParameter(
            QgsProcessingParameterBoolean(
                self.INTERIORS_FIELD,
                "Include polygon interiors, by default False",
                defaultValue=False,
                optional=True,
            )
        )

        self.addParameter(QgsProcessingParameterFeatureSink(self.OUTPUT, "Corners"))

    def processAlgorithm(self, parameters, context, feedback):
        source = self.parameterAsSource(parameters, self.INPUT, context)
        eps_field = self.parameterAsDouble(parameters, self.EPS_FIELD, context)
        interiors_field = self.parameterAsBool(
            parameters, self.INTERIORS_FIELD, context
        )

        # Convert QGIS feature to GeoSeries and calculate number of corners
        geometry_series = qgs_to_gpd(source)
        corners_series = momepy.corners(
            geometry_series, eps=eps_field, include_interiors=interiors_field
        )
        corners_values = corners_series.to_list()

        fields = source.fields()
        fields.append(QgsField("corners", QVariant.Int))

        # Create sink
        (sink, dest_id) = self.parameterAsSink(
            parameters,
            self.OUTPUT,
            context,
            fields,
            source.wkbType(),
            source.sourceCrs(),
        )

        # Get features from source
        features = source.getFeatures()
        total = 100.0 / source.featureCount() if source.featureCount() else 0

        # Process each feature directly
        for current, feature in enumerate(features):
            if feedback.isCanceled():
                break

            # Create output feature
            output_feature = QgsFeature(fields)
            output_feature.setGeometry(feature.geometry())

            # Copy attributes and add new corners
            attributes = feature.attributes()
            attributes.append(corners_values[current])
            output_feature.setAttributes(attributes)

            # Add feature to sink
            sink.addFeature(output_feature, QgsFeatureSink.Flag.FastInsert)

            # Update progress
            feedback.setProgress(int(current * total))

        return {self.OUTPUT: dest_id}

    def createInstance(self):
        return self.__class__()


class Squareness(QgsProcessingAlgorithm):
    INPUT = "INPUT"
    OUTPUT = "OUTPUT"
    EPS_FIELD = "EPS_FIELD"
    INTERIORS_FIELD = "INTERIORS_FIELD"

    def name(self) -> str:
        return "squareness"

    def displayName(self) -> str:
        return "Squareness"

    def group(self) -> str:
        return "Shape"

    def groupId(self) -> str:
        return "shape"

    def shortHelpString(self) -> str:
        return "Calculates the squareness of each object given its geometry"

    def initAlgorithm(self, configuration=None):
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT,
                "Input Layer",
                [QgsProcessing.SourceType.VectorPolygon],
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.EPS_FIELD,
                "Deviation from 180 degrees to consider a corner, by default 10",
                type=QgsProcessingParameterNumber.Double,
                defaultValue=10.0,
                optional=True,
            )
        )

        self.addParameter(
            QgsProcessingParameterBoolean(
                self.INTERIORS_FIELD,
                "Include polygon interiors, by default False",
                defaultValue=False,
                optional=True,
            )
        )

        self.addParameter(QgsProcessingParameterFeatureSink(self.OUTPUT, "Squareness"))

    def processAlgorithm(self, parameters, context, feedback):
        source = self.parameterAsSource(parameters, self.INPUT, context)
        eps_field = self.parameterAsDouble(parameters, self.EPS_FIELD, context)
        interiors_field = self.parameterAsBool(
            parameters, self.INTERIORS_FIELD, context
        )

        # Convert QGIS feature to GeoSeries and calculate squareness
        geometry_series = qgs_to_gpd(source)
        squareness_series = momepy.squareness(
            geometry_series, eps=eps_field, include_interiors=interiors_field
        )
        squareness_values = squareness_series.to_list()

        fields = source.fields()
        fields.append(QgsField("squareness", QVariant.Double))

        # Create sink
        (sink, dest_id) = self.parameterAsSink(
            parameters,
            self.OUTPUT,
            context,
            fields,
            source.wkbType(),
            source.sourceCrs(),
        )

        # Get features from source
        features = source.getFeatures()
        total = 100.0 / source.featureCount() if source.featureCount() else 0

        # Process each feature directly
        for current, feature in enumerate(features):
            if feedback.isCanceled():
                break

            # Create output feature
            output_feature = QgsFeature(fields)
            output_feature.setGeometry(feature.geometry())

            # Copy attributes and add new squareness
            attributes = feature.attributes()
            attributes.append(squareness_values[current])
            output_feature.setAttributes(attributes)

            # Add feature to sink
            sink.addFeature(output_feature, QgsFeatureSink.Flag.FastInsert)

            # Update progress
            feedback.setProgress(int(current * total))

        return {self.OUTPUT: dest_id}

    def createInstance(self):
        return self.__class__()


class EquivalentRectangularIndex(QgsProcessingAlgorithm):
    INPUT = "INPUT"
    OUTPUT = "OUTPUT"

    def name(self) -> str:
        return "equivalent_rectangular_index"

    def displayName(self) -> str:
        return "Equivalent rectangular index"

    def group(self) -> str:
        return "Shape"

    def groupId(self) -> str:
        return "shape"

    def shortHelpString(self) -> str:
        return "Calculates the equivalent rectangular index of each object given its geometry"

    def initAlgorithm(self, configuration=None):
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT,
                "Input Layer",
                [QgsProcessing.SourceType.VectorPolygon],
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT, "Equivalent rectangular index"
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        source = self.parameterAsSource(parameters, self.INPUT, context)

        # Convert QGIS feature to GeoSeries and calculate equivalent rectangular index
        geometry_series = qgs_to_gpd(source)
        eri_series = momepy.equivalent_rectangular_index(geometry_series)
        eri_values = eri_series.to_list()

        fields = source.fields()
        fields.append(QgsField("eri", QVariant.Double))

        # Create sink
        (sink, dest_id) = self.parameterAsSink(
            parameters,
            self.OUTPUT,
            context,
            fields,
            source.wkbType(),
            source.sourceCrs(),
        )

        # Get features from source
        features = source.getFeatures()
        total = 100.0 / source.featureCount() if source.featureCount() else 0

        # Process each feature directly
        for current, feature in enumerate(features):
            if feedback.isCanceled():
                break

            # Create output feature
            output_feature = QgsFeature(fields)
            output_feature.setGeometry(feature.geometry())

            # Copy attributes and add new equivalent rectangular index
            attributes = feature.attributes()
            attributes.append(eri_values[current])
            output_feature.setAttributes(attributes)

            # Add feature to sink
            sink.addFeature(output_feature, QgsFeatureSink.Flag.FastInsert)

            # Update progress
            feedback.setProgress(int(current * total))

        return {self.OUTPUT: dest_id}

    def createInstance(self):
        return self.__class__()


class Elongation(QgsProcessingAlgorithm):
    INPUT = "INPUT"
    OUTPUT = "OUTPUT"

    def name(self) -> str:
        return "elongation"

    def displayName(self) -> str:
        return "Elongation"

    def group(self) -> str:
        return "Shape"

    def groupId(self) -> str:
        return "shape"

    def shortHelpString(self) -> str:
        return "Calculates the elongation of each object given its geometry"

    def initAlgorithm(self, configuration=None):
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT,
                "Input Layer",
                [QgsProcessing.SourceType.VectorPolygon],
            )
        )

        self.addParameter(QgsProcessingParameterFeatureSink(self.OUTPUT, "Elongation"))

    def processAlgorithm(self, parameters, context, feedback):
        source = self.parameterAsSource(parameters, self.INPUT, context)

        # Convert QGIS feature to GeoSeries and calculate elongation
        geometry_series = qgs_to_gpd(source)
        elongation_series = momepy.elongation(geometry_series)
        elongation_values = elongation_series.to_list()

        fields = source.fields()
        fields.append(QgsField("elongation", QVariant.Double))

        # Create sink
        (sink, dest_id) = self.parameterAsSink(
            parameters,
            self.OUTPUT,
            context,
            fields,
            source.wkbType(),
            source.sourceCrs(),
        )

        # Get features from source
        features = source.getFeatures()
        total = 100.0 / source.featureCount() if source.featureCount() else 0

        # Process each feature directly
        for current, feature in enumerate(features):
            if feedback.isCanceled():
                break

            # Create output feature
            output_feature = QgsFeature(fields)
            output_feature.setGeometry(feature.geometry())

            # Copy attributes and add new elongation
            attributes = feature.attributes()
            attributes.append(elongation_values[current])
            output_feature.setAttributes(attributes)

            # Add feature to sink
            sink.addFeature(output_feature, QgsFeatureSink.Flag.FastInsert)

            # Update progress
            feedback.setProgress(int(current * total))

        return {self.OUTPUT: dest_id}

    def createInstance(self):
        return self.__class__()


class CentroidCornerDistance(QgsProcessingAlgorithm):
    INPUT = "INPUT"
    OUTPUT = "OUTPUT"
    EPS_FIELD = "EPS_FIELD"
    INTERIORS_FIELD = "INTERIORS_FIELD"

    def name(self) -> str:
        return "centroid_corner_distance"

    def displayName(self) -> str:
        return "Centroid corner distance"

    def group(self) -> str:
        return "Shape"

    def groupId(self) -> str:
        return "shape"

    def shortHelpString(self) -> str:
        return (
            "Calculates the centroid corner distance of each object given its geometry"
        )

    def initAlgorithm(self, configuration=None):
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT,
                "Input Layer",
                [QgsProcessing.SourceType.VectorPolygon],
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.EPS_FIELD,
                "Deviation from 180 degrees to consider a corner, by default 10",
                type=QgsProcessingParameterNumber.Double,
                defaultValue=10.0,
                optional=True,
            )
        )

        self.addParameter(
            QgsProcessingParameterBoolean(
                self.INTERIORS_FIELD,
                "Include polygon interiors, by default False",
                defaultValue=False,
                optional=True,
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSink(self.OUTPUT, "Centroid corner distance")
        )

    def processAlgorithm(self, parameters, context, feedback):
        source = self.parameterAsSource(parameters, self.INPUT, context)
        eps_field = self.parameterAsDouble(parameters, self.EPS_FIELD, context)
        interiors_field = self.parameterAsBool(
            parameters, self.INTERIORS_FIELD, context
        )

        # Convert QGIS feature to GeoSeries and calculate centroid corner distance
        geometry_series = qgs_to_gpd(source)
        ccd_series = momepy.centroid_corner_distance(
            geometry_series, eps=eps_field, include_interiors=interiors_field
        )
        ccd_values = ccd_series.to_list()

        fields = source.fields()
        fields.append(QgsField("ccd", QVariant.Double))

        # Create sink
        (sink, dest_id) = self.parameterAsSink(
            parameters,
            self.OUTPUT,
            context,
            fields,
            source.wkbType(),
            source.sourceCrs(),
        )

        # Get features from source
        features = source.getFeatures()
        total = 100.0 / source.featureCount() if source.featureCount() else 0

        # Process each feature directly
        for current, feature in enumerate(features):
            if feedback.isCanceled():
                break

            # Create output feature
            output_feature = QgsFeature(fields)
            output_feature.setGeometry(feature.geometry())

            # Copy attributes and add new centroid corner distance
            attributes = feature.attributes()
            attributes.append(ccd_values[current])
            output_feature.setAttributes(attributes)

            # Add feature to sink
            sink.addFeature(output_feature, QgsFeatureSink.Flag.FastInsert)

            # Update progress
            feedback.setProgress(int(current * total))

        return {self.OUTPUT: dest_id}

    def createInstance(self):
        return self.__class__()


class Linearity(QgsProcessingAlgorithm):
    INPUT = "INPUT"
    OUTPUT = "OUTPUT"

    def name(self) -> str:
        return "linearity"

    def displayName(self) -> str:
        return "Linearity"

    def group(self) -> str:
        return "Shape"

    def groupId(self) -> str:
        return "shape"

    def shortHelpString(self) -> str:
        return "Calculates the linearity of each LineString"

    def initAlgorithm(self, configuration=None):
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT,
                "Input Layer",
                [QgsProcessing.SourceType.VectorLine],
            )
        )

        self.addParameter(QgsProcessingParameterFeatureSink(self.OUTPUT, "Linearity"))

    def processAlgorithm(self, parameters, context, feedback):
        source = self.parameterAsSource(parameters, self.INPUT, context)

        # Convert QGIS feature to GeoSeries and calculate linearity
        geometry_series = qgs_to_gpd(source)
        linearity_series = momepy.linearity(geometry_series)
        linearity_values = linearity_series.to_list()

        fields = source.fields()
        fields.append(QgsField("linearity", QVariant.Double))

        # Create sink
        (sink, dest_id) = self.parameterAsSink(
            parameters,
            self.OUTPUT,
            context,
            fields,
            source.wkbType(),
            source.sourceCrs(),
        )

        # Get features from source
        features = source.getFeatures()
        total = 100.0 / source.featureCount() if source.featureCount() else 0

        # Process each feature directly
        for current, feature in enumerate(features):
            if feedback.isCanceled():
                break

            # Create output feature
            output_feature = QgsFeature(fields)
            output_feature.setGeometry(feature.geometry())

            # Copy attributes and add new linearity
            attributes = feature.attributes()
            attributes.append(linearity_values[current])
            output_feature.setAttributes(attributes)

            # Add feature to sink
            sink.addFeature(output_feature, QgsFeatureSink.Flag.FastInsert)

            # Update progress
            feedback.setProgress(int(current * total))

        return {self.OUTPUT: dest_id}

    def createInstance(self):
        return self.__class__()


class CompactnessWeightedAxis(QgsProcessingAlgorithm):
    INPUT = "INPUT"
    OUTPUT = "OUTPUT"

    def name(self) -> str:
        return "compactness_weighted_axis"

    def displayName(self) -> str:
        return "Compactness weighted axis"

    def group(self) -> str:
        return "Shape"

    def groupId(self) -> str:
        return "shape"

    def shortHelpString(self) -> str:
        return (
            "Calculates the compactness-weighted axis of each object in a given layer."
        )

    def initAlgorithm(self, configuration=None):
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT,
                "Input layer",
                [QgsProcessing.SourceType.VectorPolygon],
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSink(self.OUTPUT, "Compactness weighted axis")
        )

    def processAlgorithm(self, parameters, context, feedback):
        source = self.parameterAsSource(parameters, self.INPUT, context)

        # Convert QGIS source to GeoSeries and calculate compactness-weighted axis
        geometry_series = qgs_to_gpd(source)
        cwa_series = momepy.compactness_weighted_axis(geometry_series)
        cwa_values = cwa_series.to_list()

        # Create output fields (original fields + new cwa field)
        fields = source.fields()
        fields.append(QgsField("cwa", QVariant.Double))

        # Create sink
        (sink, dest_id) = self.parameterAsSink(
            parameters,
            self.OUTPUT,
            context,
            fields,
            source.wkbType(),
            source.sourceCrs(),
        )

        # Get features from source
        features = source.getFeatures()
        total = 100.0 / source.featureCount() if source.featureCount() else 0

        # Process each feature directly
        for current, feature in enumerate(features):
            if feedback.isCanceled():
                break

            # Create output feature
            output_feature = QgsFeature(fields)
            output_feature.setGeometry(feature.geometry())

            # Copy attributes and add new cwa
            attributes = feature.attributes()
            attributes.append(cwa_values[current])
            output_feature.setAttributes(attributes)

            # Add feature to sink
            sink.addFeature(output_feature, QgsFeatureSink.Flag.FastInsert)

            # Update progress
            feedback.setProgress(int(current * total))

        return {self.OUTPUT: dest_id}

    def createInstance(self):
        return self.__class__()


class SunlightOptimised(QgsProcessingAlgorithm):
    pass
