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
        width: "400px",
        position: "fixed",
        bottom: 15,
        right: 15,
        // top: 100,
        // left: 600,
        zIndex: 1000,
        backgroundColor: "white",
        // paddingLeft: "40px",
        // paddingRight: "40px",
        // paddingBottom: "20px",
        paddingTop: "5px",
        // padding: "0px 10px 20px 10px !important",
        borderRadius: "8px",
        display: "flex",
        justifyContent: "center",
        flexDirection: "column",
        textAlign: "center",
        alignContent: "center",
        alignItems: "center",
      }}
    >
      <div
        style={{
          width: "100%",
          display: "flex",
          alignItems: "center",
          flexDirection: "column",
        }}
      >
        <h4 style={{ marginTop: "5px", marginBottom: "10px" }}>Endangered</h4>
        <Box
          sx={{
            background: "linear-gradient(to left, #EB7F70, #CBAD5F)",
            width: "85%",
            height: "15px",
            borderRadius: "8px",
          }}
        ></Box>
        <div
          style={{
            width: "85%",
            display: "flex",
            justifyContent: "space-between",
          }}
        >
          <h6 style={{ margin: "2px" }}>Low Volume</h6>
          <h6 style={{ margin: "2px" }}>High Volume</h6>
        </div>
      </div>
      <div
        style={{
          width: "100%",
          display: "flex",
          alignItems: "center",
          flexDirection: "column",
        }}
      >
        <h4 style={{ marginTop: "5px", marginBottom: "10px" }}>Risk</h4>
        <Box
          sx={{
            background: "linear-gradient(to left, #000035, #90d5ff)",
            width: "85%",
            height: "15px",
            borderRadius: "8px",
          }}
        ></Box>
        <div
          style={{
            width: "85%",
            display: "flex",
            justifyContent: "space-between",
          }}
        >
          <h6 style={{ margin: "2px" }}>Low</h6>
          <h6 style={{ margin: "2px" }}>High</h6>
        </div>
      </div>
      <div style={{ width: "100%" }}>
        <h4 style={{ margin: "5px" }}>Years</h4>
        <Slider
          aria-label="Always visible"
          defaultValue={2010}
          getAriaValueText={valuetext}
          step={1}
          marks={marks}
          valueLabelDisplay="auto"
          min={2009}
          max={2023}
          sx={{
            width: "85%",
            height: "10px",
            marginTop: "2px",
          }}
          //   orientation="vertical"
        />
      </div>
    </Box>
  );
}
