import numpy as np
import pandas as pd

array = np.load(r"C:\Users\brand\Downloads\responses_211022.npy")

print(array)
counter = 0

sorted_images = np.argsort(array, axis=1)[:, ::-1]
sorted_responses = np.sort(array, axis=1)[:, ::-1]

most_activated = []
most_activated_responses = []

for row in sorted_images:
    top_four = row[:4]
    modified_top_four = [int(idx + 1) for idx in top_four]
    # Gets the top 4 most active images per neuron
    most_activated.append((modified_top_four))

for row in sorted_responses:
    top_four = row[:4]
    modified_top_four = [round(value, 4) for value in top_four]
    # Gets the neuronal responses of the top 4 most active images per neuron
    most_activated_responses.append((modified_top_four))

print(len(most_activated))

df = pd.DataFrame(most_activated, columns=[
                  '1st most activated', '2nd most activated', '3rd most activated', '4th most activated'])
df_responses = pd.DataFrame(most_activated_responses, columns=[
    '1st most activated', '2nd most activated', '3rd most activated', '4th most activated'])

df.index += 1
df_responses.index += 1

print(array[15, 1009])

# print(df)
# print(df_responses)

# df.to_csv('best_images.csv')
# df_responses.to_csv('response_data.csv')

# df_responses['row_mean'] = df_responses.mean(axis=1)
# df_sorted = df_responses.sort_values(
#     by='row_mean', ascending=False).drop(columns='row_mean')
# print(df_sorted)
# df_sorted.to_csv('most_activated_neurons.csv')
