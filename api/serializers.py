from rest_framework import serializers

from api.models import Article, StarArticle, Orders


class StarArticleSerializer(serializers.ModelSerializer):
	class Meta:
		model = StarArticle
		fields = 'star',


class ArticleSerializer(serializers.ModelSerializer):
	star = serializers.SerializerMethodField()

	@staticmethod
	def get_star(article):
		queryset = StarArticle.objects.filter(article=article)
		data = StarArticleSerializer(queryset, many=True).data
		total = 0
		for key in data:
			total += key['star']
		star = str(total // len(data))
		if (total % len(data)) >= len(data) // 2:
			star = '{}.5'.format(star)
		return star

	class Meta:
		model = Article
		fields = '__all__'


class OrderDetailSerializer(serializers.ModelSerializer):
	u_relname = serializers.SerializerMethodField()

	@staticmethod
	def get_u_relname(order):
		users = order.users_set.all()
		for user in users:
			if user.role.first().r_code != '0':
				return user.u_relname

	class Meta:
		model = Orders
		fields = ('order_money', 'u_relname', 'order_createtime', 'order_finishtime', 'order_number',
				  'order_addr', 'order_tips')
