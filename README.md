# Crime Analysis with Dashboard for the City of Los Angeles

This project analyzes **crime data for the City of Los Angeles** using a modular Python architecture and a fully interactive **Streamlit dashboard**.  
The original Jupyter Notebook has been fully refactored into clean, production-ready **.py modules** for reusability, scalability, and deployment.

---

## 🚀 Features

### Dataset:
https://catalog.data.gov/dataset/crime-data-from-2020-to-present

### Data Processing
- Clean and standardize the LA crime dataset  
- Handle missing values  
- Format and extract time-based features (`time_occ`, `hour`)  
- Drop redundant or unused columns  
- Normalize column names  

### Exploratory Data Analysis
- Crimes by area  
- Crimes by hour  
- Top location hotspots  
- Top crime types per area  
- Time vs Area heatmaps  

### Mapping & Geo Analysis
- Folium heatmap of crimes by area  
- Marker map showing top 5 crime locations by area  

### Interactive Streamlit Dashboard
- Sidebar filters  
- Summary statistics  
- Visualizations (bar charts, heatmaps)  
- Embedded Folium maps  
