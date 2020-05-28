from data_store import Store

store = Store()
store.load_store('merged')
if store.player1[0][2] == 0:
    store.update_values(player1=-1, player2=1)
else:
    store.update_values(player1=1, player2=-1)
store.save_store('merged_edited')
