import React from "react";
import { MapContainer, TileLayer, GeoJSON } from "react-leaflet";
import { useState, useCallback } from "react";
import "leaflet/dist/leaflet.css";
import countyGeoJson from "./counties.json";
import Legend from "./Legend";

// Function to fetch population data from the Census API
async function fetchPopulationData(state, county, year) {
  const apiKey = "bfc8ad381595852cdf120078d2bb4ce23679bed5";
  const url = `https://api.census.gov/data/${year}/acs/acs5?get=B01003_001E&for=county:${county}&in=state:${state}&key=${apiKey}`;

  try {
    const response = await fetch(url);
    const data = await response.json();
    const population = data[1][0];
    return population;
  } catch (error) {
    console.error("Error fetching population data:", error);
  }
}

export default function Map() {
  const [hoveredCounty, setHoveredCounty] = useState(null);
  const [year, setYear] = React.useState(2010);
  const [population, setPopulation] = useState(null);

  const onEachFeature = useCallback(
    (feature, layer) => {
      layer.on({
        mouseover: async (e) => {
          setHoveredCounty(feature.properties.NAME);
          e.target.setStyle({ weight: 3, color: "blue" });

          // Fetch population data for the hovered county
          const fetchedPopulation = await fetchPopulationData(
            feature.properties.STATEFP,
            feature.properties.COUNTYFP,
            year
          );

          if (fetchedPopulation !== null) {
            const popupContent = `<b>${feature.properties.NAME}</b><br><b>Population: ${fetchedPopulation}</b>`;
            e.target.bindPopup(popupContent).openPopup();
            setPopulation(fetchedPopulation);
          } else {
            const popupContent = `<b>${feature.properties.NAME}</b><br><b>Population data not available</b>`;
            e.target.bindPopup(popupContent).openPopup();
          }
        },
        mouseout: (e) => {
          setHoveredCounty(null);
        },
      });
    },
    [year] // Depend on the `year` state
  );
  const position = [30.2672, -97.7431]; // Default center position (Austin, TX)

  return (
    <div>
      <MapContainer
        center={position}
        zoom={7}
        style={{ height: "100vh", width: "100%" }}
      >
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution="&copy; OpenStreetMap contributors"
          opacity={0.3}
        />
        <GeoJSON
          key={year}
          data={countyGeoJson}
          onEachFeature={onEachFeature}
          opacity={0.6}
          style={{ weight: 1, color: "black" }}
        />
        <TileLayer
          url="https://api.gbif.org/v2/map/occurrence/adhoc/{z}/{x}/{y}@1x.png?style=scaled.circles&mode=GEO_CENTROID&locale=en&country=US&year=1990%2C2025&advanced=false&occurrenceStatus=present&iucnRedListCategory=EN&srs=EPSG%3A3857&squareSize=256"
          attribution='<a href="https://www.gbif.org">GBIF</a>'
          zoomOffset={-1}
          tileSize={512}
          opacity={1}
        />
      </MapContainer>
      <Legend year={year} setYear={setYear} />
    </div>
  );
}
