# VizKG
VizKG is a Python library for Visualizing SPARQL Query Results over Knowledge Graphs.

Supported visualizations so far:
- Table
- ImageGrid
- Map
- Tree
- Timeline
- Dimensions
- Graph
- WordCloud
- Tree Map
- SunBurst Chart
- Line Chart
- Bar Chart
- Area Chart
- StackedArea Chart
- Histogram
- Density Plot
- Box Plot
- Violin Plot
- Bubble Chart
- Scatter Chart
- HeatMap

## Installation
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install VizKG.

```bash
pip install myKGlib
```

## Usage
```python
import myKGlib.vizkg as VizKG

sparql_query = """
    #images of cat
    #defaultView:ImageGrid
    SELECT ?item ?itemLabel ?pic
    WHERE
    {
    ?item wdt:P31 wd:Q146 .
    ?item wdt:P18 ?pic
    SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en" }
    }
    """
#to query another endpoint, change the URL for the service and the query
sparql_service_url = "https://query.wikidata.org/sparql"
chart = VizKG(sparql_query=sparql_query, sparql_service_url=sparql_service_url, chart='imageGrid')
chart.plot()
```