import numpy as np
import pandas as pd
# import seaborn as sns
import time
import math
# import matplotlib.pyplot as plt
import sklearn
# import pandas_profiling
from sklearn.model_selection import train_test_split,cross_val_score,RandomizedSearchCV
from statsmodels.stats.outliers_influence import variance_inflation_factor
from sklearn.ensemble import RandomForestClassifier,RandomForestRegressor,VotingClassifier,GradientBoostingClassifier,AdaBoostClassifier,BaggingClassifier,GradientBoostingRegressor,VotingRegressor
from scipy.stats import randint as sp_randint
from sklearn.decomposition import IncrementalPCA
from sklearn.metrics import accuracy_score,classification_report,confusion_matrix,f1_score,mean_squared_error,roc_auc_score,r2_score,median_absolute_error
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')
import pickle
from imblearn.over_sampling import RandomOverSampler
from sklearn.linear_model import LogisticRegression,LinearRegression,ElasticNet,Ridge
from sklearn.tree import DecisionTreeClassifier,DecisionTreeRegressor
from sklearn.neighbors import KNeighborsClassifier,KNeighborsRegressor
import xgboost  as xgb
from sklearn.naive_bayes import BernoulliNB,MultinomialNB
from multiprocessing import Pool

class Ultimate_Classification():
    def start(self): 
        
        #init to load data set
        file_type=input('is your file excel or csv-Type x or c: ')
        file_location = input('Please enter the file location : ')
        if(file_type=='c'):
            
            try:
                df=pd.read_csv(file_location)
            except :
                print('file not found')
        else:
            try:
                df=pd.read_excel(file_location)
            except :
                print('file not found')

        target_variable=input('Enter column name of target variable : ')

        #start time --to calculate overall time taken 
        start= time.perf_counter()

        #initializing all the models
        rfc=RandomForestClassifier(random_state=1)
        dt=DecisionTreeClassifier()
        knn = KNeighborsClassifier()
        xg=xgb.XGBClassifier()
        bnb=BernoulliNB()
        lr = LogisticRegression(random_state=1,fit_intercept=True)
        mnb= MultinomialNB()

        model_list = [rfc,dt,xg,lr,bnb]

        
        #removing features that are having more than 80% null values (if missing values are '?')

        for i in df.columns:
            if(df[df[i]=='?'].shape[0])>=40000:
                df.drop(i,axis=1,inplace=True)
        #columns that are reatined can be obtained from cols80
        self.t=df.shape

        # if missing values are null i.e np.Nan
        for i in df.columns:
            
            if(df[i].isnull().sum())>=40000:
                df.drop(i,axis=1,inplace=True)

        #replacing ? with np.nan
        for i in df.select_dtypes(exclude=['int64','float64']).columns:
            df[i].replace({'?':np.nan},inplace=True)

        self.t1=df.shape
        #filling nulls values

        df0=df.fillna(df.mean())
        df0=df0.fillna(method='ffill')
        df0=df0.fillna(method='bfill')
        
        #converting numerical columns to numeric (i.e if features are provided as object type where as they are actually numeric)
        for i in df0.columns:
            try:
                df0[i]=df0[i].apply(pd.to_numeric)
            except:
                continue
        

        #independent variables and dependent variable as x and y for vif
        X=df0.select_dtypes(exclude='object').drop(target_variable,axis=1)
        y=df0[target_variable]

        
        ## passing X to the function so that the multicollinearity gets removed.
            

        X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=.8)

        rfc.fit(X_train,y_train)

        y_pred_train_bvif=rfc.predict(X_train)
        y_pred_bvif=rfc.predict(X_test)

        acc_score_bvif_mean=(accuracy_score(y_test,y_pred_bvif))
        self.accu_train_meanFill=(accuracy_score(y_pred_train_bvif,y_train)*100)
        self.accu_test_meanFill=(acc_score_bvif_mean*100)

        df1=df.fillna(df.median())
        df1=df1.fillna(method='ffill')
        df1=df1.fillna(method='bfill')
        
        #converting numerical columns to numeric (i.e if features are provided as object type where as they are actually numeric)
        for i in df1.columns:
            try:
                df1[i]=df1[i].apply(pd.to_numeric)
            except:
                continue
        

        #independent variables and dependent variable as x and y for vif
        X=df1.select_dtypes(exclude='object').drop(target_variable,axis=1)
        y=df1[target_variable]

        
        ## passing X to the function so that the multicollinearity gets removed.
            

        X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=.8)

        rfc.fit(X_train,y_train)

        y_pred_train_bvif=rfc.predict(X_train)
        y_pred_bvif=rfc.predict(X_test)

        acc_score_bvif_median=(accuracy_score(y_test,y_pred_bvif))
        self.accu_train_medianFill=(accuracy_score(y_pred_train_bvif,y_train)*100)
        self.accu_test_medianFill=(acc_score_bvif_median*100)


        df2=df.fillna(value=0)
        df2=df2.fillna(method='ffill')
        df2=df2.fillna(method='bfill')
        #converting numerical columns to numeric (i.e if features are provided as object type where as they are actually numeric)
        for i in df2.columns:
            try:
                df2[i]=df2[i].apply(pd.to_numeric)
            except:
                continue
        

        #independent variables and dependent variable as x and y for vif
        X=df2.select_dtypes(exclude='object').drop(target_variable,axis=1)
        y=df2[target_variable]

        ## passing X to the function so that the multicollinearity gets removed.
            

        X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=.8)

        rfc.fit(X_train,y_train)

        y_pred_train_bvif=rfc.predict(X_train)
        y_pred_bvif=rfc.predict(X_test)

        acc_score_bvif_0=(accuracy_score(y_test,y_pred_bvif))
        self.accu_train_zeroFill=(accuracy_score(y_pred_train_bvif,y_train)*100)
        self.accu_test_zeroFill=(acc_score_bvif_0*100)
        
        if(acc_score_bvif_0>acc_score_bvif_median)&(acc_score_bvif_0>acc_score_bvif_mean):
            df=df2
            acc_score_bvif=acc_score_bvif_0
            
        elif(acc_score_bvif_median>acc_score_bvif_mean):
            df=df1
            acc_score_bvif=acc_score_bvif_median

        else:
            df=df0
            acc_score_bvif=acc_score_bvif_median


        #independent variables and dependent variable as x and y for vif
        X=df.select_dtypes(exclude='object').drop(target_variable,axis=1)
        y=df[target_variable]

        ## passing X to the function so that the multicollinearity gets removed.
            

        X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=.8)
        # removing multi collinearity using vif
        # removing collinear variables  
        self.cols_bvif=(X.shape)  

        x=X
        thresh = 5.0
        output = pd.DataFrame()
        k = x.shape[1]
        vif = [variance_inflation_factor(x.values, j) for j in range(x.shape[1])]
        for i in range(1,k):
            print("Iteration no.",i)
            a = np.argmax(vif)
            if vif[a] <= thresh :
                break
            if i == 1 :          
                output = x.drop(x.columns[a], axis = 1)
                vif = [variance_inflation_factor(output.values, j) for j in range(output.shape[1])]
            elif i > 1 :
                output = output.drop(output.columns[a],axis = 1)
                vif = [variance_inflation_factor(output.values, j) for j in range(output.shape[1])]
        X=(output)

        self.vif_columns=X.shape

        X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=.8)

        rfc.fit(X_train,y_train)
        y_pred_train_avif=rfc.predict(X_train)
        y_pred_avif=rfc.predict(X_test)
        acc_score_avif=accuracy_score(y_test,y_pred_avif)*100
        print('overall accuracy train data after VIF: ',accuracy_score(y_pred_train_avif,y_train)*100)
        print('overall accuracy test data after VIF: ',acc_score_avif)
        

        contCols=[]
        cat=df.select_dtypes(exclude=['int64','float64']).columns
        #if accuracy before vif is more than after then retain all the columns
        if(acc_score_avif+5<acc_score_bvif):
            print('Since our model is impacted highly we prefer not to consider VIF')
            contCols=df.select_dtypes(exclude='object').drop(target_variable,axis=1).columns
            X=df.drop(target_variable,axis=1)

        #if after vif accuracy is not impacted then retain columns returned from vif function
        else:
            contCols,temp=list(X.columns),list(X.columns)
            temp.extend(cat)
            X=df[temp]
            
        cols=[] #cols is final columns that have to be  retained
        cat1=[] #These categorical columns are to be treated as they have levels more than 50
        cat2=[] #These categorical columns can be taken as it is since they have less levels
        
        # level redution for categorical variables if total columns exceed 500
        dummies=pd.get_dummies(df,drop_first=True)

        if(len(dummies.columns)>500):
            desc=df.describe(include='object',exclude=['int64','float64'])
            desc=desc.reset_index()
            for i in X.select_dtypes(exclude=['int64','float64']):
                if (desc[desc['index']=='unique'][i][1]>50):
                    cat1.append(i)
                else:
                    cat2.append(i)
            print(cat1)
            print(cat2)
            #level redution to 75-80% of values or at max 50 levels
            catCol=[]
            vals=[]
            for i in cat1:
                temp=df[i].value_counts().reset_index()
                sum1=0
                for j in range(temp.shape[0]):
                    sum1+=temp.iloc[j][1]
                    if((sum1>=35000)&(sum1<=40000)&(j<50)):
                        vals.append(list(temp.nlargest(j+1,i)['index']))
                        catCol.append(i)
                        break
            count=0
            for i in catCol:
                t=df[~(df[i].isin(vals[0]))][i].unique()
                d={}
                for j in t:
                    d[j]='others'
                df[i].replace(d,inplace=True)
                count+=1
            #cols is final columns that have to be  retained
            
            cols.extend(catCol)
            cols.extend(contCols)
            cols.extend(cat2)

            df=df[cols].copy()

        self.cols=df.shape

        #categorical to numeric using get dummies
        dummies=pd.get_dummies(df,drop_first=True)
        X=dummies
        self.col_dummies=X.shape
        # random oversampling
        ros = RandomOverSampler(random_state=1)
        X_resampled, y_resampled = ros.fit_resample(X,y)

        X_train, X_test, y_train, y_test = train_test_split(X_resampled, y_resampled, train_size=.8)

        #building different models

        #logistic regression only if target variable has 2 classes
        if(len(y.unique())==2):
            lr.fit(X_train,y_train)
            y_pred_train_lr=lr.predict(X_train)
            y_pred_lr=lr.predict(X_test)
            acc_tr_lr=accuracy_score(y_pred_train_lr,y_train)*100
            acc_t_lr=accuracy_score(y_test,y_pred_lr)*100
            print('overall accuracy train data using logistic regression: ',acc_tr_lr)
            print('overall accuracy test data using logistic regression: ',acc_t_lr)


            bnb.fit(X_train,y_train)
            y_pred_train_bnb=bnb.predict(X_train)
            y_pred_bnb=bnb.predict(X_test)
            acc_tr_bnb=accuracy_score(y_pred_train_bnb,y_train)*100
            acc_t_bnb=accuracy_score(y_test,y_pred_bnb)*100
            print('overall accuracy train data using bernouli navie bayes: ',acc_tr_bnb)
            print('overall accuracy test data using bernouli navie bayes: ',acc_t_bnb)

        if(len(y.unique())>2):
            temp=list(any(df[i]<0) for i in df.select_dtypes(exclude='object').columns)
            #since multinomial navie bayes doesnt work with negative values
            if (True not in temp):
                mnb.fit(X_train,y_train)
                y_pred_train_mnb=mnb.predict(X_train)
                y_pred_mnb=mnb.predict(X_test)
                acc_tr_mnb=accuracy_score(y_pred_train_mnb,y_train)*100
                acc_t_mnb=accuracy_score(y_test,y_pred_mnb)*100
                print('overall accuracy train data using multinoial navie bayes: ',acc_tr_mnb)
                print('overall accuracy test data using multinomial navie bayes: ',acc_t_mnb)



        dt.fit(X_train,y_train)
        y_pred_train_dt=dt.predict(X_train)
        y_pred_dt=dt.predict(X_test)
        acc_tr_dt=accuracy_score(y_pred_train_dt,y_train)*100
        acc_t_dt=accuracy_score(y_test,y_pred_dt)*100
        print('overall accuracy train data using decision tree: ',acc_tr_dt)
        print('overall accuracy test data using decision tree: ',acc_t_dt)


        xg.fit(X_train,y_train)
        y_pred_train_xg=xg.predict(X_train)
        y_pred_xg=xg.predict(X_test)
        acc_tr_xg=accuracy_score(y_pred_train_xg,y_train)*100
        acc_t_xg=accuracy_score(y_test,y_pred_xg)*100
        print('overall accuracy train data using XG boost: ',acc_tr_xg)
        print('overall accuracy test data using xg boost: ',acc_t_xg)


        rfc.fit(X_train,y_train)
        y_pred_train_rfc=rfc.predict(X_train)
        y_pred_rfc=rfc.predict(X_test)
        acc_tr_rfc=accuracy_score(y_pred_train_rfc,y_train)*100
        acc_t_rfc=accuracy_score(y_test,y_pred_rfc)*100
        print('overall accuracy train data using random forest classifier: ',acc_tr_rfc)
        print('overall accuracy test data using random forest classifier: ',acc_t_rfc)

        try:
            acc_t_lr
        except NameError:
            acc_t_lr=0
        try:
            acc_t_bnb
        except NameError:
            acc_t_bnb=0
        try:
            acc_t_mnb
        except NameError:
            acc_t_mnb=0
        
        self.bestModel=''
        self.bestModelName=''
        if(acc_t_rfc>acc_t_dt)&(acc_t_rfc>acc_t_bnb)&(acc_t_rfc>acc_t_lr)&(acc_t_rfc>acc_t_xg)&(acc_t_rfc>acc_t_mnb):
            self.bestModel=rfc
            self.bestModelName='random_forest_classifier'
            y_pred_train=y_pred_train_rfc
            y_pred=y_pred_rfc
            accu_best_train=acc_tr_rfc
            accu_best_test=acc_t_rfc
        elif(acc_t_bnb>acc_t_xg)&(acc_t_bnb>acc_t_lr)&(acc_t_bnb>acc_t_dt):
            self.bestModel=bnb
            self.bestModelName='bernouli_navie_bayes'
            y_pred_train=y_pred_train_bnb
            y_pred=y_pred_bnb
            accu_best_train=acc_tr_bnb
            accu_best_test=acc_t_bnb
        elif(acc_t_xg>acc_t_dt)&(acc_t_xg>acc_t_lr)&(acc_t_xg>acc_t_mnb):
            self.bestModel=xg
            self.bestModelName='XG_boost'
            y_pred_train=y_pred_train_xg
            y_pred=y_pred_xg
            accu_best_train=acc_tr_xg
            accu_best_test=acc_t_xg
        elif(acc_t_dt>acc_t_lr)&(acc_t_dt>acc_t_mnb):
            self.bestModel=dt
            self.bestModelName='Decision_Tree'
            y_pred_train=y_pred_train_dt
            y_pred=y_pred_dt
            accu_best_train=acc_tr_dt
            accu_best_test=acc_t_dt
        elif(acc_t_lr>acc_t_mnb):
            self.bestModel=lr
            self.bestModelName='Logistic_Regression'
            y_pred_train=y_pred_train_lr
            y_pred=y_pred_lr
            accu_best_train=acc_tr_lr
            accu_best_test=acc_t_lr
        else:
            self.bestModel=mnb
            self.bestModelName='multiNomial_navieBayes'
            y_pred_train=y_pred_train_mnb
            y_pred=y_pred_mnb
            accu_best_train=acc_tr_mnb
            accu_best_test=acc_t_mnb

        print('max train and test accuracy are:',accu_best_train,accu_best_test)
        #checking if hyper parameter tuning gives us best result for our best model

        max_features=len(X.columns)

        #random forest hyper parameter tuning 
        params={'n_estimators':sp_randint(5,25),
        'criterion':['gini','entropy'],
        'max_depth':sp_randint(2,math.floor(max_features/2)),
        'min_samples_split':sp_randint(2,500),
        'min_samples_leaf':sp_randint(1,500),
        'max_features':sp_randint(2,max_features)}

        rand_search_rfc=RandomizedSearchCV(rfc,param_distributions=params,cv=3,random_state=1)

        rand_search_rfc.fit(X_train,y_train)
        rand_search_rfc.best_params_
        rfc_hyp=RandomForestClassifier(**rand_search_rfc.best_params_)
        rfc_hyp.fit(X_train,y_train)

        y_pred_train_rfc_hyp=rfc_hyp.predict(X_train)
        y_pred_rfc_hyp=rfc_hyp.predict(X_test)
        acc_tr_rfc_hyp=accuracy_score(y_pred_train_rfc_hyp,y_train)*100
        acc_t_rfc_hyp=accuracy_score(y_test,y_pred_rfc_hyp)*100

        print('train test accuracy of rfc hyper parameter tuned:',acc_tr_rfc_hyp,acc_t_rfc_hyp)

        if(acc_t_rfc_hyp>acc_t_rfc):
            rfc=rfc_hyp
            if(self.bestModel==rfc):
                self.bestModel=rfc_hyp
                best_params=rand_search_rfc.best_params_

        try:
            
            vc = VotingClassifier(estimators=[('lr',lr),('rfc',rfc),('dt',dt),('xg',xg),('bnb',bnb)],voting='soft')
            vc.fit(X_train,y_train)
        except NameError:
            vc = VotingClassifier(estimators=[('mnb',mnb),('rfc',rfc),('dt',dt),('xg',xg)],voting='soft')
            vc.fit(X_train,y_train)
        
        y_pred_train_vc=vc.predict(X_train)
        y_pred_vc=vc.predict(X_test)
        acc_tr_vc=accuracy_score(y_pred_train_vc,y_train)*100
        acc_t_vc=accuracy_score(y_test,y_pred_vc)*100
        print('overall accuracy train data using voting classifier: ',acc_tr_vc)
        print('overall accuracy test data using voting classifier: ',acc_t_vc)

        if (acc_t_vc>99.5):
            self.bestModel=vc
            y_pred_train=y_pred_train_vc
            y_pred=y_pred_vc
            accu_best_train=acc_tr_vc
            accu_best_test=acc_t_vc
        
            
        self.f1_score_train=sklearn.metrics.f1_score(y_pred_train,y_train,average='micro')
        self.f1_score_test=sklearn.metrics.f1_score(y_test,y_pred,average='micro')

        self.confusion_mat_train=sklearn.metrics.confusion_matrix(y_pred_train,y_train)
        self.confusion_mat_test=sklearn.metrics.confusion_matrix(y_test,y_pred)

        self.classification_report_train=sklearn.metrics.classification_report(y_pred_train,y_train)
        self.classification_report_test=sklearn.metrics.classification_report(y_test,y_pred)

        #self.roc_auc_score_train=sklearn.metrics.roc_auc_score(y_pred_train,y_train,multi_class='ovr')
        #self.roc_auc_score_test=sklearn.metrics.roc_auc_score(y_test,y_pred,multi_class='ovr')

        #10 fold cross validation to be more certain about our models accuracy
        self.scores_train = cross_val_score(self.bestModel, X_train, y_train, cv=10)
        self.scores_test = cross_val_score(self.bestModel, X_test, y_test , cv=10)

        end=time.perf_counter()
        print('-'*50)
        print('Best model is: ',self.bestModelName)

        print('total time taken is', ((end-start)/60),'minutes')
        print('-'*50)
        #funtion to return all the values 
    
    def f1_score(self):
        print('overall f1_score train data: ',self.f1_score_train)
        print('overall f1_score test data: ',self.f1_score_test)

    def confusion_matrix(self):
        print('confusion_matrix of train data:\n',self.confusion_mat_train)
        print('confusion_matrix of test data:\n',self.confusion_mat_test)

    def classification_report(self):
        print('classification_report of train data:\n',self.classification_report_train)
        print('classification_report of test data:\n',self.classification_report_test)

    #def roc_auc_score(self):
        #print('overall roc_auc_score train data: ',self.roc_auc_score_train)
        #print('overall roc_auc_score test data: ',self.roc_auc_score_test)

    def accuracy_medianFill(self):
        print('overall accuracy train data with medianFill: ',self.accu_train_medianFill)
        print('overall accuracy test data with medianFill: ',self.accu_test_medianFill)

    def accuracy_zeroFill(self):
        print('overall accuracy train data with zeroFill: ',self.accu_train_zeroFill)
        print('overall accuracy test data with zeroFill: ',self.accu_test_zeroFill)
    
    def accuracy_meanFill(self):
        print('overall accuracy train data with meanFill: ',self.accu_train_meanFill)
        print('overall accuracy test data with meanFill: ',self.accu_test_meanFill)

    def columns(self):
        print('columns retained after removing columns with 80% ?',self.t)
        print('columns retained after removing columns with 80% NULL',self.t1)
        print('continuous columns before vif are : ',self.cols_bvif)
        print('continuous columns retained after vif are:',self.vif_columns)
        print('Final columns that are retained are',self.cols)
        print('Final columns after doing one hot encoding are: ',self.col_dummies)
    
    def cross_validation(self):
        print("Accuracy: %0.3f (+/- %0.3f)" % (self.scores_train.mean(), self.scores_train.std() * 2))
        print("Accuracy: %0.2f (+/- %0.2f)" % (self.scores_test.mean(), self.scores_test.std() * 2))

    def runAll(self):
        self.start()
        self.accuracy_meanFill()
        self.accuracy_zeroFill()
        self.accuracy_medianFill()
        self.f1_score()
        self.confusion_matrix()
        self.classification_report()
        #self.roc_auc_score
        self.columns()
        #self.best_model()
        self.cross_validation()

