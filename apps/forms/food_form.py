from wtforms import Form, StringField, SelectField, validators, DecimalField
from wtforms.widgets import HiddenInput

from apps.models.food_model import MenuCategory


class FoodForm(Form):
    goods_name = StringField(label="菜品名称",
                             validators=[
                                 validators.Length(max=32, message="最多32个字"),
                                 validators.DataRequired(message="菜品名必填")
                             ],
                             render_kw={'class': 'form-control', 'placeholder': '请输入菜品名'}
                             )

    goods_price = DecimalField(label="菜品价钱", places=2,
                               validators=[
                                   validators.DataRequired(message="菜品价格必填")
                               ],
                               render_kw={'class': 'form-control', 'placeholder': '请输入菜品价格'}
                               )

    category_id = SelectField(label="菜品分类",
                              validators=[validators.DataRequired(message='请选择标签'), ],
                              render_kw={'class': 'form-control'},
                              default=1,
                              coerce=str
                              )
    description = StringField(label="菜品描述",
                              validators=[
                                  validators.Length(max=128, message='最多128个字符'),
                                  validators.DataRequired(message="菜品描述必填")
                              ],
                              render_kw={'class': 'form-control', 'placeholder': '请输入菜品描述'}
                              )
    tips = StringField(label="菜品提示信息",
                       validators=[
                           validators.Length(max=128, message='最多128个字符'),
                           validators.DataRequired(message="菜品提示信息必填")
                       ],
                       render_kw={'class': 'form-control', 'placeholder': '请输入菜品提示信息'}
                       )
    goods_img = StringField(label='菜品图片', id="image-input", widget=HiddenInput())

    def __init__(self, pub_id, *args, **kwargs):
        super(FoodForm, self).__init__(*args, **kwargs)
        self.category_id.choices = [(str(v.pub_id), v.name) for v in
                                    MenuCategory.query.filter(MenuCategory.shop_id == pub_id).all()]

    def validate_goods_price(self, obj):
        obj.data = float("{:.2f}".format(obj.data))
    #
    # def __init__(self, shop, *args, **kwargs):
    #     super(FoodForm, self).__init__(*args, **kwargs)
    #     self.category_id.choices = [(cate.id, cate.name) for cate in shop.categories]
