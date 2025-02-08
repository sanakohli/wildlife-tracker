import React from "react";
import { Box, Slider, Card } from "@mui/material";

export default function Timeline() {
  const marks = [
    {
      value: 1990,
      label: "1990",
    },
    {
      value: 2010,
      label: "2010",
    },

    {
      value: 2030,
      label: "2030",
    },
  ];

  function valuetext(value) {
    return `${value}`;
  }

  return (
    <Box
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
        step={10}
        marks={marks}
        // valueLabelDisplay="on"
        min={1990}
        max={2030}
        sx={{ height: "7px" }}
      />
      <h3 style={{ margin: "5px" }}>Years</h3>
    </Box>
  );
}
