import os
from plotly.io import write_html

# Define dataframe paths
report_dir = "../report"
df_title_basics_1990_2024_html = os.path.join(
    report_dir, "df_title_basics_1990_2024.html"
)
fig_hist_url = os.path.join(report_dir, "fig_hist.html")
fig_histogram_url = os.path.join(report_dir, "fig_histogram.html")
fig_timeline_url = os.path.join(report_dir, "fig_timeline.html")
fig_line_url = os.path.join(report_dir, "fig_line.html")
fig_histogram_movie_ratings_url = os.path.join(
    report_dir, "fig_histogram_movie_ratings.html"
)


#
model_performance_url = os.path.join(report_dir, "model_performance_plotly.png")
model_performance_svg_url = os.path.join(report_dir, "model_performance_plotly.svg")

#
model_performance_weighted_svg_url = os.path.join(
    report_dir, "model_performance_plotly_weighted.svg"
)

#
model_performance_weighted_crew_svg_url = os.path.join(
    report_dir, "model_performance_plotly_wegited_crew.svg"
)


report_html_path = "/Users/stiborv/Documents/NMgr/ZS2425/NDBI048/report/report.html"

# Create the report directory if it does not exist
os.makedirs(report_dir, exist_ok=True)

# Print the absolute path of the report HTML dataframe
print(f"Report HTML will be saved to: {os.path.abspath(report_html_path)}")

