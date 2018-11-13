from wtforms import Form, StringField, validators, BooleanField, DecimalField
from wtforms.widgets import HiddenInput

from apps.models.shop_model import ShopSellerModel


class ShopForm(Form):
    shop_name = StringField(label="店铺名称",
                            validators=[
                                validators.Length(max=16, message="店铺名称最多16位"),
                                validators.DataRequired(message="必填")],
                            render_kw={'class': 'form-control', 'placeholder': '请输入店铺名'}
                            )

    brand = BooleanField(label="是否品牌", default=True)
    on_time = BooleanField(label="准时送达", default=False)
    fengniao = BooleanField(label='配送', default=True)
    bao = BooleanField(label='保险', default=False)
    piao = BooleanField(label='发票', default=False)
    zhun = BooleanField(label='准标识', default=False)
    start_send = DecimalField(label="起送价格", places=2,
                              validators=[
                                  validators.DataRequired(message="必填")],
                              render_kw={'class': 'form-control', 'placeholder': '请输入起送价格'}
                              )
    send_cost = DecimalField(label="配送价格", places=2,
                             validators=[
                                 validators.DataRequired(message="必填")],
                             render_kw={'class': 'form-control', 'placeholder': '请输入配送费用'}
                             )
    notice = StringField(label="店铺公告",
                         validators=[
                             validators.DataRequired(message="必填"),
                             validators.Length(max=128, message="不得超过128个字符")
                         ],
                         render_kw={'class': 'form-control', 'placeholder': '请输入店铺公告'}
                         )
    discount = StringField(label='优惠信息',
                           validators=[
                               validators.DataRequired(message='必填'),
                               validators.Length(max=128, message="不得超过128个字符")
                           ],
                           render_kw={'class': 'form-control', 'placeholder': '请输入优惠信息'}
                           )

    shop_img = StringField(label='店铺logo', id="image-input", widget=HiddenInput())

    def validate_start_send(self, obj):
        obj.data = float("{:.2f}".format(obj.data))

    def validate_send_cost(self, obj):
        obj.data = float("{:.2f}".format(obj.data))


