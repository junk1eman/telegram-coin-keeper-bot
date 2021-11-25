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


# your_data = [('АРЕНДА', 31500), ('АВТО', 12100), ('ОТПУСК', 9900), ('ПОДАРКИ', 9595), ('ЕДАВНЕДОМА', 5253), ('ЕДА', 2630), ('НАКОПЛЕНИЯ', 2000), ('ТРАНСПОРТ', 1458), ('АЛКОГОЛЬ', 1450), ('ЗДОРОВЬЕ', 587), ('НАЛОГ', 500), ('ДОМ', 264), ('МАРИНА', 0)]
#
# your_data = analyse_data(your_data)
# plot_diagram(your_data)
