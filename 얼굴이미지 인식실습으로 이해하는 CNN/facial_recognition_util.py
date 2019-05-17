from pandas.io.parsers import read_csv
import os
import numpy as np
from sklearn.utils import shuffle

image_file_training = 'training.csv'

def load(test=False, cols=None):
    image_file = image_file_test if test else image_file_training
    image_df = read_csv(os.path.expanduser(image_file))  # load pandas dataframe

    # The Image column has pixel values separated by space; convert
    # the values to numpy arrays:
    image_df['Image_arr'] = image_df['Image'].apply(lambda im: np.fromstring(im, sep=' '))

    if cols:  # get a subset of columns
        image_df = image_df[list(cols) + ['Image_arr']]

    print(image_df.count())  # prints the number of values for each column
    image_df_clean = image_df.dropna()  # drop all rows that have missing values in them

    X = np.vstack(image_df_clean['Image_arr'].values) / 255.  # scale pixel values to [0, 1]
    X = X.astype(np.float32)

    if not test:  # only FTRAIN has any target columns
        y = image_df_clean[image_df_clean.columns[:-2]].values
        y = (y - 48) / 48  # scale target coordinates to [-1, 1]
        X, y = shuffle(X, y, random_state=42)  # shuffle train data
        y = y.astype(np.float32)
    else:
        y = None

    return X, y

def plot_sample(x, y, axis):
    img = x.reshape(96, 96)
    points = y.reshape(30,)
    axis.imshow(img, cmap="gray")
    axis.scatter(points[0::2] * 48 + 48, points[1::2] * 48 + 48, marker='x', s=50, c='r')
