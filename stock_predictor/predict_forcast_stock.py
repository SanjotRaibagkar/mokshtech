import sys


model=['RNN']


if __name__ == '__main__':
    ''' to predict stocks from property : run : python <filename> p x
        to preict particular symbol : run :     python filenmae p symbol
        to predict and run forcast : run :      python <filename> p x x f x
        to only run forcast for report :run :   python <filename> f x
        to run forcast for a symbol  : run      python <filename> f symbol days
    '''
    print(sys.argv)
    try:
        assert sys.argv[1]=='p' or sys.argv[1]=='f'
        from stockprediction import exe_predictstock as ex_p
        from stockprediction import exe_forcaststock as fs

        if sys.argv[1]=='p':
            if sys.argv[2]!='x':
                ex_p.predictstock(sys.argv[2])
            else:
                ex_p.exe_predictstock()
            if sys.argv[3]=='f':
                if sys.argv[4]!='x':
                    fs.final_run(sys.argv[4],sys.argv[5])
                else:
                    fs.final_run()


        elif sys.argv[1]=='f':
            if sys.argv[2]!='x' or sys.argv[2]!="":
                fs.final_run(sys.argv[2],sys.argv[3])
            else:
                fs.final_run()
        else:
            print(''' to predict stocks from property : run :                   python <filename> p x
                        to predict particular symbol : run :                    python <filename> p symbol
                        to predict and run forcast : run  :                     python <filename> p x x f x
                        to only run forcast from predict report :run:           python <filename> f x
                        to run forcast for a symbol without prediction  : run : python <filename> f symbol days
                    ''')
    except Exception as e:
        print('predict_forcast_stock',e)
        print(''' to predict stocks from property : run :           python <filename> p x
            to predict particular symbol : run :                    python <filename> p symbol
            to predict and run forcast : run  :                     python <filename> p x x f x
            to only run forcast from predict report :run:           python <filename> f x
            to run forcast for a symbol without prediction  : run : python <filename> f symbol days
        ''')
