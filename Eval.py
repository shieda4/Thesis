from lib.neural_network import Residual
from lib.data_store import Store

if __name__ == '__main__':
    net = Residual()
    store = Store()

    net.load_model('models/model2')
    store.load_store('store1')

    net.evaluate(store.merged)
