from analytix import analytics
from analytix.youtube import YouTubeAnalytics, YoutubeService

service = YoutubeService("/Users/chouwilliam/OrbitNext/secret.json")
service.authorise()

analytics = YouTubeAnalytics(service)
report = analytics.retrieve(dimensions = ("days",))
df = report.to_dataframe()
print(df.head())
