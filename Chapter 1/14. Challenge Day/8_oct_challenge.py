import streamlit as st
from PIL import Image
import pandas as pd
logo = Image.open("logo.png")
st.sidebar.image(logo, width=100)
st.sidebar.header("Justice League")
st.sidebar.text("Hari Kishore Reddy Konda &\n Dan Adrian Dobre ")
st.title("Body Mass Index Study")

st.subheader("Total number of Overweight Men and Women")
img = Image.open("_total_no_men_women_overweight.png")
st.image(img, caption="From the above graph we can observe that 32 men and 36 women are overweight")

st.subheader("Overall BMI distribution")
img = Image.open("weight_height_by_bmi.png")
st.image(img, caption="X axis=50-160 Kg - Y axis=140-200 CM - Overall BMI values distributed according to weight and height")

st.subheader("Overall BMI distribution Vs The Mean")
img = Image.open("weight_height_by_bmi_PLUS_THE_MEAN.png")
st.image(img, caption="X axis=50-160 Kg- Y axis=140-200 CM - Weight and Height Average of the Group coincides with BMI of 4")

st.subheader("Overall BMI distribution for Men")
img = Image.open("weight_height_by_bmi_men_only.png")
st.image(img)

st.subheader("Overall BMI distribution for Women")
img = Image.open("weight_height_by_bmi_women_only.png")
st.image(img, caption="X axis=50-160 Kg- Y axis=140-200 CM - Underweight people of both genders represent a small percentage of the group, while the majority is represented by the BMI of 3 or above")

st.subheader("Men Height")
img = Image.open("men_height.png")
st.image(img, caption="The X axis represents the height in CM, while the Y axis represents the number of people of that height")

st.subheader("Women Height")
img = Image.open("women_height.png")
st.image(img, caption="Overall distribution is simetric, with a noticeable difference in min and max heights of men")

# st.subheader("Men Weight")
# img = Image.open("men_weight.png")
# st.image(img, caption="The X axis represents the weight in Kg ranging from 50 to 160 Kg, while the Y axis represents the number of people of that weight")

# st.subheader("Women Weight")
# img = Image.open("women_weight.png")
# st.image(img, caption="The percentage of women overweight is higher than the men")

st.subheader("Number of extremely underweight persons Male/Female")
img = Image.open("_bmi_0.png")
st.image(img, caption="On the graph we can observe that 6 men and 7 women are in this caterogy")

st.subheader("Number of extremely overweight persons Male/Female")
img = Image.open("_bmi_5.png")
st.image(img, caption="On the graph we can observe that 105 men and 93 women are in this caterogy")

st.subheader("Average Height and Weight with Respect to the Body Mass Index")
img = Image.open("mean_values_of_weight_and_height.png")
st.image(img)

st.subheader("Overall Male BMI Distribution")
img = Image.open("overall_male_bmi.png")
st.image(img)

st.subheader("Overall Female BMI Distribution")
img = Image.open("overall_female_bmi.png")
st.image(img, caption="Selection Bias - For both genders the BMI distribution is very simillar and negatively skewed")