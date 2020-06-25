from neural_network import Residual
from data_store import Store

net = Residual()
store = Store()

net.load_model('models/model2')
store.load_store('store1')

net.evaluate(store.merged)
