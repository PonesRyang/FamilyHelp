from audioop import avg

from rest_framework import serializers

from api.models import Article, StarArticle


class StarArticleSerializer(serializers.ModelSerializer):
	class Meta:
		model = StarArticle
		fields = 'star',


class ArticleSerializer(serializers.ModelSerializer):
	star = serializers.SerializerMethodField()

	@staticmethod
	def get_star(article):
		queryset = StarArticle.objects.filter(article=article)
		data = StarArticleSerializer(queryset,many=True).data
		total = 0
		for key in data:
			total += key['star']
		star = str(total//len(data))
		if (total % len(data)) >= len(data)//2:
			star = '{}.5'.format(star)
		return star

	class Meta:
		model = Article
		fields = '__all__'
