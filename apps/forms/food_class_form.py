from wtforms import Form, StringField, SelectField, validators, DecimalField, BooleanField

from apps.models.food_model import MenuCategory


class FoodClassForm(Form):
    name = StringField(label="菜品分类名",
                       validators=[
                           validators.Length(max=32, message="最多32个字"),
                           validators.DataRequired(message="菜品分类名必填")
                       ],
                       render_kw={'class': 'form-control', 'placeholder': '请输入菜品分类名'}
                       )
    description = StringField(label="菜品分类描述",
                              validators=[
                                  validators.Length(max=128, message="最多128个字"),
                                  validators.DataRequired(message="菜品分类描述必填")
                              ],
                              render_kw={'class': 'form-control', 'placeholder': '请输入菜品分类描述'}
                              )
    type_accumulation = StringField(label="菜品分类编号",
                                    validators=[
                                        validators.Length(max=16, message="最多16个字"),
                                        validators.DataRequired(message="菜品分类编号必填")
                                    ],
                                    render_kw={'class': 'form-control', 'placeholder': '请输入菜品分类编号'}
                                    )
    is_default = BooleanField(label="是否默认", default=False)

    shop_id = SelectField(label="所属店铺", coerce=str,
                          validators=[validators.DataRequired(message='请选择标签'), ],
                          render_kw={'class': 'form-control'},
                          default=1,
                          )

    def __init__(self, user, *args, **kwargs):
        super(FoodClassForm, self).__init__(*args, **kwargs)
        self.shop_id.choices = [(i.pub_id, i.shop_name) for i in user.shop_seller]

    # def __init__(self, shop, *args, **kwargs):
    #     super(FoodClassForm, self).__init__(*args, **kwargs)
    #     self.shop = shop
    #
    # def validate_is_default(self, obj):
    #     m1 = MenuCategory.query.filter(
    #         MenuCategory.shop == self.shop,
    #         MenuCategory.is_default == True,
    #     ).first()
    #     if m1:
    #         obj.data = False





