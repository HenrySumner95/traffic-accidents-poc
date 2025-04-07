import pandas as pd
import os

df = pd.DataFrame()

for file in os.listdir("data"):
    if "csv" in file:
        df = pd.concat([df, pd.read_csv(r"data/" + file, skiprows = 0)])

df = df.rename(columns = {
    "Unnamed: 0" : "admin",
    "Unnamed: 1" : "year",
    "Estimated number of road traffic deaths" : "Total number of deaths",
    "Estimated number of road traffic deaths.1" : "Number of deaths male",
    "Estimated number of road traffic deaths.2" : "Number of deaths female",
    "Estimated road traffic death rate (per 100 000 population)" : "Deaths per 100k",
    "Estimated road traffic death rate (per 100 000 population).1" : "Deaths per 100k (male)",
    "Estimated road traffic death rate (per 100 000 population).2" : "Deaths per 100k (female)"
    }
)

df = df.drop(df[df.year == "Year"].index)

display(df)

for col in df.columns:
    if col not in ["admin", "year"]:
        df[col] = df[col].str.extract(r'^([\d.]+)')
        if "per" in col:
            df[col] = df[col].astype(float)
        else:
            df[col] = df[col].astype(int)

rename_map = {"Bahamas" : "The Bahamas",
              "United Kingdom of Great Britain and Northern Ireland" : "United Kingdom",
              "Congo" : "Democratic Republic of the Congo",
              "Venezuela (Bolivarian Republic of)" : "Venezuela",
              "Iran (Islamic Republic of)" : "Iran",
              "Viet Nam" : "Vietnam",
              "Republic of Korea" : "South Korea",
              "Democratic People's Republic of Korea" : "North Korea",
              "Lao People's Democratic Republic" : "Laos",
              "Netherlands (Kingdom of the)" : "Netherlands",
              "Bolivia (Plurinational State of)" : "Bolivia",
              "Micronesia (Federated States of)" : "Micronesia",
              "Turkiye" : "Türkiye",
              "Cote d'Ivoire" : "Ivory Coast",
              "Brunei Darussalam" : "Brunei",
              "Syrian Arab Republic" : "Syria",
              "Russian Federation" : "Russia",
              "Republic of Moldova" : "Moldova"
             }

for k, v in rename_map.items():
    df = df.replace(to_replace = k, value = v)

df_latest = df[df["year"] == "2019"]
df_latest["rank"] = df_latest["Deaths per 100k"].rank()

display(df_latest.describe())

#why in the goddamn hell does the first bin need to be -0.1 in order to include 0 values? Beats me
df_latest["bin"] = pd.cut(df_latest["Deaths per 100k"], [-0.1, 8, 16, 25, 50, 100],
                          labels = ["#22c2fc",
                                    "#ffab00",
                                    "#c96a04",
                                    "#c41d1d",
                                    "#550000"])

print(json.dumps(dict(zip(df_latest["admin"], df_latest["bin"]))))
