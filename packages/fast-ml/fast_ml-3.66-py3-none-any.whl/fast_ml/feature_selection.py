import pandas as pd
import numpy as np
from sklearn.metrics import *




def get_constant_features(df, threshold=0.99, dropna=False):
    constant_feats = []

    for var in df.columns:
        s = df[var].value_counts(normalize=True, dropna=dropna)
        if s.iloc[0]>=threshold:
            constant_feats.append(var)
    
    return constant_feats

def get_duplicate_features (df):
    
    duplicate_features_ = []
    duplicate_pairs_ = {}

    for i,v1 in enumerate(df.columns,0):
        duplicate_feat = []
        if v1 not in duplicate_features_:
            for v2 in df.columns[i+1:]:
                if df[v1].equals(df[v2]):
                    duplicate_features_.append(v2)
                    duplicate_feat.append(v2)
            if duplicate_feat:
                duplicate_pairs_[v1] = duplicate_feat
                
    return duplicate_features_

def get_duplicate_pairs (df):
    '''
    To get list of duplicate features from this dictionary run this command
    [item for sub_list in list(duplicate_pairs_.values()) for item in sub_list]
    
    '''
    duplicate_features_ = []
    duplicate_pairs_ = {}

    for i,v1 in enumerate(df.columns,0):
        duplicate_feat = []
        if v1 not in duplicate_features_:
            for v2 in df.columns[i+1:]:
                if df[v1].equals(df[v2]):
                    duplicate_features_.append(v2)
                    duplicate_feat.append(v2)
            if duplicate_feat:
                duplicate_pairs_[v1] = duplicate_feat
                
    return duplicate_pairs_

def get_correlated_pairs(df, threshold=0.9):
    
    df_corr = df.corr()
    df_corr = pd.DataFrame(df_corr.unstack())
    df_corr = df_corr.reset_index()
    df_corr.columns = ['feature1', 'feature2', 'corr']
    df_corr['abs_corr'] = df_corr['corr'].abs()

    #print('original corr dataframe Shape', df_corr.shape)

    # Removing correlation below the threshold
    df_corr = df_corr.query(f'abs_corr >= {threshold}')

    # Removing correlations within the same features
    df_corr = df_corr[~(df_corr['feature1']==df_corr['feature2'])]

    # Removing cases where first v1 was compared with v2 and then later v2 compared with v1
    for v1 in df_corr['feature1'].unique():
        for v2 in df_corr['feature2'].unique():
            drop_ix = df_corr[(df_corr['feature1']==v2) & (df_corr['feature2'] == v1)].index
            df_corr.drop(index=drop_ix, inplace=True)

    # Creating correlation groups        
    df_corr['corr_group'] = (df_corr.groupby(by='feature1').cumcount()==0).astype('int')
    df_corr['corr_group'] = df_corr['corr_group'].cumsum()

    # Formating changes
    df_corr.sort_values(by='corr_group', inplace=True)
    df_corr.reset_index(drop=True, inplace=True)
    df_corr = df_corr[[ 'corr_group', 'feature1', 'feature2', 'corr', 'abs_corr']]
    #print('Final corr dataframe Shape', df_corr.shape)
    
    return df_corr

def recursive_feature_elimination(model, X_train, y_train, X_valid, y_valid):
    rfe_df = pd.DataFrame(columns = ['dropped_feature', 'num_features', 'train_roc', 'valid_roc'])
    features_to_drop = []

    for i in range(0, len(X_train.columns)):
        X_train_c = X_train.copy()
        X_valid_c = X_valid.copy()

        X_train_c = X_train_c.drop(columns = features_to_drop)
        X_valid_c = X_valid_c.drop(columns = features_to_drop)

        #model = RandomForestClassifier(n_estimators=50, max_depth=4, random_state=SEED)
        model.fit(X_train_c, y_train)
        #print(model)

        #train
        y_train_pred = model.predict_proba(X_train_c)[:,1]
        train_roc = roc_auc_score(y_train, y_train_pred)
        #print('Train ROC Score:', train_roc)

        #test
        y_valid_pred = model.predict_proba(X_valid_c)[:,1]
        valid_roc = roc_auc_score(y_valid, y_valid_pred)
        #print('Test ROC Score:', test_roc)

        data = {'feature': X_train_c.columns, 'fi': model.feature_importances_}
        fi = pd.DataFrame(data)
        fi.sort_values(by = 'fi', ascending=False, inplace=True)

        lowest_fi = list(fi['feature'])[-1]
        features_to_drop.append(lowest_fi)

        if i ==0:
            drop_f = 'None'
        else:
            drop_f = features_to_drop[-1]

        rfe_df.loc[i] = [drop_f, len(X_train_c.columns), train_roc, valid_roc]

    print('Done')
    rfe_df['train_roc_rank'] =rfe_df['train_roc'].rank(method='min', ascending=False).astype('int')
    rfe_df['valid_roc_rank'] =rfe_df['valid_roc'].rank(method='min', ascending=False).astype('int')
    
    return rfe_df

def variables_clustering (df, variables, method):
    """
    This function helps in performing the variable clustering.
    
    'spearman': This evaluates the monotonic relationship between two continuous or ordinal variables.
    'pearson': This evaluates the linear relationship between two continuous variables.

    
    Parameter:
    ----------
    df : dataframe
        Dataframe for analysis
    variables : list type, optional
        List of all the variables for which clustering needs to be done. If not provided it will automatically select all the numerical analysis
    method : str, default 'spearman'
        'pearson' : For pearson correlation
        'spearman' : For spearman correlation
        
    Returns:
    --------
    Dendogram with hierarchial clustering for variables
    """

    cluster_df = df[variables]
    
    if method in ("Pearson", "pearson"):
        corr = cluster_df.corr(method='pearson')
        title = "Pearson Correlation"
        
    elif method in ("Spearman", "spearman"):
        corr = cluster_df.corr(method='spearman')
        #corr = spearmanr(cluster_df).correlation
        title = "Spearman Correlation"
        
    fig  = plt.figure(figsize=(16, int(len(variables)/2)))
    ax = fig.add_subplot(111)
    corr_linkage = hierarchy.ward(corr)
    dendro = hierarchy.dendrogram(corr_linkage, labels=variables, leaf_rotation=360, orientation ='left', ax = ax)
    dendro_idx = np.arange(0, len(dendro['ivl']))
    plt.title(title + ' - Hierarchial Clustering Dendrogram', fontsize = 17)
    ax.tick_params(axis='y', which='major', labelsize=10)
    plt.show()