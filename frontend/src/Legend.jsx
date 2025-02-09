import React from "react";
import { Box, Slider, Card } from "@mui/material";

export default function Legend(props) {
  const marks = [
    {
      value: 2009,
      label: "2009",
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
    <Box
      sx={{
        height: "400px",
        position: "fixed",
        top: 150,
        left: 1100,
        // top: 100,
        // left: 600,
        zIndex: 1000,
        backgroundColor: "white",
        // paddingLeft: "40px",
        // paddingRight: "40px",
        // paddingBottom: "20px",
        padding: "0px 10px 20px 10px !important",
        borderRadius: "8px",
        display: "flex",
        justifyContent: "center",
        flexDirection: "row",
        textAlign: "center",
      }}
    >
      <div
        style={{
          height: "100%",
          display: "flex",
          alignItems: "center",
          flexDirection: "column",
        }}
      >
        <h4>Endangered</h4>
        <Box
          sx={{
            background: "linear-gradient(#EB7F70, #CBAD5F)",
            height: "85%",
            width: "15px",
            borderRadius: "8px",
          }}
        ></Box>
      </div>
      <div
        style={{
          height: "100%",
          display: "flex",
          alignItems: "center",
          flexDirection: "column",
          marginLeft: "20px",
        }}
      >
        <h4>Risk</h4>
        <Box
          sx={{
            background: "linear-gradient(#000035, #90d5ff)",
            height: "85%",
            width: "15px",
            borderRadius: "8px",
          }}
        ></Box>
      </div>
      <div style={{ height: "100%" }}>
        <h4>Years</h4>
        <Slider
          aria-label="Always visible"
          defaultValue={2010}
          getAriaValueText={valuetext}
          step={1}
          marks={marks}
          // valueLabelDisplay="auto"
          min={2009}
          max={2023}
          sx={{
            height: "85%",
            marginLeft: "24px",
            width: "10px",
          }}
          orientation="vertical"
        />
      </div>
    </Box>
  );
}