class Ultimate_Regression():
    def start(self): 

        #taking file type and file location
        file_type=input('is your file excel or csv-Type x or c: ')
        file_location = input('Please enter the file location : ')
        #to load csv and excel without exceptions
        if(file_type=='c'):
            try:
                df=pd.read_csv(file_location)
            except :
                print('file not found')
        else:
            try:
                df=pd.read_excel(file_location)
            except :
                print('file not found')

        target_variable=input('Enter column name of target variable : ')

        #start time --to calculate overall time taken 
        start= time.perf_counter()

        #initializing all the models
        rfr=RandomForestRegressor(random_state=1)
        dt=DecisionTreeRegressor()
        knn = KNeighborsRegressor()
        gbr=GradientBoostingRegressor()
        en=ElasticNet()
        lr = LinearRegression()
        r=Ridge()
        

        
        #removing features that are having more than 80% null values (if missing values are '?')

        for i in df.columns:
            if(df[df[i]=='?'].shape[0])>=40000:
                df.drop(i,axis=1,inplace=True)
        #columns that are reatined can be obtained from cols80
        self.t=df.shape

        # if missing values are null i.e np.Nan
        for i in df.columns:
            if(df[i].isnull().sum())>=40000:
                df.drop(i,axis=1,inplace=True)

        #replacing ? with np.nan
        for i in df.select_dtypes(exclude=['int64','float64']).columns:
            df[i].replace({'?':np.nan},inplace=True)

        self.t1=df.shape
        #filling nulls values

        df0=df.fillna(df.mean())
        df0=df0.fillna(method='ffill')
        df0=df0.fillna(method='bfill')
        
        #converting numerical columns to numeric (i.e if features are provided as object type where as they are actually numeric)
        for i in df0.columns:
            try:
                df0[i]=df0[i].apply(pd.to_numeric)
            except:
                continue
        

        #independent variables and dependent variable as x and y for vif
        X=df0.select_dtypes(exclude='object').drop(target_variable,axis=1)
        y=df0[target_variable]

        
        ## passing X to the function so that the multicollinearity gets removed.
            

        X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=.8)

        rfr.fit(X_train,y_train)

        y_pred_train_bvif=rfr.predict(X_train)
        y_pred_bvif=rfr.predict(X_test)

        r2_score_bvif_mean=(r2_score(y_test,y_pred_bvif))
        self.r2_train_meanFill=(r2_score(y_pred_train_bvif,y_train)*100)
        self.r2_test_meanFill=(r2_score_bvif_mean*100)

        df1=df.fillna(df.median())
        df1=df1.fillna(method='ffill')
        df1=df1.fillna(method='bfill')
        
        #converting numerical columns to numeric (i.e if features are provided as object type where as they are actually numeric)
        for i in df1.columns:
            try:
                df1[i]=df1[i].apply(pd.to_numeric)
            except:
                continue
        

        #independent variables and dependent variable as x and y for vif
        X=df1.select_dtypes(exclude='object').drop(target_variable,axis=1)
        y=df1[target_variable]

        
        ## passing X to the function so that the multicollinearity gets removed.
            

        X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=.8)

        rfr.fit(X_train,y_train)

        y_pred_train_bvif=rfr.predict(X_train)
        y_pred_bvif=rfr.predict(X_test)

        r2_score_bvif_median=(r2_score(y_test,y_pred_bvif))
        self.r2_train_medianFill=(r2_score(y_pred_train_bvif,y_train)*100)
        self.r2_test_medianFill=(r2_score_bvif_median*100)


        df2=df.fillna(value=0)
        df2=df2.fillna(method='ffill')
        df2=df2.fillna(method='bfill')
        #converting numerical columns to numeric (i.e if features are provided as object type where as they are actually numeric)
        for i in df2.columns:
            try:
                df2[i]=df2[i].apply(pd.to_numeric)
            except:
                continue
        

        #independent variables and dependent variable as x and y for vif
        X=df2.select_dtypes(exclude='object').drop(target_variable,axis=1)
        y=df2[target_variable]

        ## passing X to the function so that the multicollinearity gets removed.
            

        X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=.8)

        rfr.fit(X_train,y_train)

        y_pred_train_bvif=rfr.predict(X_train)
        y_pred_bvif=rfr.predict(X_test)

        r2_score_bvif_0=(r2_score(y_test,y_pred_bvif))
        self.r2_train_zeroFill=(r2_score(y_pred_train_bvif,y_train)*100)
        self.r2_test_zeroFill=(r2_score_bvif_0*100)
        
        if(r2_score_bvif_0>r2_score_bvif_median)&(r2_score_bvif_0>r2_score_bvif_mean):
            df=df2
            r2_score_bvif=r2_score_bvif_0
            
        elif(r2_score_bvif_median>r2_score_bvif_mean):
            df=df1
            r2_score_bvif=r2_score_bvif_median

        else:
            df=df0
            r2_score_bvif=r2_score_bvif_median


        #independent variables and dependent variable as x and y for vif
        X=df.select_dtypes(exclude='object').drop(target_variable,axis=1)
        y=df[target_variable]

        ## passing X to the function so that the multicollinearity gets removed.
            

        X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=.8)
        # removing multi collinearity using vif
        # removing collinear variables  
        self.cols_bvif=(X.shape)  

        x=X
        thresh = 5.0
        output = pd.DataFrame()
        k = x.shape[1]
        vif = [variance_inflation_factor(x.values, j) for j in range(x.shape[1])]
        for i in range(1,k):
            print("Iteration no.",i)
            a = np.argmax(vif)
            if vif[a] <= thresh :
                break
            if i == 1 :          
                output = x.drop(x.columns[a], axis = 1)
                vif = [variance_inflation_factor(output.values, j) for j in range(output.shape[1])]
            elif i > 1 :
                output = output.drop(output.columns[a],axis = 1)
                vif = [variance_inflation_factor(output.values, j) for j in range(output.shape[1])]
        X=(output)

        self.vif_columns=X.shape

        X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=.8)

        rfr.fit(X_train,y_train)
        y_pred_train_avif=rfr.predict(X_train)
        y_pred_avif=rfr.predict(X_test)
        r2_score_avif=r2_score(y_test,y_pred_avif)*100
        print('overall r2 train data after VIF: ',r2_score(y_pred_train_avif,y_train)*100)
        print('overall r2 test data after VIF: ',r2_score_avif)
        

        contCols=[]
        cat=df.select_dtypes(exclude=['int64','float64']).columns
        #if r2 before vif is more than after then retain all the columns
        if(r2_score_avif+5<r2_score_bvif):
            print('Since our model is impacted highly we prefer not to consider VIF')
            contCols=df.select_dtypes(exclude='object').drop(target_variable,axis=1).columns
            X=df.drop(target_variable,axis=1)

        #if after vif r2 is not impacted then retain columns returned from vif function
        else:
            contCols,temp=list(X.columns),list(X.columns)
            temp.extend(cat)
            X=df[temp]
            
        cols=[] #cols is final columns that have to be  retained
        cat1=[] #These categorical columns are to be treated as they have levels more than 50
        cat2=[] #These categorical columns can be taken as it is since they have less levels
        
        # level redution for categorical variables if total columns exceed 500
        dummies=pd.get_dummies(df,drop_first=True)

        if(len(dummies.columns)>500):
            desc=df.describe(include='object',exclude=['int64','float64'])
            desc=desc.reset_index()
            for i in X.select_dtypes(exclude=['int64','float64']):
                if (desc[desc['index']=='unique'][i][1]>50):
                    cat1.append(i)
                else:
                    cat2.append(i)
            print(cat1)
            print(cat2)
            #level redution to 75-80% of values or at max 50 levels
            catCol=[]
            vals=[]
            for i in cat1:
                temp=df[i].value_counts().reset_index()
                sum1=0
                for j in range(temp.shape[0]):
                    sum1+=temp.iloc[j][1]
                    if((sum1>=35000)&(sum1<=40000)&(j<50)):
                        vals.append(list(temp.nlargest(j+1,i)['index']))
                        catCol.append(i)
                        break
            count=0
            for i in catCol:
                t=df[~(df[i].isin(vals[0]))][i].unique()
                d={}
                for j in t:
                    d[j]='others'
                df[i].replace(d,inplace=True)
                count+=1
            #cols is final columns that have to be  retained
            
            cols.extend(catCol)
            cols.extend(contCols)
            cols.extend(cat2)

            df=df[cols].copy()

        self.cols=df.shape

        #categorical to numeric using get dummies
        dummies=pd.get_dummies(df,drop_first=True)
        X=dummies

        self.col_dummies=X.shape

        X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=.8)

        #building different models

        
        lr.fit(X_train,y_train)
        y_pred_train_lr=lr.predict(X_train)
        y_pred_lr=lr.predict(X_test)
        r2_tr_lr=r2_score(y_pred_train_lr,y_train)*100
        r2_t_lr=r2_score(y_test,y_pred_lr)*100
        print('overall r2 train data using linear regression: ',r2_tr_lr)
        print('overall r2 test data using linear regression: ',r2_t_lr)


        en.fit(X_train,y_train)
        y_pred_train_en=en.predict(X_train)
        y_pred_en=en.predict(X_test)
        r2_tr_en=r2_score(y_pred_train_en,y_train)*100
        r2_t_en=r2_score(y_test,y_pred_en)*100
        print('overall r2 train data using ElasticNetnavie bayes: ',r2_tr_en)
        print('overall r2 test data using ElasticNetnavie bayes: ',r2_t_en)
        


        dt.fit(X_train,y_train)
        y_pred_train_dt=dt.predict(X_train)
        y_pred_dt=dt.predict(X_test)
        r2_tr_dt=r2_score(y_pred_train_dt,y_train)*100
        r2_t_dt=r2_score(y_test,y_pred_dt)*100
        print('overall r2 train data using decision tree: ',r2_tr_dt)
        print('overall r2 test data using decision tree: ',r2_t_dt)


        gbr.fit(X_train,y_train)
        y_pred_train_gbr=gbr.predict(X_train)
        y_pred_gbr=gbr.predict(X_test)
        r2_tr_gbr=r2_score(y_pred_train_gbr,y_train)*100
        r2_t_gbr=r2_score(y_test,y_pred_gbr)*100
        print('overall r2 train data using gbr boost: ',r2_tr_gbr)
        print('overall r2 test data using gbr boost: ',r2_t_gbr)


        rfr.fit(X_train,y_train)
        y_pred_train_rfr=rfr.predict(X_train)
        y_pred_rfr=rfr.predict(X_test)
        r2_tr_rfr=r2_score(y_pred_train_rfr,y_train)*100
        r2_t_rfr=r2_score(y_test,y_pred_rfr)*100
        print('overall r2 train data using random forest regressor: ',r2_tr_rfr)
        print('overall r2 test data using random forest regressor: ',r2_t_rfr)

        
        r.fit(X_train,y_train)
        y_pred_train_r=r.predict(X_train)
        y_pred_r=r.predict(X_test)
        r2_tr_r=r2_score(y_pred_train_r,y_train)*100
        r2_t_r=r2_score(y_test,y_pred_r)*100
        print('overall r2 train data using ridge regressor: ',r2_tr_r)
        print('overall r2 test data using ridge regressor: ',r2_t_r)

        self.bestModel=''
        self.bestModelName=''
        l={'rfr':r2_t_rfr,'dt':r2_t_dt,'en':r2_t_en,'lr':r2_t_lr,'gbr':r2_t_gbr,'r':r2_t_r}
        max_model=[k for k,v in l.items() if v==max(l.values())]
        if max_model[0]=='rfr':
            self.bestModel=rfr
            self.bestModelName='random_forest_regressor'
            y_pred_train=y_pred_train_rfr
            y_pred=y_pred_rfr
            r2_best_train=r2_tr_rfr
            r2_best_test=r2_t_rfr
        elif max_model[0]=='en':
            self.bestModel=en
            self.bestModelName='elasticNet'
            y_pred_train=y_pred_train_en
            y_pred=y_pred_en
            r2_best_train=r2_tr_en
            r2_best_test=r2_t_en
        elif max_model[0]=='gbr':
            self.bestModel=gbr
            self.bestModelName='gradient_boosting_regression'
            y_pred_train=y_pred_train_gbr
            y_pred=y_pred_gbr
            r2_best_train=r2_tr_gbr
            r2_best_test=r2_t_gbr
        elif max_model[0]=='dt':
            self.bestModel=dt
            self.bestModelName='decision_tree'
            y_pred_train=y_pred_train_dt
            y_pred=y_pred_dt
            r2_best_train=r2_tr_dt
            r2_best_test=r2_t_dt
        elif max_model[0]=='lr':
            self.bestModel=lr
            self.bestModelName='linear_regression'
            y_pred_train=y_pred_train_lr
            y_pred=y_pred_lr
            r2_best_train=r2_tr_lr
            r2_best_test=r2_t_lr
        
        else:
            self.bestModel=r
            self.bestModelName='ridge'
            y_pred_train=y_pred_train_r
            y_pred=y_pred_r
            r2_best_train=r2_tr_r
            r2_best_test=r2_t_r

        print('max train and test r2 are:',r2_best_train,r2_best_test)
        #checking if hyper parameter tuning gives us best result for our best model

        max_features=len(X.columns)
        try:
            #random forest hyper parameter tuning 
            params={'n_estimators':sp_randint(5,25),
            'max_depth':sp_randint(2,math.floor(max_features/2)),
            'min_samples_split':sp_randint(2,500),
            'min_samples_leaf':sp_randint(1,500),
            'max_features':sp_randint(2,max_features)}

            rand_search_rfr=RandomizedSearchCV(rfr,param_distributions=params,cv=3,random_state=1)

            rand_search_rfr.fit(X_train,y_train)
            rand_search_rfr.best_params_
            rfr_hyp=RandomForestClassifier(**rand_search_rfr.best_params_)
            rfr_hyp.fit(X_train,y_train)

            y_pred_train_rfr_hyp=rfr_hyp.predict(X_train)
            y_pred_rfr_hyp=rfr_hyp.predict(X_test)
            r2_tr_rfr_hyp=r2_score(y_pred_train_rfr_hyp,y_train)*100
            r2_t_rfr_hyp=r2_score(y_test,y_pred_rfr_hyp)*100

            print('train test r2 of rfr hyper parameter tuned:',r2_tr_rfr_hyp,r2_t_rfr_hyp)

            if(r2_t_rfr_hyp>r2_t_rfr)&(r2_t_rfr_hyp<100):
                rfr=rfr_hyp
                if(self.bestModel==rfr):
                    self.bestModel=rfr_hyp
                    best_params=rand_search_rfr.best_params_
        except:
            pass
   
        vr = VotingRegressor([('lr',lr),('rfr',rfr),('dt',dt),('gbr',gbr),('en',en),('r',r)])
        vr.fit(X_train,y_train)
        
        y_pred_train_vr=vr.predict(X_train)
        y_pred_vr=vr.predict(X_test)
        r2_tr_vr=r2_score(y_pred_train_vr,y_train)*100
        r2_t_vr=r2_score(y_test,y_pred_vr)*100
        print('overall r2 train data using voting regressor: ',r2_tr_vr)
        print('overall r2 test data using voting regressor: ',r2_t_vr)

        if (r2_t_vr>99.9995):
            self.bestModel=vr
            self.bestModelName='Voting_regressor'
            y_pred_train=y_pred_train_vr
            y_pred=y_pred_vr
            r2_best_train=r2_tr_vr
            r2_best_test=r2_t_vr
        
        end=time.perf_counter()

        #cross validation
        print('Best Model is: ',self.bestModelName)

        print('total time taken is', ((end-start)/60),'minutes')

        self.mse_train=sklearn.metrics.mean_squared_error(y_pred_train,y_train)
        self.mse_test=sklearn.metrics.mean_squared_error(y_test,y_pred)

        self.mae_train=sklearn.metrics.median_absolute_error(y_pred_train,y_train)
        self.mae_test=sklearn.metrics.median_absolute_error(y_test,y_pred)

    def mse(self):
        print('mean_squared_error of train data: ',self.mse_train)
        print('mean_squared_error of test data: ',self.mse_test)

    def mae(self):
        print('Median_Absolute_error of train data: ',self.mae_train)
        print('Median_Absolute_error of test data: ',self.mae_test)

    def r2_medianFill(self):
        print('overall r2 train data with medianFill: ',self.r2_train_medianFill)
        print('overall r2 test data with medianFill: ',self.r2_test_medianFill)

    def r2_zeroFill(self):
        print('overall r2 train data with zeroFill: ',self.r2_train_zeroFill)
        print('overall r2 test data with zeroFill: ',self.r2_test_zeroFill)
    
    def r2_meanFill(self):
        print('overall r2 train data with meanFill: ',self.r2_train_meanFill)
        print('overall r2 test data with meanFill: ',self.r2_test_meanFill)

    def columns(self):
        print('columns retained after removing columns with 80% ?',self.t)
        print('columns retained after removing columns with 80% NULL',self.t1)
        print('continuous columns before vif are : ',self.cols_bvif)
        print('continuous columns retained after vif are:',self.vif_columns)
        print('Final columns that are retained are',self.cols)
        print('Final columns after doing one hot encoding are: ',self.col_dummies)
        try:
            print(f'Feature Importance:',self.bestModel.feature_importances_)
        except Exception as e:
            pass

