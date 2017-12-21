import pandas as pd
import numpy as np

#Import dataframe
raw_data = pd.read_csv(r'C:\Users\Khew Min Shiu\NS1-AAPL_US.csv')
##raw_data = pd.read_csv(r'C:\Users\Khew Min Shiu\NS1-TWTR_US.csv')

#Brief statistic on 'Sentiment' and 'Buzz'
raw_data['Sentiment'].describe()
raw_data['News Buzz'].describe()

#A brief statistic on difference of sentiment on a day
sentiment_diff = raw_data['Sentiment High'] - raw_data['Sentiment Low']
sentiment_diff.describe()

#Calculate how many positive sentiment values, how many 'Sentiment High' > 0, how many 'Sentiment High' < 0
positive = np.sum((raw_data['Sentiment'] > 0) * 1)
high = np.sum( (raw_data['Sentiment High']>0)*1 * (raw_data['Sentiment Low']>0)*1)
low = np.sum( (raw_data['Sentiment High']<0)*1 * (raw_data['Sentiment Low']<0)*1)
print('There is a total of %d positive sentiment values on news/articles/social media across the 3 months period.'%positive)
print('Besides that, %d day(s) are totally positive and %d day(s) are totally negative in sentiment values.'%(high,low))

#Calculate sum of news volume
print('The sum of news volume for Apple in US from 2017-09-20 to 2017-12-20 is %d.'%raw_data['News Volume'].sum())

#Calculate total days with 0 sentiment and buzz'
temp_df = raw_data[raw_data['Sentiment'] == 0]
print('In a total of 3 months period, there is %d day(s) which this asset has zero sentiment and buzz.'%temp_df['Date'].count())

#Build a ordinary least square model to predict sentiment
from statsmodels.formula.api import ols
Y_positive = raw_data[raw_data['Sentiment'] >= 0 ]['Sentiment']
Y_negative = raw_data[raw_data['Sentiment'] < 0 ]['Sentiment']
X_positive = raw_data[raw_data['Sentiment'] >= 0 ]['News Volume']
X_negative = raw_data[raw_data['Sentiment'] < 0 ]['News Volume']
df_positive = pd.DataFrame(data={'Y':Y_positive, 'X':X_positive}) 
model_1 = ols("Y ~ X",df_positive).fit()
print(model_1.summary())

#Negative sentiment value model
df_negative = pd.DataFrame(data={'Y':Y_negative, 'X':X_negative}) 
model_2 = ols("Y ~ X", df_negative).fit()

#SVM model (positive)
from sklearn.svm import SVC
svc = SVC(kernel = 'linear')
svc.fit(X_positive.reshape(-1,1),Y_positive.reshape(-1,1))
print(model_2.summary())

#Positive prediction
y_pred_positive = [svc.predict(70),svc.predict(50),svc.predict(0)]
y_pred_positive

#SVM model (negative)
from sklearn.svm import SVC
svc_2 = SVC(kernel = 'linear')
svc_2.fit(X_negative.reshape(-1,1),Y_negative.reshape(-1,1))

#Negative prediction
y_pred_negative = [svc_2.predict(70),svc_2.predict(50),svc_2.predict(10)]
y_pred_negative
