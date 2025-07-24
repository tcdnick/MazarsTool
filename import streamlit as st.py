import streamlit as st
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
import pandas as pd


### python -m streamlit run risk_assessment_tool.py
### Ctrl + c ---> stop application


# QUESTIONS FOR LIKELIHOOD
Q1 = "What is the estimated total CO₂ emitted (in metric tons) from operations in the last reporting year?"
Q2 = "What is the estimated total methane emitted (in metric tons) from operations in the last reporting year?"
Q3 = "What percentage of hazardous waste is generated in tons per year?"
Q4 = "What is the annual water consumption in cubic billion meters per unit product?"
Q5 = "How likely is your company to draw water from stressed or protected sources?"
Q6 = "To what degree is wastewater treatment inconsistent or not monitored regularly?"
Q7 = "How much microfibre and microplastics is released in Kg per year?"
Q8 = "Amount of freshwater used by the industry in cubic billion meters per unit product?"
Q9 = "What percentage of your operational land overlaps or impacts forested or natural areas?"
Q10 = "What percentage of total industrial waste generated is recovered or recycled (EPI-based)?"
Q11 = "To what extent does your supply chain use recycled or secondary raw materials?"

# QUESTIONS FOR IMPACT
Q12 = "What is the estimated total CO₂ emitted (in metric tons) from operations in the last reporting year?"
Q13 = "What is the estimated total methane emitted (in metric tons) from operations in the last reporting year?"

# ANSWERS FOR LIKELIHOOD
A1 = ["N/A", "5", "4", "3", "2", "1"]
A2 = ["N/A", "5", "4", "3", "2", "1"]
A3 = ["N/A", "5", "4", "3", "2", "1"]
A4 = ["N/A", "5", "4", "3", "2", "1"]
A5 = ["N/A", "5", "4", "3", "2", "1"]
A6 = ["N/A", "5", "4", "3", "2", "1"]
A7 = ["N/A", "5", "4", "3", "2", "1"]
A8 = ["N/A", "5", "4", "3", "2", "1"]
A9 = ["N/A", "5", "4", "3", "2", "1"]
A10 = ["N/A", "5", "4", "3", "2", "1"]


# ANSWERS FOR IMPACT
A11 = ["N/A", "Not Serious", "Somewhat Serious", "Moderately Serious", "Serious", "Very Serious"]
A12 = ["N/A", "Not Serious", "Low Damage", "Some Damage", "Moderate Damage", "Major Damage"]
A13 = ["N/A", "Not Serious", "Low Damage", "Some Damage", "Moderate Damage", "Major Damage"]

# QUESTION AND ANSWER GROUPINGS
qlist_likelihood = [Q1, Q2, Q3, Q4, Q5, Q6, Q7, Q8, Q9]
alist_likelihood = [A1, A2, A3, A4, A5, A6, A7, A8, A9]
qlist_impact= [Q10, Q11, Q12, Q13]
alist_impact = [A10, A11, A12, A13]
    
with st.sidebar:
    st.header('Risk Factors Affecting the Likelihood')
    likelihood_total = 0
    likelihood_answers = 0
    for idx, question in enumerate(qlist_likelihood):
        ask = qlist_likelihood[idx]
        answer = alist_likelihood[idx]
        if idx == 0:
            # Use a slider for the first question
            box = st.slider(ask, min_value=1, max_value=10, value=5)
            user_answer = box  # Use the slider value directly
            likelihood_total += user_answer
            likelihood_answers += 1
        else:
            box = st.radio(ask, answer, index=3)
            user_answer = answer.index(box)
            likelihood_total += user_answer
            if box == "N/A":
                likelihood_answers += 0
            else:
                likelihood_answers += 1
    
    st.divider()
    
    st.header('Risk Factors Affecting the Impact')
    impact_total = 0
    impact_answers = 0
    for idx, question in enumerate(qlist_impact):
        ask = qlist_impact[idx]
        answer = alist_impact[idx]
        box = st.select_slider(ask, answer, value=answer[3])
        user_answer = answer.index(box)
        impact_total = user_answer + impact_total
        if box == "N/A":
            impact_answers = 0 + impact_answers
        else:
            impact_answers = 1 + impact_answers
    st.divider()
    st.markdown('Version 1.0')
    st.markdown('Developed by VEN, TCD')

if likelihood_answers == 0:
    likelihood_answers = 1

if impact_answers == 0:
    impact_answers = 1

# User risk score is reported based on the actual calculated number
# Axis have been switched as per egbc Version 4.0
x_pt = impact_total/impact_answers
y_pt = likelihood_total/likelihood_answers

x_user = [x_pt]
y_user = [y_pt]

