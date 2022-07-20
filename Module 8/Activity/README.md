# Module 8 Activity
## Boston House-price

In this activity, you will develop a predictive model using a dataset.

Using the Boston House-price dataset available at the URL provided below, perform the following tasks using PySpark: 

Boston Housing dataset https://www.cs.toronto.edu/~delve/data/boston/bostonDetail.html


- Compute the pairwise **correlations of the variables**; 
- Select the **top three variables based on the pairwise correlations** of the variables; 
- Create a **regression model using a polynomial function of degree two** on the three selected variables. Use 70% of the data for training; 
- Compute the **R-Squared value of the model** using the remaining 30% of the test data; and 
- Discuss any challenges that you faced in performing the above tasks in the ‘Predictive Modelling’ discussion forum and reply to other students’ queries to help resolve their issues.

## Using the Boston Dataset 

For this example, we will use the Boston dataset, which contains data about the housing and price data in the Boston area. This dataset was taken from the StatLib library, which is maintained at Carnegie Mellon University. It is commonly used in machine learning, and it is a good candidate to learn about regression problems. The Boston dataset is available from a number of sources, but it is now available directly from the sklearn.datasets package. This means you can load it directly in Scikit-learn without needing explicitly to download it.