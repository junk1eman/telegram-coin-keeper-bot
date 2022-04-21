import matplotlib.pyplot as plt


def analyse_data(data):
    sum = 0
    for values in data:
        sum += values[1]
    result_data = {}
    other = 0
    for values in data:
        if values[1]/sum > 0.05:
            result_data.update({values[0]: values[1]})
        else:
            other += values[1]
            result_data.update({'ПРОЧЕЕ': other})
            # print(result_data)
    return result_data


def plot_diagram(data):
    labels = []
    sizes = []
    for x, y in data.items():
        labels.append(x)
        sizes.append(y)

        # Plot
    plt.pie(sizes, labels=labels, autopct='%1i%%')

    plt.axis('equal')
    # plt.xlabel('ВАШИ РАСХОДЫ ЗА МЕСЯЦ')
    plt.title('ВАШИ РАСХОДЫ ЗА МЕСЯЦ')
    plt.savefig('export/diagram.jpg')
    plt.clf()
    plt.cla()
    plt.close()

