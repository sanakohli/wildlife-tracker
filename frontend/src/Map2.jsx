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
        const popupContent = `<b>${feature.properties.NAME}</b><b>${feature.properties.NAME}</b>`;
        e.target.bindPopup(popupContent).openPopup();
      },
      mouseout: (e) => {
        setHoveredCounty(null);
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
      <Timeline year={year} setYear={setYear} />
    </div>
  );
}
