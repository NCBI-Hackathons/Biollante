import pickle
from sklearn.metrics import confusion_matrix
import numpy as np

with open('mystery_predictions.p', 'rb') as h:

    m_pred = pickle.load(h)

with open('mystery_y_test.p', 'rb') as h:

    m_true = pickle.load(h)

m_pred = np.array(m_pred)
m_true = np.array(m_true)

cm = confusion_matrix(m_true, m_pred)

print cm
