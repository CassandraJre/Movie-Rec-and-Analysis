from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("Recommendations").getOrCreate()

ratings = spark.read.csv("s3://cs383-final-project/ratings.csv", header=True, inferSchema=True)
movies = spark.read.csv("s3://cs383-final-project/movies.csv", header=True, inferSchema=True)

#ensure the rating is a float number
ratings = ratings.withColumn("rating", ratings["rating"].cast("float"))

#filters for best movies based on rating
bestMovies = ratings.filter(ratings.rating >= 4)
#counts number of high ratings per movie
recs = bestMovies.groupBy("movieId").count()
#add the title adn genre from movies.csv
recs = recs.join(movies, "movieId")

recs.write.mode("overwrite").csv("s3://cs383-final-project/output/recs", header=True)

spark.stop()