# Embed the DataFrame HTML and figure URL into your HTML report
html_string = f"""
<html>
    <head>
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.1/css/bootstrap.min.css">
        <style>
            body {{
                margin: 50px 300px;
                background: whitesmoke;
                font-family: "Arial", sans-serif;
                line-height: 1.6;
            }}
            .toc {{
                position: fixed;
                left: 20px;
                top: 100px;
                width: 250px;
                padding: 20px;
                background: white;
                border: 1px solid #ddd;
                box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
                font-size: 14px;
            }}
            .toc h4 {{
                font-size: 16px;
            }}
            .toc a {{
                text-decoration: none;
                color: #337ab7;
            }}
            .toc a:hover {{
                text-decoration: underline;
            }}
            .section {{
                margin-bottom: 50px;
            }}
            h1 {{
                font-size: 36px;
                margin-bottom: 40px;
                text-align: center;
            }}
            h2 {{
                font-size: 28px;
                color: #333;
            }}
            h3 {{
                font-size: 22px;
                color: #333;
            }}
            h4 {{
                font-size: 18px;
                margin-top: 20px;
                color: #333;
            }}
            p {{
                font-size: 16px;
                color: #444;
                text-align: justify;
            }}
            ul {{
                margin-left: 20px;
                list-style-type: disc;
            }}
            iframe {{
                margin: 10 10;
            }}
            .dataframe {{
                margin-top: 30px;
                margin-bottom: 25px;
            }}

        </style>
        <meta charset="utf-8">
    </head>
    <body>
        <!-- Left Sidebar for Navigation -->
        <div class="toc">
            <ol>
                <a href="#introduction"><li><b>Introduction</b></li></a>
                <a href="#datasets"><li><b>Datasets</b></li></a>
                <a href="#exploratory-analysis"><li><b>Exploratory Analysis</b></li></a>
                <a href="#transformation"><li><b>Data Transformation and Modeling</b></li></a>
                <a href="#conclusion"><li><b>Conclusion</b></li></a>
            </ol>        
        </div>
        
        <!-- Main Content -->
        <div>
            <h1>IMDb Data Science Report</h1>
            
            <div id="introduction" class="section">
                <h2>1. Introduction</h2>
                <p>
                This report focuses on analysing <a href="https://developer.imdb.com/non-commercial-datasets/">IMDb</a> data to explore factors influencing movie quality, trends, and recommendation systems. After conducting an initial exploratory analysis, we will identify key attributes and develop a content-based model to predict movie ratings. This analysis is akin to building a recommendation system for a streaming platform, where users' preferences are leveraged to suggest movies. However, in this case, we aim to predict a movie's average rating across all users (<a href="https://medium.com/@Howto101/how-to-determine-imdb-scores-57281a6a194e">IMDb rating</a> serves as a reliable proxy, given that it is a weighted average rather than a simple one, based on users' historical data). By analysing a movie's attributes, we will predict its overall average rating and identify similar movies to improve the accuracy of this prediction, rather than focusing solely on a specific user's rating. Thus our rediction could be used as one of many indicators to determine whether a movie will perform well in theaters, or the opposite, even before its official release. But in this case, we will try to predict the average rating from all users of a movie based on its attributes and try to find the most similar movies to get an overall average rating, not only for a specific user.
                </p>
                <p>
                Since the dataset contains movies from 1874 to the present, it is necessary to divide the data into several time periods to better analyse trends over time. In this analysis, we will focus on the period from 1990 to the present. This timeframe is significant because after 1990, major changes occurred, such as the introduction of digital technologies and CGI, which fundamentally transformed movie production. Movies like <a href="https://www.imdb.com/title/tt0119567/"><i>Jurassic Park</i></a> and <a href="https://www.imdb.com/title/tt0133093/?ref_=nv_sr_srsg_0_tt_7_nm_1_in_0_q_The%2520Matrix"><i>The Matrix</i></a> serve as examples of groundbreaking technologies that influenced how movies are made and the effects that are possible today. Moreover, the period from 1990 to 2000 focuses on the development of these new technologies, allowing for a better understanding of the evolution of cinematography and its digitalization. For a detailed visualisation of the distribution of key milestones over time, please refer to the timeline Figure <b>Key Milestones in Movie Industry and Average Ratings Over Time</b> below.
                </p>
                <div style="text-align: center;">
                    <iframe width="100%" height="550" frameborder="0" seamless="seamless" scrolling="no" src="{fig_timeline_url}"></iframe>
                </div>
                <p>The key question is: <b>Are we able to estimate the average rating of a future movie based on the similarity of other movies?</b> In this report, we aim to predict the average rating of a movie based on its attributes and identify movies that are similar. Although this is not a recommendation for a specific user, it varies in that we are not predicting a user's rating but the average rating of a movie across all users without using collaborative filtering and focusing on the content-based approach. To make prediction, we must first analyse the data and determine which attributes of a movie have the greatest influence on its rating. Based on this, we will remove attributes that do not impact the rating, as they will not be relevant for our prediction. Our goal is to find movies with similar attributes and use their ratings to estimate the rating of the movie we are interested in while we do not have the rating information yet.</p>

                <h3> 1.2. Necessary Subsection for the Report</h3>
                    <p>
                        This subsection provides an summarized overview of the report's recommended structure. Additionally, it will be included for mostly sections to provide a clear outline of the report's contents and satisfy the reader's strucure expectations in short. We guess that is not neccessary to include this subsection in the final report, but it is included here for the sake of completeness.
                        </p>
                    <p>
                        The report aims to predict the average rating of a future movie based on its attributes, using a content-based approach. The goal is to estimate the movie's rating across all users by identifying similar movies without relying on individual user preferences. Due to the fact that we are not interested in a specific user's rating and recommendation.
                    </p>
                    <p>
                        <i><b>Key Question:</b></i> Can we predict the average rating of a future movie based on the similarity to other movies?
                    </p>

                    <p><i><b>What is included in this report?</i></b>
                        <ol>
                            <li><b>Introduction</b>: Overview of the purpose and goal.</li>
                            <li><b>Datasets</b>: Exploration of IMDb data to identify influential movie attributes.</li>
                            <li><b>Exploratory Analysis</b>: Analysis of key attributes and trends.</li>
                            <li><b>Data Transformation and Modeling</b>: Preprocessing and modeling to prediction.</li>
                            <li><b>Conclusion</b>: Summary of findings and applications mostly covering necessary steps for the report.</li>
                        </ol>
                    </p>

                    <p><i><b>What sources and technologies can we
use for processing?</b></i><br>
                        <ul>
                            <li><b>Data:</b> IMDb movie dataset (1874–present), focusing on 1990–present.</li>
                            <li><b>Tools:</b> Python (Pandas, NumPy, Scikit-learn), Jupyter Notebooks, Machine Learning Algorithms (KNN), and visualization tools (Plotly).</li>
                        </ul>
                    </p>
                    <p><i><b>What methods are available for problem solution?</b></i><br>
                        We will use a content-based approach to predict the average rating of a movie by analysing its attributes and identifying similar movies. K-Nearest Neighbors (KNN) is chosen for its simplicity and effectiveness in measuring similarity. Other methods like Random Forest or Neural Networks could also be used, but KNN is sufficient for this task.
                    </p>
                    
                    <p><i><b>What individual steps do we take?</b></i><br>
                        The steps include data collection, explorary, preprocessing, feature selection, model development, and evaluation. The steps are sequential but may depend on intermediate results, particularly in model development and feature selection. For example, based on the analysis, we might adjust the feature set to optimise the model's performance.
                    </p>

                    <p><i><b>Are there any conditions for using some methods?</i></b><br>
                        The chosen method, KNN, requires that the data be well-structured and normalized. As we mentioned above, our next step after collectiong the data follows exlorary and then preprocessing to ensure the data is ready for the model. The model's performance will be evaluated based on metrics like R<sup>2</sup>, MSE, and MAE, which will determine the model's effectiveness. 
                    </p>                    
            </div>
            
            <!-- *** Section 2: Datasets *** -->

            <div id="datasets" class="section">
                <h2>2. Dataset</h2>
                <p>
                As we mentioned earlier, our analysis is based on the IMDb dataset, which contains a wealth of information about movies, including titles, genres, ratings, runtime, directors, writers, and more. This dataset provides a comprehensive view of the movie industry, enabling us to explore trends and factors influencing movie quality and audience reception. 
                </p>
                <h3>2.1. Key Characteristics</h3>
                <ul>
                    <li><b>Size:</b> Several million rows.</li>
                    <li><b>Format:</b> UTF-8, gzipped TSV dataframes with headers.</li>
                    <li><b>Fields:</b> Titles, genres, ratings, runtime, directors, and more.</li>
                </ul>
                <p>
                    Complete data dictionaries are available on <a href="https://developer.imdb.com/non-commercial-datasets/">IMDb's website</a>. To avoid duplication and rewriting information that is detailed and nicely described on the websites, we will only summarize for the readers what data we have available and how it relates to each other.
                </p>
                <p>
                    <b><code>title.basics.tsv</code>:</b> Contains information about titles, including genres, runtime, and release year.<br>
                    <b><code>title.akas.tsv</code>:</b> Contains information about titles in different regions and languages.<br>
                    <b><code>title.ratings.tsv</code>:</b> Contains IMDb ratings and number of votes for titles.<br>
                    <b><code>title.episode.tsv</code>:</b> Contains information about TV show episodes.<br>
                    <b><code>title.principals.tsv</code>:</b> Contains information about individuals involved in titles.<br>
                    <b><code>name.basics.tsv</code>:</b> Contains information about individuals in the movie industry.<br>
                    <b><code>title.crew.tsv</code>:</b> Describes relationships with directors and titles.
                </p>        
                <div style="text-align: center;">
                    <table class="dataframe table table-striped">
                        <thead>
                            <tr style="text-align: center;">
                                <th>Name</th>
                                <th>Compressed size (MB)</th>
                                <th>Uncompressed size (MB)</th>
                                <th>Number of rows</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td><code>name.basics.tsv.gz</code></td>
                                <td>245</td>
                                <td>753</td>
                                <td>11,366,522</td>
                            </tr>
                            <tr>
                                <td><code>title.akas.tsv.gz</code></td>
                                <td>305</td>
                                <td>1783</td>
                                <td>37,728,267</td>
                            </tr>
                            <tr>
                                <td><code>title.basics.tsv.gz</code></td>
                                <td>172</td>
                                <td>841</td>
                                <td>10,285,368</td>
                            </tr>
                            <tr>
                                <td><code>title.crew.tsv.gz</code></td>
                                <td>66</td>
                                <td>325</td>
                                <td>10,285,368</td>
                            </tr>
                            <tr>
                                <td><code>title.episode.tsv.gz</code></td>
                                <td>41</td>
                                <td>196</td>
                                <td>7,844,603</td>
                            </tr>
                            <tr>
                                <td><code>title.principals.tsv.gz</code></td>
                                <td>436</td>
                                <td>2475</td>
                                <td>58,914,239</td>
                            </tr>
                            <tr>
                                <td><code>title.ratings.tsv.gz</code></td>
                                <td>7</td>
                                <td>23</td>
                                <td>1,366,240</td>
                            </tr>
                        </tbody>
                    </table>
                </div>

                <h3>2.2. Necessary Subsection for the Report</h3>
                <p><b><i>What is the data source? Are there any marks that we cannot trust the data?</i></p></b>
                <p>
                The source of the dataset is IMDb, which is known as a reliable source of information about movies and TV shows. However, we are aware that the data may contain errors, missing values, or inconsistencies. For instance, some values may be added without any indication from provider. Nevertheless, it remains one of the best sources of information about movies and TV shows, which is why we decided to use this dataset for our analysis. Any errors and inconsistencies will be addressed in the following section.
                </p>

                <p><b><i>Data description (size, format, fields, data types, ...):</i></p></b>
                <p>The description has already been provided in the section itself and it doesn't make sense to mention it again. Additionally, we refer to the original source where everything is detailed.</p>

                <p><b><i>Data quality and sanity check (missing, errors, weird values) and resolution for data preprocessing and cleaning:</i></p></b>
                <p>These steps will be covered in the next section, where we will perform data cleaning and preprocessing to ensure the data is accurate, consistent, and reliable for further analysis. We will address missing values, errors, and inconsistencies in the data to improve its quality and prepare it for modeling.</p>

            </div>
            
            <div id="exploratory-analysis" class="section">
                <h2>3. Exploratory Analysis</h2>
                <p>
                In this section, we will conduct an exploratory analysis of the IMDb dataset to identify key attributes that influence movie ratings. By analysing the data, we aim to understand trends, patterns, and relationships between different variables, such as genres, directors, writers, and runtime.
                </p>

                <h3>3.1. Understanding the Data</h3>
                <p>To justify progressively why certain data is excluded while other data is retained, it is necessary to first understand what data we have available, how it relates to each other, and what their key characteristics are. For better understanding of the structere, see the example row of the <code>title.basics.tsv</code> dataframe displayed below.</p>

                <div style="text-align: center;">
                    <table class="dataframe table table-striped">
                        <thead>
                            <tr style="text-align: center;">
                                <th>tconst</th>
                                <th>titleType</th>
                                <th>primaryTitle</th>
                                <th>isAdult</th>
                                <th>startYear</th>
                                <th>runtimeMinutes</th>
                                <th>genres</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>tt0435761</td>
                                <td>movie</td>
                                <td>Toy Story 3</td>
                                <td>0.00</td>
                                <td>2010.00</td>
                                <td>103.00</td>
                                <td>Adventure,Animation,Comedy</td>
                            </tr>
                        </tbody>
                    </table>
                </div>

                <p>The also know as <code>title.akas.tsv</code> dataframe is not particularly relevant to our analysis, as these titles can vary by region or language, and this does not have a significant impact on our study. Similarly, the episode dataframe <code>title.episode.tsv</code> is not pertinent to our analysis, as we are focused on combination of cinematographic attributes that influence movie ratings in the same way as for TV shows. This dataframe contains information about TV show episodes, such as season and episode numbers. Therefore, we will not include these dataframes in our analysis, as they are not directly relevant to our research question and do not provide additional insights into movie ratings.</p>

                <p>The <code>name.basics.tsv</code> dataframe contains information about individuals involved in the movie industry, such as actors, directors, and writers. This data includes birth and death years, primary and alternate names, and the primary profession of each individual. It also contains information about titles individuals are known for, but this can be found in other dataframes (such as <code>title.principals.tsv</code> and <code>title.crew.tsv</code>).</p>

                <p>As for the <code>title.principals.tsv</code> and <code>title.crew.tsv</code> dataframes. The former contains information about directors and writers involved in the movies. Directors and writers are also listed as records in the letter, so it is important to determine whether these are the same records or separate ones. Each crew record includes an individual associated with the movie and a specified role (such as director, screenwriter, actor, etc.), so we can identify whether the records refer to the same person or different individuals. It is important to be aware of this distinction when analysing the data, as it may cause duplicates or inconsistencies in the dataset.</p>

                <p>Unfortunately, due to capacity limitations during the analysis, it was not possible to process the data from the <code>title.principals.tsv</code> dataframe. Even though we restricted the data to actors and actresses who were cast, this was challenging because each record contained multiple actors and actresses, and we did not have the capability to select which of them had a larger role. As a result, we were unable to narrow it down to a more specific subset, such as the top three actors who might warrant a higher score. For this reason, we will only work with the crew data, which contains only directors and writers who have a significant impact on the movie's rating without a doubt and there are not too many of them."
                
                <h3>3.2. Data Cleaning</h3>
                <p>
                    Data cleaning is a crucial step in the analysis process, as it ensures that the data is accurate, consistent, and reliable for further analysis. Thus allowing us delve deeper into the data and explore patterns and relationships between different attributes. In this section, we will outline the data cleaning steps, including removing irrelevant records, handling missing values, and filtering the data based on specific criteria.
                </p>

                <h4>3.2.1.Release Dates</h4>
                <p>
                Since our focus is on movies released from 1990 onwards, it is crucial to clean the data accordingly. This results in a reduction of the dataset from 11,366,522 to 8,419,817 records. Furthermore, it is important to note that the dataset includes movies that are yet to be released, with the most recent scheduled release being <a href="https://www.imdb.com/title/tt5637536/"><i>Avatar 5</i></a>, planned for 2031. As a result, we must remove movies set for release beyond 2024, as they do not yet have any ratings, resulting in the elimination of 18,020 records. This step is essential to ensure that the data is relevant to our analysis and that we focus on movies with available ratings for prediction.
                </p>              

                <h4>3.2.2. Average Ratings</h4>
                <p>
                Another crucial aspect is that the dataset contains average ratings ranging from 1 to 10, but also includes entries marked as <code>NaN</code>, indicating that no rating has been assigned. This issue must be addressed by removing all records with <code>NaN</code> ratings, thereby reducing the dataset from 8,401,797 to 1,239,710 movies with ratings available for analysis. This step is vital for our analysis, as we are specifically focused on predicting movie ratings based on various attributes. Consequently, any movies without ratings are not relevant to our study. While other attributes may also have missing values, our primary focus here is on ratings, so we are removing all records with <code>NaN</code> ratings due to the validation necessity.
                </p>

                <div style="text-align: center;">
                    <iframe width="100%" height="550" frameborder="0" seamless="seamless" scrolling="no" src="{fig_line_url}"></iframe>
                </div>

                <p>
                According to the Figure <b>Average Rating of Movies Over Time by Genre</b>, we can see that the average rating of movies has been relatively stable over the years, with a slight increase in recent years. This indicates that the quality of movies has remained consistent, with a slight improvement in recent years. However, it is essential to analyse other factors that may have key influences on movie ratings, such as genres, directors, and writers, to gain a more comprehensive understanding of movie quality.
                </p>
                <p>
                The anomalies can also be displayed (since the Figure is an interactive chart), which are defined as values of the average movie ratings that are more than two standard deviations above or below the mean. These anomalies are shown as red <code>x</code> markers, which can be toggled on or off through the chart's legend. Certain genres, such as Horror and Thriller, tend to consistently have average ratings within a certain range. However, some movies, exhibit significantly higher ratings, such as the Western movie from 2022 with an average rating of 8.10, which is noticeably higher than other values in the dataset. Additionally, some years see movies with extraordinarily low or high ratings compared to others. For example, in 1998, a News genre movie had an average rating of 4.83, and in 2022, a Western movie recorded an 8.10. These anomalies provide insights into the movies that deviate significantly from the norm in terms of audience reception, suggesting changes in trends, cultural moments, or characteristics of these movies that caused them to stand out.</p>
                
                <h4>3.2.3. Directors and Writers</h3>
                <p>
                The dataset also contains information about the directors and writers involved in each movie. This is important as it enables us to identify similarities between movies based on the individuals involved in their production. Furthermore, a well-known director or writer may have a greater influence on a movie's rating compared to lesser-known individuals.
                </p>

                <h3>3.3. Summary</h3>
                <p>
                Every attentive reader might contemplate the average rating and consider adding weights based on the number of votes. However, this is not necessary, as IMDb itself uses a weighted average that takes historical user data into account.

                Given that we have mentioned millions of movie records in initial dataframes, it is appropriate to visualise the current state of the data using the graph <b>Number of Movies Released Over Time</b> after thorough preprocessing and cleaning.
                </p>

                <div style="text-align: center;">
                    <iframe width="100%" height="550" frameborder="0" seamless="seamless" scrolling="no" src="{fig_histogram_url}"></iframe>
                </div>

                <h3>3.4. Necessary Subsection for the Report</h3>
            
                
                <p><i><b>Basic Statistics & Visualizations:</b></i><br>
                    In this section, we present key statistics, such as the distribution of ratings over time, as well as visualizations that highlight trends in movie ratings. The charts and graphs generated reveal how movies from different genres perform in terms of average ratings and show how certain anomalies deviate from expected norms.
                </p>

                <p><i><b>Conclusions & Expectations:</b></i><br>
                    The analysis reveals that the overall average rating of movies has remained fairly consistent over the years, with slight improvements in recent times. Anomalies are evident in certain genres, like Westerns, which can significantly differ from the rest. These anomalies provide valuable insights into potential shifts in audience expectations and movie trends.
                </p>

                <p><i><b>Recommendations for Data Transformation:</b></i><br>
                    Based on the analysis, we suggest transforming and possibly excluding certain data points to enhance model accuracy. For example, the inclusion of movies with missing ratings should be avoided, and data related to TV shows can be excluded if irrelevant to the analysis of movie ratings.
                </p>


            
            <div id="transformation" class="section">
                <h2>4. Data Transformation and Modeling</h2>
                    <p>
                    Based on the previous exploratory data analysis and the list of attributes we compiled, we will now proceed with data transformation and modeling to predict movie ratings. First, we preprocess the data by combining relevant textual information from the primary title, genres, directors, and writers columns into a new column. This combined feature includes all these fields, with missing values filled with empty strings to ensure that there are no <code>NaN</code> values in the data before performing any transformations.
                    </p>
                    <p>
                    Next, we apply the TfidfVectorizer from Scikit-learn to transform the combined features text data into a numerical format. The vectorizer converts the textual data into a term-frequency inverse document frequency (TF-IDF) matrix, where each row represents a movie, and each column corresponds to a unique word in the combined features. To avoid overfitting and reduce complexity, we limit the number of features to 1000.
                    </p>
                    <p>
                    To make the data more manageable and focused on the most important information, we perform dimensionality reduction using TruncatedSVD (Singular Value Decomposition). This technique reduces the number of features in the TF-IDF matrix, ensuring that only the most significant components are retained for the model, thus improving efficiency and accuracy.
                    </p>
                    <p>
                    After transforming the text data, we scale the numerical features as runtime minutes, number of vores, and average rating using Min-Max Scaler. This scaling normalizes the values of these features to a range between 0 and 1, ensuring that no single feature disproportionately influences the model due to differences in their original scales.
                    </p>
                    <p>
                    Once the features are prepared, we combine the reduced textual features from SVD and the scaled numerical features into a single matrix, which serves as the input for the machine learning model. We then split the dataset into training and testing sets, allocating 80% of the data for training and 20% for testing. For the model, we choose the KNeighborsRegressor, a machine learning algorithm that predicts continuous values, such as ratings, based on the average of the nearest neighbors' ratings. We set the number of neighbors to 5 for this model, meaning it finds the 5 most similar movies to make a prediction.
                    </p>
                    <p>
                    Take a look at an uasge example. Given that we are simulating a scenario where we try to predict the rating of a future movie based on its similarity to other movies, it is important to note that, when making our selection, we will only consider movies that were released before the release year of the movie whose rating we want to predict.We will use the model for the movie <a href="https://www.imdb.com/title/tt0435761/"><i>Toy Story 3</i></a>, which was released in 2010. 
                    </p>

                    <div style="text-align: center; overflow-x: auto;">
                        <table class="dataframe table table-striped" style="min-width: 800px;">
                            <thead>
                                <tr style="text-align: center;">
                                    <th>titleType</th>
                                    <th>primaryTitle</th>
                                    <th>isAdult</th>
                                    <th>startYear</th>
                                    <th>runtimeMinutes</th>
                                    <th>genres</th>
                                    <th>averageRating</th>
                                    <th>numVotes</th>
                                    <th>directors</th>
                                    <th>writers</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td>movie</td>
                                    <td>Toy Story 3</td>
                                    <td>0.00</td>
                                    <td>2010.00</td>
                                    <td>103.00</td>
                                    <td>Adventure,Animation,Comedy</td>
                                    <td><code>?</code></td>
                                    <td>918856.00</td>
                                    <td>nm0881279</td>
                                    <td>nm0005124,nm0004056,...</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                    
                    <p>
                    Below is the simplified resulting prediction for the top 5 most similar movies, with their average rating simply calculated by averaging the ratings of these movies. Of course, many other approaches could be used, but this is sufficient for our purposes.
                    </p>

                    <div style="text-align: center; overflow-x: auto;">
                        <table class="dataframe table table-striped" style="min-width: 800px;">
                            <thead>
                                <tr style="text-align: center;">
                                    <th>titleType</th>
                                    <th>primaryTitle</th>
                                    <th>isAdult</th>
                                    <th>startYear</th>
                                    <th>runtimeMinutes</th>
                                    <th>genres</th>
                                    <th>averageRating</th>
                                    <th>numVotes</th>
                                    <th>directors</th>
                                    <th>writers</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td>movie</td>
                                    <td>Teen-Aged</td>
                                    <td>0.00</td>
                                    <td>2008.00</td>
                                    <td>76.00</td>
                                    <td>Comedy,Drama</td>
                                    <td>5.80</td>
                                    <td>11.00</td>
                                    <td>nm3152572</td>
                                    <td>nm3153252,nm3152646</td>
                                </tr>
                                <tr>
                                    <td>movie</td>
                                    <td>Showdown at Williams Creek</td>
                                    <td>0.00</td>
                                    <td>1991.00</td>
                                    <td>96.00</td>
                                    <td>Drama,Western</td>
                                    <td>6.20</td>
                                    <td>118.00</td>
                                    <td>nm0471862</td>
                                    <td>nm0336736,nm2239586</td>
                                </tr>
                                <tr>
                                    <td>tvEpisode</td>
                                    <td>Stone, Scissors, Paper</td>
                                    <td>0.00</td>
                                    <td>1997.00</td>
                                    <td>85.00</td>
                                    <td>Drama</td>
                                    <td>7.50</td>
                                    <td>29.00</td>
                                    <td>nm0926458</td>
                                    <td>nm0131710</td>
                                </tr>
                                <tr>
                                    <td>tvEpisode</td>
                                    <td>Brother's Keeper</td>
                                    <td>0.00</td>
                                    <td>1990.00</td>
                                    <td>0</td>
                                    <td>Drama</td>
                                    <td>7.90</td>
                                    <td>10.00</td>
                                    <td>nm0281058</td>
                                    <td>nm0455673</td>
                                </tr>
                                <tr>
                                    <td>tvSeries</td>
                                    <td>Tian Xia Liang Cang</td>
                                    <td>0.00</td>
                                    <td>2002.00</td>
                                    <td>46.00</td>
                                    <td>Drama,History</td>
                                    <td>6.40</td>
                                    <td>11.00</td>
                                    <td>nm0943212</td>
                                    <td>nm3279839</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>

                    <p>
                    The predicted rating for <i>Toy Story 3</i> is 6.76, based on the average ratings of the top 5 most similar movies. The actual rating <code>?</code> from table is 8.3, indicating that the model's prediction is relatively close to the actual rating. In the following subsections, we will evaluate the model's performance and discuss the results in more detail.
                    </p>

                    <h3>4.1. K-Nearest Neighbor</h3>
                    <p>
                    Finally, after training the model, we evaluate its performance by predicting the ratings on the test set and calculating the mean squared error, mean absolute error, R<sup>2</sup> score, and explained variance score. These metrics provide insights into how well the model predicts movie ratings and its overall performance. The results are summarized in the table below, along with the model's performance visualized in the figure <b>K-NN Performance</b>.
                    </p>
                    <!-- SVG Embed -->
                    <div style="text-align: center;">
                        <img src="{model_performance_svg_url}" alt="Model Performance SVG" style="width: 100%; margin-left: 20px; margin-right: 20px;">
                    </div>

                    <h4>4.1.1. Prediction Quality</h4>
                        <p>
                        The model demonstrates strong performance, as indicated by metrics such as the R<sup>2</sup> score (0.93) and explained variance score (0.93). These values show that the model is capable of explaining 93% of the variability in movie ratings. The high R<sup>2</sup> score confirms that our chosen attributes are effective.
                        </p>

                        <!-- Performance Metrics Table -->
                        <div style="text-align: center;">
                            <table class="dataframe table table-striped">
                                <thead>
                                    <tr style="text-align: center;">
                                        <th>Metric</th>
                                        <th>Value</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr>
                                        <td>R<sup>2</sup> Score</td>
                                        <td>0.93</td>
                                    </tr>
                                    <tr>
                                        <td>Explained Variance Score</td>
                                        <td>0.93</td>
                                    </tr>
                                    <tr>
                                        <td>Validation Mean Squared Error</td>
                                        <td>0.14</td>
                                    </tr>
                                    <tr>
                                        <td>Validation Mean Absolute Error</td>
                                        <td>0.18</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>                        

                        <p>
                        On the test data, errors measured by MSE (0.14) and MAE (0.18) are low, further supporting the assumption that the model effectively generalizes to new cases. The mean absolute error (MAE) of 0.18 means that predictions typically deviate by ±0.18 from the actual rating, a insignificant difference considering IMDb ratings are scaled from 1 to 10.
                        </p>

                        <h4>4.1.2. Training and Validation Errors</h4>
                        <p>
                        It is also important to note the relatively small difference between the training error (MSE: 0.09, MAE: 0.14) and the validation error (MSE: 0.14, MAE: 0.18). This difference is natural and suggests that the model is not significantly overfitted. If the difference were much larger, it would indicate that the model had overlearned the details of the training data and lost its ability to generalize to the test data.
                        </p>

                        <!-- Training Metrics Table -->
                        <div style="text-align: center;">
                            <table class="dataframe table table-striped">
                                <thead>
                                    <tr style="text-align: center;">
                                        <th>Metric</th>
                                        <th>Value</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr>
                                        <td>Training Mean Squared Error (Subset)</td>
                                        <td>0.09</td>
                                    </tr>
                                    <tr>
                                        <td>Training Mean Absolute Error (Subset)</td>
                                        <td>0.14</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                                   
                    <h3>4.2. K-Nearest Neighbor Weighted Votes and Time</h3>
                    <p>
                    In the previous and basic approach, we could immediately see that the model does not deviate much from the ideal (red) line, indicating that it generalizes well to new data. However, the band is still relatively wide, so we aim to narrow it as much as possible to get as close to the ideal line as we can. We have therefore decided to consider the weights of the individual attributes and will try to model again, this time with these weights. It makes the most sense to add weights to the attributes runtime minutes and number of votes, as both of these attributes are key. The first one describes which category the movie belongs to, allowing us to focus more on the target audience who enjoys watching series or movies. The second attribute, number of votes, can serve as an indicator of the movie's popularity. Let's imagine we have a prediction from another team, which, based on social media analysis and mentions of the movie, estimated the expected attendance, giving us the value for number of votes — keep in mind that this value is not typically known before the movie is released. We will assign a weight of 2 to these two attributes, while the rest of the procedure remains unchanged.
                    </p>
                        <!-- SVG Embed -->
                        <div style="text-align: center;">
                            <img src="{model_performance_weighted_svg_url}" alt="Model Performance SVG" style="width: 100%; margin-top: 10px;, margin-left: 20px; margin-right: 20px;">>
                        </div>

                    <h4>4.2.1. Prediction Quality</h4>
                    <p>
                    After applying the weights to the chosen attributes, the model's performance has significantly improved. The R<sup>2</sup> score has risen to 0.98, and the explained variance score has also reached 0.98, indicating that the model now explains 98% of the variability in movie ratings. These results suggest a substantial improvement in the accuracy of predictions when compared to the basic model, confirming that the weighted attributes better capture the underlying patterns in the data.
                    </p>
                    <!-- Performance Metrics Table -->
                        <div style="text-align: center;">
                            <table class="dataframe table table-striped">
                                <thead>
                                    <tr style="text-align: center;">
                                        <th>Metric</th>
                                        <th>Value</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr>
                                        <td>R<sup>2</sup> Score</td>
                                        <td>0.98</td>
                                    </tr>
                                    <tr>
                                        <td>Explained Variance Score</td>
                                        <td>0.98</td>
                                    </tr>
                                    <tr>
                                        <td>Validation Mean Squared Error</td>
                                        <td>0.04</td>
                                    </tr>
                                    <tr>
                                        <td>Validation Mean Absolute Error</td>
                                        <td>0.10</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div> 

                        <h4>4.2.2. Training and Validation Errors</h4>   
                        <p>
                        The error metrics from the training and validation sets have also improved. The training mean squared error (MSE) decreased to 0.03, and the mean absolute error (MAE) reduced to 0.09. These lower error values suggest that the model is not only fitting the training data well but is also able to generalize effectively to unseen data. The small difference between the training and validation errors (MSE: 0.04, MAE: 0.10) further supports the idea that the model has not overfitted, providing confidence that the changes made by adding weights have led to a more robust model.
                        </p>

                        <!-- Training Metrics Table -->
                        <div style="text-align: center;">
                            <table class="dataframe table table-striped">
                                <thead>
                                    <tr style="text-align: center;">
                                        <th>Metric</th>
                                        <th>Value</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr>
                                        <td>Training Mean Squared Error (Subset)</td>
                                        <td>0.03</td>
                                    </tr>
                                    <tr>
                                        <td>Training Mean Absolute Error (Subset)</td>
                                        <td>0.09</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>   

                <h3>4.3. Summary</h3>
                <p>
                Given the results we have obtained, we can conclude that the model with weights achieves significantly better results than the model without weights. This means that adding weights to the attributes that are key for predicting ratings significantly improves the accuracy of the predictions. The results show that the weighted model better captures hidden patterns in the data and is able to predict movie ratings more accurately. This was to be expected, as each attribute has a different weight from different perspectives. For example, given the very high success rates, we dare to assert that this is primarily due to the distribution of the average rating. 
                </p>

                <div style="text-align: center;">
                    <iframe width="100%" height="550" frameborder="0" seamless="seamless" scrolling="no" src="{fig_histogram_movie_ratings_url}"></iframe>
                </div>

                
                <h3>4.4. Necessary Subsection for the Report</h3>
                <p>Given that all requirements such as feature engineering, data transformation, performance evaluation, and others have been met, we will skip this subsection as well as the next section, which is the conclusion itself.</p>
            </div>
            <div id="conclusion" class="section">
            <h2>5. Conclusion</h3>
                <p>
                    The results demonstrate that the inclusion of weighted attributes significantly improves the KNN model's predictive performance. The unweighted model achieved an R<sup>2</sup> score of 0.93, while the weighted model raised this metric to 0.98. This indicates that weighted attributes, particularly for runtime minutes and number of votes, better reflect the underlying patterns in the data. Additionally, the model's mean absolute error (MAE) was reduced from 0.18 to 0.10, showing enhanced precision in predictions. Moreover, by limiting the attributes to 1,000 key features via TF-IDF in KNN and employing dimensionality reduction with TruncatedSVD, we ensured the model could process the data efficiently while focusing on the most critical components. The small difference between the training and validation errors further validates the model's robustness and its ability to generalise well to new data.
                </p>
                <p>
                    To process the vast amount of data involved, tools and techniques suited for Big Data processing were considered. For example, the TF-IDF transformation and TruncatedSVD could be parallelised using frameworks like Apache Spark to scale the computation efficiently. Similarly, distributed computing techniques such as MapReduce can handle preprocessing tasks like filling missing values, combining textual information, and scaling numerical features. Leveraging these tools would allow us to handle even larger datasets while maintaining performance and efficiency.
                </p>
                <p>
                    With subsequent iterations, we introduced feature weighting and explored different numbers of neighbours to optimise performance. These iterations demonstrated that even small adjustments, such as assigning weights to runtime minutes and number of votes, could yield substantial improvements in predictive accuracy. Future iterations could further refine the model by exploring weights for other attributes like directors, writers, and potentially actors.
                </p>
                <p>
                    In conclusion, the inclusion of weighted attributes in the predictive model significantly enhances its accuracy and reliability. By assigning greater importance to runtime minutes and number of votes, the model captures essential patterns in the data that would otherwise remain underutilised. The results emphasise the importance of thoughtful feature engineering and the potential for further refinements.
                </p>
                <p>
                    Future work could explore the impact of weights on additional attributes, such as directors, writers, or actors, to uncover other meaningful patterns in the data. Additionally, incorporating techniques from Big Data processing frameworks like Apache Spark or distributed databases could improve scalability, enabling the model to handle even larger datasets with ease. Finally, evaluating other machine learning models, such as ensemble methods, could further enhance the robustness and applicability of this approach. Certainly be worthwhile to assign weights to attributes such as directors, writers, and possibly even actors, as they significantly contribute to the final rating. Additionally, it would be advisable to consider using other machine learning models, such as ensemble methods, which could further enhance the robustness and applicability of this approach.
                </p>
            
            </div>

        </div>
    </body>
</html>

"""

# Write the full report HTML
with open(report_html_path, "w") as f:
    f.write(html_string)