# Determine the risk assessment category that is reported
if x_pt >= 0:
    if y_pt <= 3:
        report_ra = "Low Risk"
    else:
        report_ra = "Moderate Risk"
if x_pt >= 1:
    if y_pt <= 2:
        report_ra = "Low Risk"
    elif y_pt <= 4:
        report_ra = "Moderate Risk"
    else:
        report_ra = "High Risk"
if x_pt >= 2:
    if y_pt <= 1:
        report_ra = "Low Risk"
    elif y_pt <= 3:
        report_ra = "Moderate Risk"
    else:
        report_ra = "High Risk"
if x_pt >= 3:
    if y_pt <= 2:
        report_ra = "Moderate Risk"
    elif y_pt <= 4:
        report_ra = "High Risk"
    else:
        report_ra = "Very High Risk"
if x_pt >= 4:
    if y_pt <= 1:
        report_ra = "Moderate Risk"
    elif y_pt <= 3:
        report_ra = "High Risk"
    else:
        report_ra = "Very High Risk"

# Review the risk assessment category if the value is on a border category
# This code can be cleaned up in the future
if x_pt <= 1 and y_pt == 3:
    report_ra = "Low-to-Moderate Risk"
elif x_pt <= 2 and x_pt >= 1 and y_pt == 2:
    report_ra = "Low-to-Moderate Risk"
elif x_pt <= 3 and x_pt >= 2 and y_pt == 1:
    report_ra = "Low-to-Moderate Risk"

elif x_pt == 1 and y_pt >= 2 and y_pt <= 3:
    report_ra = "Low-to-Moderate Risk"
elif x_pt == 2 and y_pt >= 1 and y_pt <= 2:
    report_ra = "Low-to-Moderate Risk"
elif x_pt == 3 and y_pt >= 0 and y_pt <= 1:
    report_ra = "Low-to-Moderate Risk"

elif x_pt <= 2 and x_pt >= 1 and y_pt == 4:
    report_ra = "Moderate-to-High Risk"
elif x_pt <= 3 and x_pt >= 2 and y_pt == 3:
    report_ra = "Moderate-to-High Risk"
elif x_pt <= 4 and x_pt >= 3 and y_pt == 2:
    report_ra = "Moderate-to-High Risk"
elif x_pt <= 5 and x_pt >= 4 and y_pt == 1:
    report_ra = "Moderate-to-High Risk"

elif x_pt == 1 and y_pt >= 4 and y_pt <= 5:
    report_ra = "Moderate-to-High Risk"
elif x_pt == 2 and y_pt >= 3 and y_pt <= 4:
    report_ra = "Moderate-to-High Risk"
elif x_pt == 3 and y_pt >= 2 and y_pt <= 3:
    report_ra = "Moderate-to-High Risk"
elif x_pt == 4 and y_pt >= 1 and y_pt <= 2:
    report_ra = "Moderate-to-High Risk"

elif x_pt <= 4 and x_pt >= 3 and y_pt == 4:
    report_ra = "High-to-Very High Risk"
elif x_pt <= 5 and x_pt >= 4 and y_pt == 3:
    report_ra = "High-to-Very High Risk"

elif x_pt == 3 and y_pt >= 4 and y_pt <= 5:
    report_ra = "High-to-Very High Risk"
elif x_pt == 4 and y_pt >= 3 and y_pt <= 4:
    report_ra = "High-to-Very High Risk"
else:
    report_ra = report_ra


# Normalized score is based on rounding to the nearest whole number
x_pt_norm = round(x_pt,0)
y_pt_norm = round(y_pt,0)

# Not used in plot
# x_user_norm = [x_pt_norm]
# y_user_norm = [y_pt_norm]


# Determine the Impact category
if x_pt_norm == 5:
    report_impact = "Very High"
elif x_pt_norm == 4:
    report_impact = "High"
elif x_pt_norm == 3:
    report_impact = "Medium"
elif x_pt_norm == 2:
    report_impact = "Low"
else:
    report_impact = "Very Low"

    
# Determine the Likelihood category
if y_pt_norm == 5:
    report_likelihood = "Highly Likely"
elif y_pt_norm == 4:
    report_likelihood = "Likely"
elif y_pt_norm == 3:
    report_likelihood = "Possible"
elif y_pt_norm == 2:
    report_likelihood = "Unlikely"
else:
    report_likelihood = "Rare"


