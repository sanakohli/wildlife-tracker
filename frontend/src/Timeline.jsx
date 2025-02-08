import React from "react";
import { Box, Slider, Card } from "@mui/material";

export default function Timeline(props) {
  const marks = [
    {
      value: 2009,
      label: "2000",
    },
    {
      value: 2016,
      label: "2016",
    },
    {
      value: 2023,
      label: "2023",
    },
  ];

  function valuetext(value) {
    props.setYear(value);
    return value;
  }

  return (
    <Card
      sx={{
        width: 500,
        position: "fixed",
        top: 550,
        left: 500,
        zIndex: 1000,
        backgroundColor: "white",
        // paddingLeft: "40px",
        // paddingRight: "40px",
        padding: "10px 40px 10px 40px",
        borderRadius: "8px",
        display: "flex",
        justifyContent: "center",
        flexDirection: "column",
        textAlign: "center",
      }}
    >
      <Slider
        aria-label="Always visible"
        defaultValue={2010}
        getAriaValueText={valuetext}
        step={1}
        marks={marks}
        valueLabelDisplay="auto"
        min={2009}
        max={2023}
        sx={{ height: "10px", marginTop: "24px" }}
      />
      <h3 style={{ margin: "5px" }}>Years</h3>
    </Card>
  );
}
