def get_sets(train_gen, test_gen):
    x_train, y_train = [], []
    x_test, y_test = [], []
    for x in train_gen:
        a, b = x
        for i, j in zip(a, b):
            x_train.append(i)
            y_train.append(j)
    for x in test_gen:
        a, b = x
        for i, j in zip(a, b):
            x_test.append(i)
            y_test.append(j)

    return x_train, x_test, y_train, y_test
