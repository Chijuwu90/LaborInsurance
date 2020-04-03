import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import locale
pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)
locale.setlocale(locale.LC_ALL, 'en_US')


start_working_year = 1988
increase_rate_year = 2019
previous_rate = 43500
current_rate = 45800
default_refund_year = 2028
pay_per_year = 37200
current_year = 2020
years = np.arange(2023, 2045)
years = np.insert(years, 0, 0., axis=0)


def cal_refund(start_getting_refund_year):

    total_working_year = start_getting_refund_year - start_working_year
    total_pay = (start_getting_refund_year - current_year) * pay_per_year

    refund_off_by = 1 - (default_refund_year - start_getting_refund_year)*0.04

    if start_getting_refund_year >= 2024:
        monthly_avg_income = 45800
    else:
        monthly_avg_income = 45340

    refund = np.zeros(shape=len(years)-1)

    for i in range(1, len(years)):
        year = years[i]
        refund[i-1] = monthly_avg_income * total_working_year * 0.0155 * refund_off_by * (year - start_getting_refund_year) * 12

    refund = np.insert(refund, 0, total_pay, axis=0)
    return refund


if __name__ == '__main__':

    color = ['b', 'r', 'k', 'g', 'y', 'orange']
    starts = np.arange(2023, 2029)
    df = pd.DataFrame(columns=["refund"])

    for i, start in enumerate(starts):
        if i == 0:
            df["year"] = years
            df.index = df["year"]
            df["age"] = df["year"].apply(lambda x: x - 1963)
            df[df["age"] < 0] = 0

        refunds = cal_refund(start)
        refunds[refunds < 0] = 0

        age = start-1963
        df["refund_" + str(start) + "(age " + str(age) + ")"] = refunds
        df["refund_" + str(start) + "(age " + str(age) + ")"] = df["refund_" + str(start) + "(age " + str(age) + ")"]\
            .apply(lambda x: locale.format_string("%d", int(x), grouping=True) if not np.isnan(x) else np.NAN)

        plt.plot(years[1:], refunds[1:], color=color[i])

    plt.xlabel("Year")
    plt.ylabel("Accumulative refund")
    plt.legend([2023, 2024, 2025, 2026, 2027, 2028])
    plt.yscale("log")
    plt.savefig("output/result.png", dpi=300)
    plt.show()

    df = df.drop(["refund", "year"], axis=1).reset_index()
    df.to_csv("output/retirement_refund.csv", index=False)
