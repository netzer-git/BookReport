import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

AMAZON_FILE = "DataSets/amazon-bestselling.csv"
GOODREADS_FILE = "DataSets/goodreads.csv"

BD_MAIN_DS = "C:/Users/ADMIN/Documents/DB/bd_dataset.csv"
BD_CATEGORIES = "C:/Users/ADMIN/Documents/DB/bd_categories.csv"
BD_AUTHORS = "C:/Users/ADMIN/Documents/DB/bd_authors.csv"

READING_BD = False
PLOTS = ["BookDepository: Average rating / Number of rating",
         "GoodReads: Average rating / Number of ratings",
         "GoodReads: Average rating / Number of text reviews",
         "BookDepository: Split books by Rating-Average",
         "GoodReads: Split books by Rating-Average",
         "GoodReads: Number of ratings / Number of text reviews"]


def read_files():
    dataframes = dict()
    dataframes['amazon_best'] = pd.read_csv(AMAZON_FILE)

    dataframes['goodreads'] = pd.read_csv(GOODREADS_FILE)
    dataframes['goodreads']['average_rating'] = pd.to_numeric(dataframes['goodreads']['average_rating'], errors='coerce')

    dataframes['bookdepository'] = pd.read_csv(BD_MAIN_DS) if READING_BD else None
    return dataframes


def plot_rating_avg_count_scatter_chart(df, x_field, y_field, title):
    df.plot.scatter(x=x_field, y=y_field, title=title)
    plt.gcf().autofmt_xdate()
    plt.show()


def plot_rating_avg_bar_chart(df, rating_avg_field, title):
    """
    Plots bar chars for specific df, arranging in X ratings (1-2, 2-3, 3-4, 4-5) and in Y number of books that got the
    rating.
    :param df: pd data frame
    :param rating_avg_field: name of the field containing the average rating
    """
    print("------- Creating plot_rating_avg_bar_chart! -------")

    avg_c = [0, 0, 0, 0]
    count = 0
    e_count = 0

    for i in range(len(df[rating_avg_field])):
        count += 1
        current_rating = df[rating_avg_field][i]
        try:
            avg_c[int(float(current_rating)) - 1] += 1
        except ValueError:
            e_count += 1
            # print(current_rating)
        except IndexError:
            if int(current_rating) == 5:
                avg_c[3] += 1
            else:
                raise Exception

    print(avg_c)
    print("reading: " + str(count))
    print("counting: " + str(sum(avg_c)))
    print("Erroring: " + str(e_count))

    rating_avg_df = pd.DataFrame(data=
    {
        "rating-avg": ["1-2", "2-3", "3-4", "4-5"],
        "number-of-books": avg_c
    })
    rating_avg_df.plot.bar(x="rating-avg", y="number-of-books", color="#DAA520", rot=45, title=title)
    plt.show()


def plot_limited_rating_avg_graph(df, rating_avg_field, title):
    print("------- Creating plot_rating_avg_graph! -------")

    avg_c = [0 for i in range(20)]  # [0 ... 19]
    count = 0
    e_count = 0

    for i in range(len(df[rating_avg_field])):
        count += 1
        current_rating = df[rating_avg_field][i]
        try:
            index = int(float(current_rating) * 10) - 30
            if 0 <= index <= 19:
                avg_c[index] += 1
            else:
                pass
        except ValueError:
            e_count += 1
        except IndexError:
            if int(current_rating) == 5:
                avg_c[19] += 1
            else:
                raise Exception

    print(avg_c)
    print("reading: " + str(count))
    print("counting: " + str(sum(avg_c)))
    print("Erroring: " + str(e_count))

    rating_avg_df = pd.DataFrame(data=
    {
        "rating-avg": [3 + float(i)/10 for i in range(0, 20, 1)],
        "number-of-books": avg_c
    })
    rating_avg_df.plot(x="rating-avg", y="number-of-books", color="#20B2AA", rot=45, title=title)
    plt.show()


def main():
    dataframes = read_files()
    amazon_best = dataframes['amazon_best']
    goodreads = dataframes['goodreads']
    bookdepository = dataframes['bookdepository']

    print("------- Pre Process Checks! -------")
    # print(amazon_best['Name'])
    # amazon_best_names = {name.lower() for name in amazon_best['Name']}
    # print(len(amazon_best_names))
    # counter = 0
    # for name in goodreads['title']:
    #     if name.lower() in amazon_best_names:
    #         counter += 1
    # print(counter)

    # print(len(goodreads['bookID']))
    # for i in range(len(goodreads['bookID'])):
    #     try:
    #         if float(goodreads['average_rating'][i]) > 5 and goodreads['ratings_count'][i] > 100_000:
    #             print(goodreads['title'][i])
    #     except ValueError:
    #         pass

    # for i in range(len(bookdepository['bestsellers-rank'])):
    #     try:
    #         if float(bookdepository['bestsellers-rank'][i]) < 1_000:
    #             print(str(bookdepository['bestsellers-rank'][i]) + " : " + str(bookdepository['title'][i]))
    #     except ValueError:
    #         pass
    #
    #
    # for i in range(len(bookdepository['bestsellers-rank'])):
    #     try:
    #         if float(bookdepository['rating-count'][i]) > 8_000_000:
    #             print(str(bookdepository['rating-avg'][i]) + ":" + str(bookdepository['rating-count'][i]) +
    #                   " -> " + str(bookdepository['title'][i]))
    #     except ValueError:
    #         pass
    #
    # for i in range(len(goodreads['title'])):
    #     if goodreads['ratings_count'][i] > 4_000_000:
    #         print(str(goodreads['title'][i]) + " : " + str(goodreads['average_rating'][i]))

    print("------- time to plot! -------")
    # print(bookdepository.head())
    # a = bookdepository['rating-avg']
    # b = bookdepository['rating-count']
    # plt.scatter(a, b)

    # bookdepository.plot.scatter(x="rating-avg", y="rating-count")
    # plt.gcf().autofmt_xdate()
    # plt.show()

    print("------- Plotting Bar Charts! -------")
    # plot_rating_avg_bar_chart(bookdepository, 'rating-avg', PLOTS[3])
    # plot_rating_avg_bar_chart(goodreads, 'average_rating', PLOTS[4])

    print("------- Plotting Scatter plots! -------")
    # plot_rating_avg_count_scatter_chart(bookdepository, 'rating-avg', 'rating-count', PLOTS[0])
    # plot_rating_avg_count_scatter_chart(goodreads, 'average_rating', 'ratings_count', PLOTS[1])
    # plot_rating_avg_count_scatter_chart(goodreads, 'average_rating', 'text_reviews_count', PLOTS[2])

    print("------- Plotting Scatter plots - now without Twilight! -------")
    # gooders_normalized = goodreads.drop([10340])                                        # removing Twilight
    # gooders_normalized = gooders_normalized[gooders_normalized['average_rating'] > 0]   # removing 0 stars
    # plot_rating_avg_count_scatter_chart(gooders_normalized, 'average_rating', 'ratings_count', PLOTS[1] + ": without Twilight")
    # plot_rating_avg_count_scatter_chart(goodreads, 'average_rating', 'text_reviews_count', PLOTS[2] +": without Twilight")

    print("------- Plotting Rating Charts in 3-5! -------")
    # plot_limited_rating_avg_graph(goodreads, 'average_rating', PLOTS[3])
    # plot_limited_rating_avg_graph(bookdepository, 'rating-avg', PLOTS[4])

    plot_rating_avg_count_scatter_chart(goodreads.drop([10340]), 'text_reviews_count', 'ratings_count', PLOTS[5])



if __name__ == '__main__':
    main()
