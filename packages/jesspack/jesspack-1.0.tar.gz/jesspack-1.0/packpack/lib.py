import plotly.express as px
import pandas as pd

def try_me(lat1,lon1):
    d = {'latitude': [lat1], 'longitude': [lon1]}
    df = pd.DataFrame(d)
    fig = px.scatter_geo(lat= df['latitude'], lon= df['longitude'], 
                    title="Dans quel pays d'Europe suis-je ?",
                    scope="europe"
                    )
    fig.show()


if __name__ == "__main__":
    # Le Wagon location
    lat1, lon1 = 42.964566102966174, 12.067718901964664
    #Insert your coordinates from google maps here
    im_here = try_me(lat1,lon1)
    print(im_here)