// src/Map.js
import React from "react";
import { useState, useEffect } from "react";
import { MapContainer, TileLayer, useMap } from "react-leaflet";
import { tileLayer } from "leaflet";
import "leaflet/dist/leaflet.css";
import L from "leaflet"; // Import Leaflet for using 'L' object
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
    tileSize: 512,
  }
);

// Function to fetch population data from the Census API
async function fetchPopulationData(fips) {
  const apiKey = "bfc8ad381595852cdf120078d2bb4ce23679bed5";
  const url = `https://api.census.gov/data/2021/acs/acs5?get=B01003_001E&for=county:${fips.substring(
    2
  )}&in=state:${fips.substring(0, 2)}&key=${apiKey}`;

  try {
    const response = await fetch(url);
    const data = await response.json();
    const population = data[1][0];
    return population;
  } catch (error) {
    console.error("Error fetching population data:", error);
  }
}

async function getCountyInfoFromLatLng(lat, lng) {
  const openCageApiKey = "1545c750cf764e909c009e78442f9ac7";
  const openCageUrl = `https://api.opencagedata.com/geocode/v1/json?q=${lat}+${lng}&key=${openCageApiKey}`;

  try {
    const response = await fetch(openCageUrl);
    const data = await response.json();

    const county = data.results[0]?.components?.county;
    const state = data.results[0]?.components?.state_code;
    const countyFips = data.results[0]?.annotations?.FIPS?.county;

    if (!county || !countyFips) {
      console.error("County or FIPS not found:", data);
      return { county: "Unknown", state: "Unknown", countyFips: null };
    }

    return { county, state, countyFips };
  } catch (error) {
    console.error("Error fetching county info:", error);
    return { county: "Unknown", state: "Unknown", countyFips: null };
  }
}

function HoverHandler() {
  const map = useMap();
  const [countyData, setCountyData] = useState({
    county: "",
    state: "",
    countyFips: "",
  });
  const [population, setPopulation] = useState(null);

  useEffect(() => {
    // Only fetch population data when county name changes
    if (countyData.county && countyData.countyFips) {
      fetchPopulationData(countyData.countyFips).then((population) => {
        setPopulation(population);
      });
    }
  }, [countyData]);

  useEffect(() => {
    const handleMouseOver = async (event) => {
      const latlng = event.latlng; // Latitude and Longitude of the mouse event
      const { county, state, countyFips } = await getCountyInfoFromLatLng(
        latlng.lat,
        latlng.lng
      );

      // Only update if county is different
      if (county !== countyData.county) {
        setCountyData({ county, state, countyFips });
        setPopulation(null); // Reset population before fetching new data
      }

      // Create and show popup
      const popup = L.popup()
        .setLatLng(latlng)
        .setContent(`You are hovering over ${county}, ${state}`)
        .openOn(map);

      // Update the popup with the population data after fetching
      if (population !== null) {
        popup.setContent(`County: ${county}<br>Population: ${population}`);
      }
    };

    // Add mouse event listener to the map
    map.on("mousemove", handleMouseOver);

    // Cleanup on component unmount
    return () => {
      map.off("mousemove", handleMouseOver);
    };
  }, [map, countyData, population]);

  return null;
}

export default function Map() {
  const position = [30.2672, -97.7431]; // Default center position (Austin, TX)
  const [map, setMap] = useState(null);

  const [year, setYear] = React.useState(2010);
  useEffect(() => {
    if (!map) return;
    // map.addLayer(openStreet);
    console.log("use ");
    map.addLayer(gbif);
  }, [map]);

  useEffect(() => {
    console.log(year);
  }, [year]);

  return (
    <div style={{ height: "100vh", width: "100%" }}>
      <MapContainer
        center={position}
        zoom={7}
        ref={setMap}
        style={{ height: "100%", width: "100%" }}
      >
        <TileLayer
          url="https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png"
          attribution="&copy; <a href='https://carto.com/'>CARTO</a>"
        />
        <HoverHandler /> {/* This component handles the hover events */}
      </MapContainer>
      <Timeline year={year} setYear={setYear} />
    </div>
  );
}