# DESCRIPTION
header = st.container()
with header:
    st.title('MAZARS ESG Risk Assessment Tool - Company Evaluation Form')
    st.markdown('This form collects data to assess your company’s sustainability risk exposure under the Environmental Pillar of ESG, aligned with ESRS (E1–E5). Please provide honest, current responses. The final report will benchmark your risks across Climate Change, Pollution, Water & Marine Resources, Biodiversity, and Circular Economy using a standardized 5x5 risk matrix and traffic light scoring.')
    st.markdown('Please follow the link to the MAZARS ESG Risk Questionnaire for more information: \
    [MAZARS ESG Risk Questionnaire](https://www.mazars.com/Home/Insights/ESG-Reporting/ESG-Risk-Questionnaire)')
    st.markdown('Next, please answer the questions in the sidebar by selecting options and sliding the bar to the appropriate \
    position. There are two sections to complete. If a question does not apply to your practice, answer "N/A".')
    st.markdown('The risk assessment score is calculated by dividing the sum of each section by the number \
    of questions answered. The raw score is then plotted.')

    # st.markdown('Email baglen@tcd.ie for any feedback or inquiries.')
    st.divider()

# Load the "ESRS 1 - Climate Change" sheet from the Excel file
excel_path = "Company Project Tool.xlsx"  # Update the filename if needed
df_esrs1 = pd.read_excel(excel_path, sheet_name="ESRS 1 - Climate Change")

# Example: Display the dataframe in Streamlit
st.header("ESRS 1 Data")
st.dataframe(df_esrs1)

# SET DEFAULT APPEARANCE OF MATRIX PLOT
fig, ax = plt.subplots()
ax.set_xlabel('Impact')
ax.set_ylabel('Likelihood')
plt.xlim([1,5])
plt.ylim([1,5])
plt.xticks([0,1,2,3,4,5])
plt.yticks([0,1,2,3,4,5])
plt.grid(linestyle='--', linewidth=0.5)

# SET BASE VALUES AS PER TABLE B-1 RISK ASSESSMENT MATRIX
x = np.array([0,1,1,2,2,3,3,4,4,5])
y_low = np.array([3,3,2,2,1,1,0,0,0,0])
y_mod = np.array([5,5,4,4,3,3,2,2,1,1])
y_high = np.array([5,5,5,5,5,5,4,4,3,3])
y_vhigh = np.array([5,5,5,5,5,5,5,5,5,5])

if x_pt >= 3:
    x_text_offset = -45
else:
    x_text_offset = 45

if y_pt >= 3:
    y_text_offset = -45
else:
    y_text_offset = 45


# PLOTTING
ax.set_title('5X5 RISK MATRIX PLOT')
ax.plot(x_user, y_user, color='black', marker='o', markersize=8)
# Removed normalized score from being plotted
# ax.plot(x_user_norm, y_user_norm, marker='s', color='blue', markersize=8, markerfacecolor='none', markeredgecolor='blue')
ax.annotate(
    'Risk Score', 
    xy=(x_pt,y_pt), xycoords='data', 
    xytext=(x_pt + x_text_offset, y_pt + y_text_offset), textcoords='offset points', 
    arrowprops=dict(arrowstyle='->',
                    connectionstyle='arc3, rad=.2'))
ax.stackplot(x, y_vhigh, color='red')
ax.stackplot(x, y_high, color='orange')
ax.stackplot(x, y_mod, color='yellow')
ax.stackplot(x, y_low, color='green')

red_patch = mpatches.Patch(color='red', label='Very High')
orange_patch = mpatches.Patch(color='orange', label='High')
yellow_patch = mpatches.Patch(color='yellow', label='Moderate')
green_patch = mpatches.Patch(color='green', label='Low')
black_circle = mlines.Line2D([], [], marker='o', color='pink', markersize=8, linestyle='None', label='Risk Score')
# Removed normalized score from being plotted
# blue_square = mlines.Line2D([], [], marker='s', color='blue', markersize=8, 
#                            markerfacecolor='none', markeredgecolor='blue', 
#                            linestyle='None', label='Normalized Score')
plt.legend(handles=[red_patch, orange_patch, yellow_patch, green_patch, black_circle], bbox_to_anchor=(1.05,1), loc=2, borderaxespad=0.)
my_fig = plt.show()


# TEXT OUTPUT
# Reporting for Impact and Likelihood represent the whole number values
# Reporting for the Risk Assessment Category is based on the decimal values
# If the Category is on the border, it is assessed as Category1-to-Category2
st.pyplot(fig)
st.markdown(f"Likelihood = **{round(x_pt,1)}** or **{report_impact}**")
st.markdown(f"Impact = **{round(y_pt,1)}** or **{report_likelihood}**")
st.markdown(f"The Risk Assessment score is **({int(x_pt_norm)}, {int(y_pt_norm)})** or **{report_ra}**")


# DESCRIPTION
header = st.container()
with header:
    
    # st.markdown('Email baglen@tcd.ie for any feedback or inquiries.')
    st.divider()
