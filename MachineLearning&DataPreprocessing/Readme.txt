1.To run these scripts, following python package needed to be installed

—- pandas (v0.14.1 or higher)
—- numpy (v1.8.0 or higher)
—- sklearn (v0.7.3 or higher )

2. Description of scripts

—-‘Get_data4ML_fromDB.py’ is used to extract data of benign and malicious websites from the database, compute statistics from the data, removes invalid data points, and store them in the following files: 
‘valid_simp_leg.pkl’   
'valid_simp_mal.pkl’
’valid_simplified_leg_stats_M.csv’
’valid_simplified_mal_stats_M.csv'
The execution might take several minutes due to the huge size of our database. 
You need to run this scripts on our virtual machine

—- ‘MachineLearning_Validation.py’ take 'valid_simp_leg.pkl’ and 'valid_simp_mal.pkl’ (outputs of ‘Get_data4ML_fromDB.py’) as inputs, train and validate our machine learning detector with the data, and output the results. (For convinience, we have also include'valid_simp_leg.pkl’ and 'valid_simp_mal.pkl’ in the same directory, so that you run this script directly) By default, the machine learning algorithm will use all the features that we mention in the paper. If you want to use only part of the features in the classifier, you can remove some features in the ‘used_feature’, which is located on the first row of the script. The following are the categories of these features:

source code change: ‘ave_ld','ave_nd'
image change: 'ave_imdiff4'
link information: ‘ave_links','ave_out'
social reputation: ’stumbleupon','twitter','linkedin','pininterest','fbcomment','googleplusone','fblike'


