from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("ActorNames").getOrCreate()

movies = spark.read.csv("s3://cs383-final-project/movies.csv",header=True,inferSchema=True)
tags = spark.read.csv("s3://cs383-final-project/tags.csv",header=True,inferSchema=True)

#Join tags file with movies
tagNames = tags.join(movies, "movieId")

tagNames = tagNames.withColumn("tag_lower", tagNames["tag"].cast("string"))

#Filter for only specific actors
jack_black = tagNames.filter(tagNames.tag_lower.contains("jack black"))
keanu_reeves = tagNames.filter(tagNames.tag_lower.contains("keanu reeves"))
christian_bale = tagNames.filter(tagNames.tag_lower.contains("christian bale"))

#Combine them
result = jack_black.union(keanu_reeves).union(christian_bale)
#Only keep necessary columns
result = result.select("movieId", "title", "tag")

result.write.mode("overwrite").csv("s3://cs383-final-project/output/actorMovies",header=True)

spark.stop()
