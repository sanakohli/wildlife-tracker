import React from "react";
import { MapContainer, TileLayer, GeoJSON } from "react-leaflet";
import { useState } from "react";
import "leaflet/dist/leaflet.css";
import countyGeoJson from "./counties.json";
import Timeline from "./Timeline";

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

export default function Map2() {
  const [hoveredCounty, setHoveredCounty] = useState(null);
  const [year, setYear] = React.useState(2010);
  const [population, setPopulation] = useState(null);

  const onEachFeature = (feature, layer) => {
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
        e.target.setStyle({ weight: 1, color: "black" });
      },
    });
  };
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
          data={countyGeoJson}
          onEachFeature={onEachFeature}
          style={{ weight: 1, color: "black" }}
        />
      </MapContainer>
      <Timeline year={year} setYear={setYear} />
    </div>
  );
}
