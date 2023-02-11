
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


##################################################################
# LOADING AND PREPARING THE DATA
##################################################################

# printing the csv files
acute = pd.read_csv('data/acute.csv')
maternity = pd.read_csv('data/maternity.csv')
athletics = pd.read_csv('data/athletics.csv')


print(acute.head(20))
print(maternity.head(20))
print(athletics.head(20))

# Change the column names, so they can work with each other
maternity.rename(columns={'UNIT': 'unit','Sex': 'gender'},
                inplace=True)
athletics.rename(columns={'Unit': 'unit','Male/female': 'gender'},
              inplace=True)

# Merging the files
df = pd.concat([acute, maternity, athletics], ignore_index=True)

# Deleting the unneeded column
df.drop(columns='Unnamed: 0', inplace=True)

print(df.sample(n=20, random_state=30))

# Drop empty rows
df.dropna(how='all', inplace=True)

# Correct all the gender column values to f and m respectively
df['gender'] = df['gender'].replace({'female': 'f',
                                     'male': 'm',
                                     'man': 'm',
                                     'woman': 'f'})

# Replace the NaN values in the gender column of the maternity unit with f
df['gender'].fillna('f', inplace=True)



# Replace the NaN values in the bmi, diagnosis, blood_test, ecg, ultrasound, mri, xray, children, months columns with 0s
cols = ['bmi',
        'diagnosis',
        'blood_test',
        'ecg',
        'ultrasound',
        'mri',
        'xray',
        'children',
        'months']
df[cols] = df[cols].fillna(0)


# Print shape of the resulting DataFrame
print(f'Data shape: {df.shape}')

# Print random 20 rows of the resulting DataFrame
print(df.sample(n=20, random_state=30))



##################################################################
#  Answering Client's Questions
##################################################################


# save the columns into variables as lists
bmi_col = list(df['bmi'])
diagnosis_col = list(df['diagnosis'])
blood_test_col = list(df['blood_test'])
ecg_col = list(df['ecg'])
ultrasound_col = list(df['ultrasound'])
mri_col = list(df['mri'])
xray_col = list(df['xray'])
children_col = list(df['children'])
months_col = list(df['months'])


print("****************************************************************")
print("*                                                              *")
print("*                 ANSWERS TO THE HOSPITAL QUESTIONS            *")
print("*                                                              *")
print("****************************************************************")



# Q1. Find the unit with the least number of patients

totals = df.unit.value_counts()
min_index = totals.idxmin()
print('The unit with the least number of patients is the', min_index.capitalize(), 'Unit')
print()

# Q2. Find the unit with the most number of patients

totals = df.unit.value_counts()
max_index = totals.idxmax()
print('The unit with the most number of patients is the', max_index.capitalize(), 'Unit')
print()



# Q3. What share of the Acute unit has a cold

acute_unit = df[df['unit'] == 'acute']
acute_cold = (acute_unit['diagnosis'] == 'cold').mean()
print(f'The answer to the 3rd question is {round(acute_cold, 3)}')
print()




# Q4. What share of the athletics unit has fracturs
athletics_unit = df[df['unit'] == 'athletics']
athletics_fracture = (athletics_unit['diagnosis'] == 'fracture').mean()
print(f'The answer to the 4th question is {round(athletics_fracture, 3)}')
print()




# Q5. What is the difference in the median ages of the patients in the acute and materninty units?
 
maternity_unit = df[df['unit'] == 'maternity']
acute_median_age = acute_unit['age'].median()
maternity_median_age = maternity_unit['age'].median()
difference = maternity_median_age - acute_median_age
print(f'The answer to the 5th question is {abs(difference)}')
print()



# Q6. Find the unit where blood tests were taken the most often

df_t = df[df["blood_test"] == "t"]
unit_counts = df_t["unit"].value_counts()
max_t_unit = unit_counts.index[0]
max_t_count = unit_counts.iloc[0]
print("The answer to the 6th question is", max_t_unit, max_t_count, "blood tests")
print()



# Q7. Find the standard deviations of the ages in each unit

# Calculate standard deviation of age in the acute unit
acute_age_std = acute['age'].std()
print(f'Standard deviation of age in the Acute unit: {acute_age_std.round(4)}')

# Calculate standard deviation of age in the maternity unit
maternity_age_std = maternity['age'].std()
print(f'Standard deviation of age in the Maternity unit: {maternity_age_std.round(4)}')

# Calculate standard deviation of age in the athletics unit
athletics_age_std = athletics['age'].std()
print(f'Standard deviation of age in the athletics unit: {athletics_age_std.round(4)}')
print()


# Q8. Print the number of patients in each unit

all_patients = df.unit.value_counts()

print(all_patients)
print()



##################################################################
# Visualising Data
##################################################################



# List of all the ages of patients in all units
ages = df['age'].tolist()

# Create age ranges
age_ranges = [0, 15, 35, 55, 70, 80]

# Create a histogram using the age ranges and ages data
plt.figure(figsize=(10, 7))
plt.hist(ages, bins=age_ranges, edgecolor='black', rwidth=0.8)

# Add x-axis label and y-axis label
plt.xlabel('Age Ranges')
plt.ylabel('Number of Patients')

# Add title to the histogram
plt.title('Age Distribution of Patients among all units')

# Show the plot
plt.show()




# Count the occurrences of each diagnosis
diagnosis_counts = df['diagnosis'].value_counts()
# print(diagnosis_counts)
most_common_diagnosis = diagnosis_counts.index[0]

# Plot the pie chart
plt.figure(figsize=(10, 7))
plt.pie(diagnosis_counts,
        labels=diagnosis_counts.index,
        autopct='%1.1f%%',
        startangle=90,
        shadow=True,
        explode=[0 if x != most_common_diagnosis else 0.1 for x in diagnosis_counts.index],
        counterclock=False)
plt.axis('equal')
plt.title("Most Common Diagnosis among Patients in all units")
plt.legend(loc='best', bbox_to_anchor=(1, 0, 0.5, 1))
plt.tight_layout()
plt.show()




# Get the ages and BMIs from the athletics medical unit data
ages = athletics_unit['age']
bmis = athletics_unit['bmi']

# Create the scatter plot
plt.figure(figsize=(10, 7))
plt.scatter(ages, bmis, marker='o', c='red', edgecolors='black')

# Add x-axis label and y-axis label
plt.xlabel('Age')
plt.ylabel('BMI')

# Add title to the scatter plot
plt.title('Age vs BMI in Athletics Medical Unit')

# Show the plot
plt.show()




# Plot the violin plot
plt.figure(figsize=(10, 7))
sns.violinplot(data=df, x="unit", y="height", palette='PuBu')

# Add quantile lines to the violin plot
sns.stripplot(data=df, x="unit", y="height", jitter=True, size=2.5, color='black')

# Add x-axis label and y-axis label
plt.xlabel('Medical Units')
plt.ylabel('Height (in cm)')

# Add title to the violin plot
plt.title('Distribution of Heights among Medical Units')

# Remove the y-axis numbers
plt.yticks([])

# Show the plot
plt.show()









