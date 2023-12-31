# FINAL ALGORITHM

from data import *
from models import *

# INITIALIZE PARAMETERS
ticker = 'amd'
window = 15
period = '5y'

# GATHER DATA
stock = GatherCandlestickData(ticker=ticker, period=period)
df1 = stock.import_data()
df2 = stock.import_compare_data()
print(df1.head())

example_retest = False
if example_retest:
    df1 = pd.read_csv(rf'{filepath}/data/example_data/df1.csv')
    df2 = pd.read_csv(rf'{filepath}/data/example_data/df2.csv')

# PREPARE DATA
prep_data = PrepareData(ticker=ticker, df1=df1, period=period)
compare = prep_data.compare_data(df2=df2)
df = prep_data.clean_data()

AnalyzeData(df=df, data_name=ticker).get_ydata_sumstats()

df = add_features(df=df, window=window)
print(df.columns)
scaled_df = PrepareData(ticker=ticker, df1=df).minmaxscalar()
scaled_df = rfe_filter(df=scaled_df, label='Target', feedback=1)
scaled_df['Target'] = scaled_df['Target'] * 2  # Convert to discrete label input
X_train, y_train, X_test, y_test = PrepareData(ticker=ticker, df1=scaled_df).xy_split(target='Target', train_len=.7)

# TRAIN AND RUN MODEL
svm_model = train_svm_model(X_train=X_train, y_train=y_train)
report = model_predict(model=svm_model, X_test=X_test, y_test=y_test)
print(f'Number of test samples: {len(y_test)}')
print(report)
