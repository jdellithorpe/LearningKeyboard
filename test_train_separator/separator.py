import sys

data_filename = sys.argv[1]
num_labels = int(sys.argv[2])
num_test_examples = int(sys.argv[3])

test_example_counts = [0]*num_labels

data_file = open(data_filename, "r")

train_file = open(data_filename + "_train.svm", "wb")
test_file = open(data_filename + "_test.svm", "wb")

data = data_file.readlines()

for example in data:
    example_label = int(example.split(" ")[0])
    if test_example_counts[example_label] < num_test_examples:
        test_file.write(example)
        test_example_counts[example_label] += 1
    else:
        train_file.write(example)
