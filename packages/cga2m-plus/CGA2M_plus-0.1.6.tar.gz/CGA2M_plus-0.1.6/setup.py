# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['cga2m_plus', 'cga2m_plus..ipynb_checkpoints']

package_data = \
{'': ['*']}

install_requires = \
['lightgbm>=3.2.1,<4.0.0',
 'matplotlib>=3.4.2,<4.0.0',
 'numpy',
 'seaborn>=0.11.1,<0.12.0']

setup_kwargs = {
    'name': 'cga2m-plus',
    'version': '0.1.6',
    'description': 'CGA2M_plus is a Python package of Constraint GA2M plus(CGA2M+). CGA2M+ is a model that improves GA2M in two respects: interpretability and accuracy.',
    'long_description': '![](https://raw.githubusercontent.com/MK-tech20/CGA2M_plus/main/images/cga2m_plus%2B.png) \n# CGA2M+ (Constraint GA2M plus)\nWe propose Constraint GA2M plus (CGA2M+), which we proposed. CGA2M+ is a modified version of GA2M to improve its interpretability and accuracy.\nFor more information, please read our paper.(coming soon!!) \nMainly, CGA2M+ differs from GA2M in two respects.\n1. introducing monotonic constraints\n2. introducing higher-order interactions keeping the interpretability of the model\n# Description of CGA2M+\nMainly, CGA2M+ differs from GA2M in two respects. We are using LightGBM as a shape function.\n\n- **introducing monotonic constraints**  \n\nBy adding monotonicity, we can improve the interpretability of our model. For example, we can make sure that "in the real estate market, as the number of rooms increases, the price decreases" does not happen. Human knowledge is needed to determine which features to enforce monotonicity on. The monotonicity constraint algorithm is implemented in LightGBM. This is a way to constrain the branches of a tree. For more details, please refer to the LightGBM implementation.\n\n![](https://raw.githubusercontent.com/MK-tech20/CGA2M_plus/main/images/constraint.png)   \n\n- **introducing higher-order interactions keeping the interpretability of the model**  \n\nGGA2M is unable to take into account higher-order interactions. Therefore, we introduce higher-order terms that are not interpretable. However, we devise a learning method so that the higher-order terms do not compromise the overall interpretability. Specifically, we train the higher-order terms as models that predict the residuals of the univariate terms and pairwise interaction terms. This allows most of the predictions to be explained by the interpretable first and second order terms. These residuals are then predicted by a higher-order term.\n\n# Algorithm  \n![](https://raw.githubusercontent.com/MK-tech20/CGA2M_plus/main/images/algorithm.png)\nFor more information, please read our paper. (coming soon!!) \n# Installation\nYou can get CGA2M+ from PyPI. Our project in PyPI is [here](https://pypi.org/project/cga2m-plus/).\n```bash\npip install cga2m-plus\n```\n\n# Usage\nFor more detail, please read `examples/How_to_use_CGA2M+.ipynb`.\nIf it doesn\'t render at all in github, please click [here](https://kokes.github.io/nbviewer.js/viewer.html#aHR0cHM6Ly9naXRodWIuY29tL01LLXRlY2gyMC9DR0EyTV9wbHVzL2Jsb2IvbWFpbi9leGFtcGxlcy9Ib3dfdG9fdXNlX0NHQTJNJTJCLmlweW5i).\n## Training\n\n```python\ncga2m = Constraint_GA2M(X_train,\n                        y_train,\n                        X_eval,\n                        y_eval,\n                        lgbm_params,\n                        monotone_constraints = [0] * 6,\n                        all_interaction_features = list(itertools.combinations(range(X_test.shape[1]), 2)))\n\ncga2m.train(max_outer_iteration=20,backfitting_iteration=20,threshold=0.05)\ncga2m.prune_and_retrain(threshold=0.05,backfitting_iteration=30)\ncga2m.higher_order_train()\n```\n## Predict\n```python\ncga2m.predict(X_test,higher_mode=True)\n```\n\n## Visualize the effect of features on the target variables.\n```python\nplot_main(cga2m_no1,X_train)\n```\n![](https://raw.githubusercontent.com/MK-tech20/CGA2M_plus/main/images/plot_main.png) \n\n## Visualize (3d) the effect of pairs of features on the target variables\n```python\nplot_interaction(cga2m_no1,X_train,mode = "3d")\n```\n![](https://raw.githubusercontent.com/MK-tech20/CGA2M_plus/main/images/plot_pairs.png) \n## Feature importance\n```python\nshow_importance(cga2m_no1,after_prune=True,higher_mode=True)\n```\n![](https://raw.githubusercontent.com/MK-tech20/CGA2M_plus/main/images/feature_importance.png) \n# License\nMIT License\n# Citation\nYou may use our package(CGA2M+) under MIT License. \nIf you use this program in your research then please cite:\n\n**CGA2M+ Package**  \n```bash\n@misc{kuramata2021cga2mplus,\n  author = {Michiya, Kuramata and Akihisa, Watanabe and Kaito, Majima and Kensyo, Kondo and Kazuhide, Nakata},\n  title = {d3rlpy: An offline deep reinforcement library},\n  year = {2021},\n  publisher = {GitHub},\n  journal = {GitHub repository},\n  howpublished = {\\url{https://github.com/MK-tech20/CGA2M_plus}}\n}\n```\n\n**CGA2M+ Paper**  \nThe paper has not been published yet. \n\n# Reference\n[1] Friedman, J. H. 2001, Greedy function approximation: a gradient boosting machine, Annals of statistics, 1189-1232, doi: 10.1214/aos/1013203451. Available online: May 02, 2021\n\n[2] Ke, G., Meng, Q., Finley, T., Wang, T., Chen, W., Ma, W., ... Liu, T. Y. 2017. Lightgbm: A highly efficient gradient boosting decision tree, Advances in neural information processing systems(NIPS’17), Long Beach California , 4-9 December, pp. 3146-3154.\n\n[3] Nelder, J. A., Wedderburn, R. W. 1972. Generalized linear models, Journal of the Royal Statistical Society: Series A (General), 135(3), 370-384, doi: 10.2307/2344614, Available online: May 02, 2021\n\n[4] Hastie, T. J., Tibshirani, R. J. 1990. Generalized additive models (Vol. 43), CRC press, doi: 10.1214/ss/1177013604. Available online: May 02, 2021\n\n[5] Lou, Y., Caruana, R., Gehrke, J., Hooker, G. 2013, August. Accurate intelligible models with pairwise interactions, Proceedings of the 19th ACM SIGKDD international conference on Knowledge discovery and data mining(KDD’13), Chicago Illinois, United States of America, 11-14 August, pp. 623-631.\n\n[6] “GitHub - microsoft/LightGBM” [Online]. Available: https://github.com/microsoft/LightGBM (Accessed: May 02, 2021)\n\n[7] “scikit-learn: machine learning in Python — scikit-learn 0.24.2 documentation” [Online]. Available: https://scikit-learn.org/stable/ (Accessed May 02, 2021)\n',
    'author': 'Michiya, Kuramata',
    'author_email': 'baisgtud43j@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/MK-tech20',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