class createModel():
    def __init__(self):
        self.reg_flag=input('input y or n for reg').lower()
        if self.reg_flag.lower()=='y':
            self.ul=Ultimate_Regression()
        else:
            self.ul=Ultimate_Classification()
        self.ul.start()
    def r2_meanFill(self):
        if self.reg_flag=='y':	
            self.ul.r2_meanFill()
    def r2_zeroFill(self):
        if self.reg_flag=='y':	
            self.ul.r2_zeroFill()
    def r2_medianFill(self):
        if self.reg_flag=='y':	
            self.ul.r2_medianFill()
    def mae(self):
        if self.reg_flag=='y':	
            self.ul.mae()
    def mse(self):
        if self.reg_flag=='y':	
            self.ul.mse()
    def columns(self):
        self.ul.columns()
    def accuracy_meanFill(self):
        if self.reg_flag!='y':		
            self.ul.accuracy_meanFill()
    def accuracy_zeroFill(self):
        if self.reg_flag!='y':		
            self.ul.accuracy_zeroFill()
    def accuracy_medianFill(self):
        if self.reg_flag!='y':		
            self.ul.accuracy_medianFill()
    def f1_score(self):
        if self.reg_flag!='y':		
            self.ul.f1_score()
    def confusion_matrix(self):
        if self.reg_flag!='y':		
            self.ul.confusion_matrix()
    def classification_report(self):
        if self.reg_flag!='y':		
            self.ul.classification_report()
    def cross_validation(self):
        if self.reg_flag!='y':		
            self.ul.cross_validation()
