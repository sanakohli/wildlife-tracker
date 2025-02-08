import { MapContainer, TileLayer, GeoJSON } from "react-leaflet";
import { useState } from "react";
import "leaflet/dist/leaflet.css";
import countyGeoJson from "./counties.json";

export default function Map2() {
  const [hoveredCounty, setHoveredCounty] = useState(null);

  const onEachFeature = (feature, layer) => {
    layer.bindTooltip(feature.properties.name, { permanent: false });

    layer.on({
      mouseover: (e) => {
        console.log(feature.properties);
        setHoveredCounty(feature.properties.NAME);
        e.target.setStyle({ weight: 3, color: "blue" });
      },
      mouseout: (e) => {
        setHoveredCounty(null);
        e.target.setStyle({ weight: 1, color: "black" });
      },
      click: (e) => {
        const popupContent = `<b>${feature.properties.name}</b>`;
        e.target.bindPopup(popupContent).openPopup();
      },
    });
  };
  const position = [30.2672, -97.7431]; // Default center position (Austin, TX)

  return (
    <div>
      <MapContainer
        center={position}
        zoom={5}
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
      {/* {hoveredCounty && <div style={{ zIndex: 9999 }}>{hoveredCounty}</div>} */}
    </div>
  );
}
