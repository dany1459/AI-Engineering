import findspark
findspark.init()
import pyspark
from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
import joblib

spark = SparkSession.builder.appName('heart_clf').getOrCreate()
df = spark.read.csv('heart.csv', header=True, inferSchema=True)
df.show(2)
input_cols = ['age','sex', 'cp','trtbps','chol','fbs','restecg','thalachh','exng','oldpeak','slp','caa','thall']
vectorizer = VectorAssembler(inputCols=input_cols, outputCol='features')

df = vectorizer.transform(df)

df_train, df_test = df.randomSplit([0.8, 0.2], seed=0)

rf_clf = RandomForestClassifier(featuresCol='features', labelCol='output')

rf_clf = rf_clf.fit(df_train)
df_test = rf_clf.transform(df_test)

criterion = MulticlassClassificationEvaluator(labelCol='output', predictionCol='prediction')
accuracy = criterion.evaluate(df_test)
print('#####', accuracy, '#####')

joblib.dump(rf_clf, 'model.pkl')
