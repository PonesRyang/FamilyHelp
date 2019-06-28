# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Relationship17(models.Model):
    reid = models.AutoField(primary_key=True)
    co = models.ForeignKey('Complain', models.PROTECT, db_column='co_id')
    u = models.ForeignKey('Users', models.PROTECT, db_column='u_id')

    class Meta:
        managed = False
        db_table = 'Relationship_17'
        unique_together = (('co', 'u'),)


class Rolepermissions(models.Model):
    rpid = models.AutoField(primary_key=True)
    per = models.ForeignKey('Permission', models.PROTECT, db_column='per_id')  # Field name made lowercase.
    role = models.ForeignKey('Roles', models.PROTECT, db_column='ro_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'RolePermissions'
        unique_together = (('per', 'role'),)


class Userrole(models.Model):
    urid = models.AutoField(primary_key=True)
    role = models.ForeignKey('Roles', models.PROTECT, db_column='ro_id')  # Field name made lowercase.
    user = models.ForeignKey('Users', models.PROTECT, db_column='u_id')

    class Meta:
        managed = False
        db_table = 'UserRole'
        unique_together = (('role', 'user'),)


class Users(models.Model):
    u_id = models.AutoField(primary_key=True)
    id = models.ForeignKey('Wallet', models.PROTECT, db_column='id', blank=True, null=True)
    u_relname = models.CharField(max_length=128, blank=True, null=True)
    u_nickname = models.CharField(max_length=128)
    u_password = models.CharField(max_length=255, null=True)
    u_tel = models.CharField(max_length=11)
    u_birthday = models.DateField(blank=True, null=True)
    u_reg_time = models.DateField(auto_now_add=True, blank=True, null=True)
    u_photo = models.CharField(max_length=256, blank=True, null=True)
    u_point = models.IntegerField(blank=True, null=True)
    star_lv = models.IntegerField(blank=True, null=True)
    role = models.ManyToManyField('Roles',through='Userrole' )
    order = models.ManyToManyField('Orders', through='UserOrderList')
    comment = models.ManyToManyField('Comment', through='UserComment')
    id_card = models.CharField(max_length=30,null=True)

    class Meta:
        managed = False
        db_table = 'Users'


class Comment(models.Model):
    order = models.ForeignKey('Orders', models.PROTECT, blank=True, null=True)
    content = models.CharField(max_length=512, blank=True, null=True)
    content_star = models.IntegerField()
    is_delete = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'comment'


class Complain(models.Model):
    u = models.ForeignKey(Users, models.PROTECT, blank=True, null=True)
    complain_content = models.CharField(max_length=512)

    class Meta:
        managed = False
        db_table = 'complain'


class OrderComplain(models.Model):
    oc_id = models.AutoField(primary_key=True)
    complain = models.ForeignKey(Complain, models.PROTECT, db_column='co_id')
    order = models.ForeignKey('Orders', models.PROTECT, db_column='or_id')

    class Meta:
        managed = False
        db_table = 'order_complain'
        unique_together = (('complain', 'order'),)


class OrderType(models.Model):
    order_type_id = models.AutoField(primary_key=True)
    order = models.ForeignKey('Orders', models.PROTECT, blank=True, null=True)
    order_type_name = models.CharField(max_length=128)

    class Meta:
        managed = False
        db_table = 'order_type'


class Orders(models.Model):
    order_id = models.AutoField(primary_key=True)
    order_type = models.ForeignKey(OrderType, models.PROTECT, blank=True, null=True)
    order_number = models.CharField(max_length=128)
    order_status = models.IntegerField()
    order_createtime = models.DateTimeField(auto_now_add=True)
    order_finishtime = models.DateTimeField(blank=True, null=True)
    order_plantime = models.DateTimeField()
    order_addr = models.CharField(max_length=128)
    order_tips = models.CharField(max_length=128, blank=True, null=True)
    complain = models.ManyToManyField(Complain, through='OrderComplain')
    district = models.ForeignKey('District', models.PROTECT, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'orders'


class Permission(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    per_name = models.CharField(max_length=128)

    class Meta:
        managed = False
        db_table = 'permission'


class Roles(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    r_name = models.CharField(max_length=12)
    r_code = models.CharField(max_length=10, blank=True, null=True)
    permission = models.ManyToManyField(Permission, through='Rolepermissions')

    class Meta:
        managed = False
        db_table = 'roles'


class UserComment(models.Model):
    ucid = models.AutoField(primary_key=True)
    co = models.ForeignKey(Comment, models.PROTECT, db_column='co_id')
    u = models.ForeignKey(Users, models.PROTECT, db_column='u_id')

    class Meta:
        managed = False
        db_table = 'user_comment'
        unique_together = (('co', 'u'),)


class UserOrderList(models.Model):
    uoid = models.AutoField(primary_key=True)
    order = models.ForeignKey(Orders, models.PROTECT,db_column='or_id')
    u = models.ForeignKey(Users, models.PROTECT, db_column='u_id')

    class Meta:
        managed = False
        db_table = 'user_order_list'
        unique_together = (('order', 'u'),)


class Wallet(models.Model):
    money_int = models.IntegerField()
    money_decimal = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'wallet'


class District(models.Model):
    """地区"""
    distid = models.IntegerField(primary_key=True)
    parent = models.ForeignKey(to='self', on_delete=models.PROTECT, db_column='pid', blank=True, null=True)
    name = models.CharField(max_length=255)


    def __str__(self):
        return self.name

    class Meta:
        db_table = 'tb_district'



