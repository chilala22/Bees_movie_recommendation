from website import create_app

# import pandas


# data1=pandas.read_csv('./movie_dataset.csv')

# print(data1.head())

app = create_app()
#means only if this file is run can it be executed
if __name__ == '__main__':
    #regulates which main.py file is being run
    #debug=True: if anychanges made to file it will be automatically rerun, turn off in production
    app.run(debug=True, port = 8083)