import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import axes3d
import seaborn as sns
import numpy as np
import pandas as pd
import copy
import itertools
            
    
def plot_main(ga2m, X, column_names=None):
    num_use = len(ga2m.use_main_features)
    if num_use < 3:
        num_col = num_use
    else:
        num_col = 3
    num_row = int((num_use + 2) / 3)

    width = num_col * 4
    height = num_row * 3
    fig, axs = plt.subplots(nrows=num_row, ncols=num_col, figsize=(width, height))
    axs = axs.reshape(-1)

    for p, i in enumerate(ga2m.use_main_features):
        max_x = np.max(X[:, i])
        min_x = np.min(X[:, i])
        x = np.linspace(start=min_x, stop=max_x)
        a = ga2m.main_model_dict[i].predict(x.reshape(-1, 1), num_iteration=ga2m.main_model_dict[i].best_iteration)

        if type(column_names) != type(None):
            axs[p].set_title(column_names[i])
        else:
            axs[p].set_title(i)
        axs[p].set_xlabel(r'$x_{}$'.format(i), fontsize=12)
        axs[p].set_ylabel(r'$f_{}(x_{})$'.format(i, i), fontsize=12)
        sns.lineplot(x=x, y=a, ax=axs[p])

    plt.tight_layout()
    plt.show()

    
    
def plot_interaction(ga2m,X,mode = '3d'):
    if mode == '3d':
        plot_interaction_3d(ga2m,X)
        
    else:
        num_use = len(ga2m.use_interaction_features)
        if num_use < 3:
            num_col = num_use
        else:
            num_col = 3
        num_row = int((num_use+2)/3)

        width = num_col * 4
        hight = num_row * 3
        fig, axs = plt.subplots(nrows=num_row,ncols=num_col,figsize=(width,hight))
        axs = axs.reshape(-1)

        for p,(i,j) in enumerate(ga2m.use_interaction_features):
            #カテゴリカルと離散数値の場合はあとで対処
            max_x0 = np.max(X[:,i])
            min_x0 = np.min(X[:,i])
            max_x1 = np.max(X[:,j])
            min_x1 = np.min(X[:,j])
            x0 = np.linspace(start=min_x0,stop=max_x0)
            x1 = np.linspace(start=min_x1,stop=max_x1)

            a,b =np.meshgrid(x0,x1)
            x =np.hstack((a.reshape(-1,1),b.reshape(-1,1)))
            preds = ga2m.interaction_model_dict[(i,j)].predict(x.reshape(-1,2),num_iteration=ga2m.interaction_model_dict[(i,j)].best_iteration)


            cp = axs[p].contourf(a, b, preds.reshape(a.shape))
            plt.colorbar(cp,ax=axs[p])

            axs[p].set_title(r'$f_{0}._{1}(x_{0},x_{1})$'.format(i,j))
            axs[p].set_xlabel(r'$x_{}$'.format(i))
            axs[p].set_ylabel(r'$x_{}$'.format(j))
        plt.tight_layout()
        plt.show()

    
    
def show_importance(ga2m,after_prune=True,higher_mode=False):
    # 重要度(←これはおまけ)
    if after_prune:
        tmp_dict = copy.deepcopy(ga2m.after_feature_importance_)
    else:
        tmp_dict = copy.deepcopy(ga2m.before_feature_importance_)

    if higher_mode == False:
        del tmp_dict['higher']

    impact_df = pd.DataFrame(tmp_dict.values(),
                             index=[str(a) for a in tmp_dict.keys()],
                             columns=['IMPORTANCE'])
    sns.barplot(data=impact_df.T, orient='h')
    plt.title('IMPORTANCE')
    plt.show()


def plot_interaction_3d(ga2m,X):
    num_use = len(ga2m.use_interaction_features)
    if num_use < 3:
        num_col = num_use
    else:
        num_col = 3
    num_row = int((num_use+2)/3)
    # print(num_col, num_row)
    width = num_col * 4
    hight = num_row * 3
    fig = plt.figure(figsize=(width,hight))

    for p,(i,j) in enumerate(ga2m.use_interaction_features):
        #カテゴリカルと離散数値の場合はあとで対処
        axs = fig.add_subplot(num_row, num_col, p+1, projection='3d')
        max_x0 = np.max(X[:,i])
        min_x0 = np.min(X[:,i])
        max_x1 = np.max(X[:,j])
        min_x1 = np.min(X[:,j])
        x0 = np.linspace(start=min_x0,stop=max_x0)
        x1 = np.linspace(start=min_x1,stop=max_x1)

        a,b =np.meshgrid(x0,x1)
        x =np.hstack((a.reshape(-1,1),b.reshape(-1,1)))
        preds = ga2m.interaction_model_dict[(i,j)].predict(x.reshape(-1,2),num_iteration=ga2m.interaction_model_dict[(i,j)].best_iteration)


        cp = axs.plot_surface(a, b, preds.reshape(a.shape), rstride=1, cstride=1, cmap=cm.coolwarm)
        #plt.colorbar(cp,ax=axs)

        axs.set_title(r'$f_{0}._{1}(x_{0},x_{1})$'.format(i,j))
        axs.set_xlabel(r'$x_{}$'.format(i))
        axs.set_ylabel(r'$x_{}$'.format(j))
    plt.tight_layout()
    plt.show()

    
