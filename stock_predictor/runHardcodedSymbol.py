from stockprediction import exe_predictstock as ex_p
from stockprediction import exe_forcaststock as fs

model=['RNN']

if __name__ == '__main__':
    ex_p.predictstock("BANKNIFTY")
    fs.final_run("BANKNIFTY", 1)
