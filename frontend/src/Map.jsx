// src/Map.js
import React from "react";
import { useState, useEffect } from "react";
import { MapContainer, TileLayer } from "react-leaflet";
import { tileLayer } from "leaflet";
import "leaflet/dist/leaflet.css";
import Timeline from "./Timeline";

const openStreet = tileLayer(
  "https://api.gbif.org/v2/map/occurrence/density/{z}/{x}/{y}@1x.png?srs=EPSG:4326&taxonKey=212&bin=hex&hexPerTile=117&style=green-noborder.poly",
  { attribution: '<a href="https://www.gbif.org">GBIF</a>' }
);

const gbif = tileLayer(
  "https://api.gbif.org/v2/map/occurrence/density/{z}/{x}/{y}@1x.png?publishingCountry=US&year=2000,2030&style=fire.point",
  {
    attribution: '<a href="https://www.gbif.org">GBIF</a>',
    zoomOffset: -1,
    tileSize: 512
  }
);

export default function Map() {
  const position = [30.2672, -97.7431];
  const [map, setMap] = useState(null);

  useEffect(() => {
    if (!map) return;
    // map.addLayer(openStreet);
    console.log('use ');
    map.addLayer(gbif);
  }, [map]);

  return (
    <div style={{ height: "100vh", width: "100%" }}>
      <MapContainer
        center={position}
        zoom={7}
        ref={setMap}
        style={{ height: "100%", width: "100%" }}
      >
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        />
      </MapContainer>
      <Timeline></Timeline>
    </div>
  );
}
