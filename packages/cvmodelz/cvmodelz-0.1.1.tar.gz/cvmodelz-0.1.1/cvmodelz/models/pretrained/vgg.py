from chainer import links as L
from chainer.links.model.vision.vgg import prepare
from chainer.links.model.vision.vgg import _max_pooling_2d

from cvmodelz.models.meta_info import ModelInfo
from cvmodelz.models.pretrained.base import PretrainedModelMixin

def _vgg_meta(final_conv_layer):
	return ModelInfo(
		name="VGG",
		input_size=224,
		feature_size=4096,
		n_conv_maps=512,

		conv_map_layer=final_conv_layer,
		feature_layer="fc7",

		classifier_layers=["fc6", "fc7", "fc8"],

		prepare_func=prepare,
	)

class BaseVGG(PretrainedModelMixin):
	def __init__(self, *args, **kwargs):
		kwargs["pooling"] = kwargs.get("pooling", _max_pooling_2d)
		super().__init__(*args, **kwargs)

	@property
	def functions(self):
		return super().functions

	def init_model_info(self):
		self.meta = _vgg_meta(self.final_conv_layer)

class VGG19(BaseVGG, L.VGG19Layers):
	final_conv_layer = "conv5_4"


class VGG16(BaseVGG, L.VGG16Layers):
	final_conv_layer = "conv5_3"

