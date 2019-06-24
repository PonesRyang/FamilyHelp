from rest_framework import serializers
from api.models import Article, StarArticle, Orders, Users, Roles, OrderType, District, Wallet


class RolesSimpleSerializer(serializers.ModelSerializer):
	class Meta:
		model = Roles
		fields = '__all__'


class RolesSerializer(serializers.ModelSerializer):
	class Meta:
		model = Roles
		fields = ('r_name',)


class StarStaffSerializer(serializers.ModelSerializer):
	role = serializers.SerializerMethodField()

	@staticmethod
	def get_role(user):
		return RolesSerializer(user.role, many=True).data

	class Meta:
		model = Users
		fields = ('u_relname', 'u_tel', 'u_birthday', 'u_photo', 'star_lv', 'role')


class OrdersTypeSerializer(serializers.ModelSerializer):
	class Meta:
		model = OrderType
		fields = ('order_type_name',)


class DistrictSimpleSerializer(serializers.ModelSerializer):
	class Meta:
		model = District
		fields = ('distid', 'name')


class DistrictDetailSerializer(serializers.ModelSerializer):
	cities = serializers.SerializerMethodField()

	@staticmethod
	def get_cities(district):
		queryset = District.objects.filter(parent=district)
		return DistrictSimpleSerializer(queryset, many=True).data

	class Meta:
		model = District
		fields = ('distid', 'name', 'cities')


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


class WalletSerializer(serializers.ModelSerializer):
	money = serializers.SerializerMethodField()

	@staticmethod
	def get_money(wallet):
		return '{}.{}'.format(wallet.money_int,wallet.money_decimal)

	class Meta:
		model = Wallet3
		fields = 'money',
