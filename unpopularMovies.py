from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("Unpopular Movies").getOrCreate()

ratings = spark.read.csv("s3://cs383-final-project/ratings.csv", header=True, inferSchema=True)
movies = spark.read.csv("s3://cs383-final-project/movies.csv", header=True, inferSchema=True)

ratings = ratings.withColumn("rating", ratings["rating"].cast("float"))
#find popularity based on number of ratings
unpopular = ratings.groupBy("movieId").count()
unpopular = unpopular.withColumnRenamed("count", "num_ratings")
#add title column and genre
unpopular = unpopular.join(movies, "movieId")
#sorts from least to most popular
unpopular = unpopular.orderBy("num_ratings", ascending=True)

unpopular.write.mode("overwrite").csv("s3://cs383-final-project/output/unpopularMovies", header=True)

spark.stop()
