import findspark
findspark.init()
import pyspark
from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.ml.feature import VectorAssembler, StringIndexer
from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml.evaluation import MulticlassClassificationEvaluator

spark = SparkSession.builder.appName('iris_clf').getOrCreate()
df = spark.read.csv('iris.csv', header=True, inferSchema=True)

schema = StructType([
    StructField('sepal_length', DoubleType()),
    StructField('sepal_width', DoubleType()),
    StructField('petal_length', DoubleType()),
    StructField('petal_width', DoubleType()),
    StructField('type', StringType())
])

df2 = spark.read.csv('iris.csv', header=True, schema=schema)

input_cols = ['sepal_length','sepal_width','petal_length','petal_width']
output_col = ['type']
vectorizer = VectorAssembler(inputCols=input_cols, outputCol="features")

df = vectorizer.transform(df2)

indexer = StringIndexer(inputCol='type', outputCol='indexed_type')

df = indexer.fit(df).transform(df)

df_train, df_test = df.randomSplit([0.7, 0.2], seed=0)

rf_clf = RandomForestClassifier(featuresCol='features', labelCol='indexed_type')

rf_clf = rf_clf.fit(df_train)
df_test = rf_clf.transform(df_test)

criterion = MulticlassClassificationEvaluator(labelCol='indexed_type', predictionCol='prediction')
accuracy = criterion.evaluate(df_test)
print('#####', accuracy, '#####')
