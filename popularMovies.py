
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("PopularMovies").getOrCreate()

#load data
ratings = spark.read.csv("s3://cs383-final-project/ratings.csv", header=True, inferSchema=True)
movies = spark.read.csv("s3://cs383-final-project/movies.csv", header=True, inferSchema=True)

ratings = ratings.withColumn("rating", ratings["rating"].cast("float"))

#finds popularity based on number of ratings
popular = ratings.groupBy("movieId").count()
popular = popular.withColumnRenamed("count", "num-ratings")
#add title column and genre
popular = popular.join(movies, "movieId")
#sorts from most to least popular
popular = popular.orderBy("num-ratings", ascending=False)

popular.write.mode("overwrite").csv("s3://cs383-final-project/output/popular_movies", header=True)

spark.stop()
