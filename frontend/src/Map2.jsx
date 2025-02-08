import React from "react";
import { MapContainer, TileLayer, GeoJSON } from "react-leaflet";
import { useState } from "react";
import "leaflet/dist/leaflet.css";
import countyGeoJson from "./counties.json";
import Timeline from "./Timeline";

export default function Map2() {
  const [hoveredCounty, setHoveredCounty] = useState(null);
  const [year, setYear] = React.useState(2010);

  const onEachFeature = (feature, layer) => {
    layer.on({
      mouseover: (e) => {
        setHoveredCounty(feature.properties.NAME);
        e.target.setStyle({ weight: 3, color: "blue" });
        const popupContent = `<b>${feature.properties.NAME}</b><b>${feature.properties.NAME}</b>`;
        e.target.bindPopup(popupContent).openPopup();
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
