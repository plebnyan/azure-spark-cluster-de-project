import pycountry
from fuzzywuzzy import process
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType
import pycountry_convert as pcc
import plotly.express as px

spark = SparkSession.builder.appName("viz").getOrCreate()

df = spark.read.csv('input/visa_number_in_japan.csv',header=True,inferSchema=True)

#Clean & standanize the column names
new_column_names = [col_name.replace(' ', '_')
                    .replace('/', '')
                    .replace('.', '')
                    .replace(',', '')
                    for col_name in df.columns]
df = df.toDF(*new_column_names)

#clean null values
df= df.dropna(how='all')


#transform dataset
df = df.select('year','country','number_of_issued_numerical')


def correct_country_name(name, threshold=85):
    countries = [country.name for country in pycountry.countries]
    corrected_name,score = process.extractOne(name, countries)

    if score >= threshold:
        return corrected_name
    return name
def get_continent_name(country_name):
    try:
        country_code = pcc.country_name_to_country_alpha2(country_name, cn_name_format='default')
        continent_code = pcc.country_alpha2_to_continent_code(country_code)
        return pcc.convert_continent_code_to_continent_name(continent_code)
    except:
        return None




correct_country_name_udf= udf(correct_country_name, StringType())

df =df.withColumn('country',correct_country_name_udf(df['country']))

#country name transalation
country_corrections = {
    'Andra': 'Russia',
    'Antigua Berbuda': 'Antigua and Barbuda',
    'Barrane': 'Bahrain',
    'Brush': 'Bhutan',
    'Komoro': 'Comoros',
    'Benan': 'Benin',
    'Kiribass': 'Kiribati',
    'Gaiana': 'Guyana',
    'Court Jiboire': "Côte d'Ivoire",
    'Lesot': 'Lesotho',
    'Macau travel certificate': 'Macao',
    'Moldoba': 'Moldova',
    'Naure': 'Nauru',
    'Nigail': 'Niger',
    'Palao': 'Palau',
    'St. Christopher Navis': 'Saint Kitts and Nevis',
    'Santa Principa': 'Sao Tome and Principe',
    'Saechel': 'Seychelles',
    'Slinum': 'Saint Helena',
    'Swaji Land': 'Eswatini',
    'Torque menistan': 'Turkmenistan',
    'Tsubaru': 'Zimbabwe',
    'Kosovo': 'Kosovo'
}

df =df.replace(country_corrections, subset='country')
continent_udf = udf(get_continent_name, StringType())

df = df.withColumn('continent', continent_udf(df['country']))


df.createGlobalTempView('japan_visa')

df_cont = spark.sql("""
    SELECT year, continent, sum(number_of_issued_numerical) visa_issued
    FROM global_temp.japan_visa
    WHERE continent IS NOT NULL
    GROUP BY year, continent
""")

df_cont = df_cont.toPandas()

fig = px.bar(df_cont, x='year', y='visa_issued', color='continent', barmode='group')

fig.update_layout(title_text="Number of visa issued in Japan between 2006 and 2017",
                  xaxis_title='Year',
                  yaxis_title='Number of visa issued',
                  legend_title='Continent')

fig.write_html('output/visa_number_in_japan_continent_2006_2017.html')
spark.stop()