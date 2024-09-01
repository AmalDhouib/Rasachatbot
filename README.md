This project is related to the previous one named "WebScrapping." This application collects essential data about French startups, including the name of the coordinator, the domain, the name of the startup, 
the number of likes, and the link to their websites. It also visualizes some results using histograms and other charts. The application detects the number of likes using machine learning regression algorithms.
To save time and energy, and to make things easier, I integrated a simple chatbot that answers questions related to the dataset. Users can query the chatbot, which reads the dataset line by line to provide 
accurate answers with a single message.
For web scraping, I used Selenium and BeautifulSoup, and the information was stored in an Excel file. For the machine learning algorithms, I used Linear Regression, SVM, Decision Tree Regressor, and Random Forest. 
After calculating the mean squared error (MSE) for each, Linear Regression was found to be the best-performing algorithm.
For the chatbot, I utilized the Rasa framework, and Flask was used for integrating the application to streamline the process.

Please make sure to install rasa before clonning the code!!!!

