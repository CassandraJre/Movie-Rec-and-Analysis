from pyspark.sql import SparkSession
spark = SparkSession.builder.appName("averageRatings").getOrCreate()

ratings = spark.read.csv("s3://cs383-final-project/ratings.csv", header=True, inferSchema=True)
movies = spark.read.csv("s3://cs383-final-project/movies.csv", header=True, inferSchema=True)

#group ratings by movie and calculate average ratings
average_ratings = ratings.groupBy("movieId").avg("rating")
#combines avg ratings and titles to show in results
result = average_ratings.join(movies, "movieId")
#sorts with the best movies first
result = result.orderBy("avg(rating)", ascending=False)

#show first 20 lines for testing
result.show(20)

result.write.mode("overwrite").csv("s3://cs383-final-project/output/average_ratings", header=True)

spark.stop()