"""
# カテゴリ変数のプロット
def plot_cat(ga2m, X, column_names = None, categorical_features=[]):
    categorical_features = list(set(ga2m.use_main_features)&set(categorical_features))
    num_cat = len(categorical_features)
    if num_cat < 3:
        num_col = num_cat
    else:
        num_col = 3
    num_row = int((num_cat+2)/3)
    
    width = num_col * 4
    height = num_row * 3
    fig, axs = plt.subplots(nrows = num_row, ncols = num_col, figsize=(width, height))
    axs = axs.reshape(-1)
    
    for p, i in enumerate(categorical_features):
        n_unique = np.unique(X[:,i])
        a = ga2m.main_model_dict[i].predict(n_unique.reshape(-1,1))
        if type(column_names) != type(None):
            axs[p].set_title(column_names[i])
        else:
            axs[p].set_title(i)
        axs[p].set_xlabel(r"$x_{}$".format(i), fontsize=12)
        axs[p].set_ylabel(r"$f(x_{})$".format(i), fontsize=12)
        axs[p].bar(n_unique, a)
        
    plt.tight_layout()
    plt.show()

    
# カテゴリ変数×カテゴリ変数のプロット
def plot_cat_interaction(ga2m, X, column_names = None, categorical_features=[]):
    categorical_features = list(set(ga2m.use_main_features)&set(categorical_features))
    categorical_features = sorted(categorical_features)
    combinations = list(itertools.combinations(categorical_features,2))
    categorical_features = list(set(ga2m.use_interaction_features)&set(combinations))    
    
    num_cat = len(categorical_features)
    if num_cat < 3:
        num_col = num_cat
    else:
        num_col = 3
    num_row = int((num_cat+2)/3)
    
    width = num_col * 4
    height = num_row * 3
    fig, axs = plt.subplots(nrows=num_row, ncols=num_col, figsize=(width, height))
    if num_cat > 1:
        axs = axs.reshape(-1)

    for p, (i,j) in enumerate(categorical_features):
        x0 = np.unique(X[:,i])
        x1 = np.unique(X[:,j])
        a,b =np.meshgrid(x0,x1)
        x =np.hstack((b.reshape(-1,1),a.reshape(-1,1)))
        preds = ga2m.interaction_model_dict[(i,j)].predict(x.reshape(-1,2),num_iteration=ga2m.interaction_model_dict[(i,j)].best_iteration)
        preds = preds.reshape(-1,1)
        data = np.hstack((x,preds))
        data = pd.DataFrame(data, columns = ["a", "b", "c"])
        data = data.pivot("a", "b", "c")
        if num_cat > 1:
            sns.heatmap(data, annot=False, linewidths = 0.7, ax = axs[p])
            axs[p].set_title(r'$f_{0}._{1}(x_{0},x_{1})$'.format(i,j))
            axs[p].set_xlabel(r'$x_{}$'.format(i))
            axs[p].set_ylabel(r'$x_{}$'.format(j))
        else:
            sns.heatmap(data, annot=False, linewidths = 0.7, ax = axs)
            axs.set_title(r'$f_{0}._{1}(x_{0},x_{1})$'.format(i,j))
            axs.set_xlabel(r'$x_{}$'.format(i))
            axs.set_ylabel(r'$x_{}$'.format(j))
    plt.tight_layout()
    plt.show()


# 連続変数×カテゴリ変数のプロット
def plot_catcon_interaction(ga2m, X, column_names = None, categorical_features=[]):
    ## モデル内で使用されているカテゴリ変数、連続変数を抽出
    categorical_features = sorted(list(set(ga2m.use_main_features)&set(categorical_features)))
    continuous_features = sorted(list(set(ga2m.use_main_features)^set(categorical_features)))
    
    ## カテゴリ変数、連続変数の組み合わせ
    cat_combinations = list(itertools.combinations(categorical_features, 2))
    con_combinations = list(itertools.combinations(continuous_features, 2))
    ## モデル内で使用されているカテゴリ変数、連続変数の組み合わせを抽出
    cat_combinations = list(set(ga2m.use_interaction_features)&set(cat_combinations))
    con_combinations = list(set(ga2m.use_interaction_features)&set(con_combinations))
    cat_con_combinations = list(set(cat_combinations)|set(con_combinations))
    ## モデル内で使用されているカテゴリ変数×連続変数の組み合わせを抽出
    catcon_combinations = list(set(ga2m.use_interaction_features)-set(cat_con_combinations))
    
    num_cat = len(catcon_combinations)
    if num_cat < 2:
        num_col = num_cat
    else:
        num_col = 2
    num_row = int((num_cat+1)/2)
    
    width = num_col * 6
    height = num_row * 4
    fig, axs = plt.subplots(nrows=num_row, ncols=num_col, figsize=(width, height))
    axs = axs.reshape(-1)
    
    for p, (i,j) in enumerate(catcon_combinations):
        cat_unique = sorted(list((np.unique(X[:,j]))))
        for u in cat_unique:
            x = np.empty((1000, 2))
            x[:,0] = np.linspace(X[:,i].min(), X[:,i].max(), 1000)
            x[:,1] = u
            preds =ga2m.interaction_model_dict[(i,j)].predict(x.reshape(-1,2),num_iteration=ga2m.interaction_model_dict[(i,j)].best_iteration)
            axs[p].plot(x[:,0], preds, label=r"$x_{0}$={1}".format(j,u), linewidth=0.7)
        
        axs[p].legend(loc="best",fontsize=8)
        axs[p].set_title(r'$f_{0}._{1}(x_{0},x_{1})$'.format(i,j))
        axs[p].set_xlabel(r'$x_{}$'.format(i))
        axs[p].set_ylabel(r'$f_{0}._{1}(x_{0},x_{1})$'.format(i,j))
    plt.tight_layout()
    plt.show()

"""