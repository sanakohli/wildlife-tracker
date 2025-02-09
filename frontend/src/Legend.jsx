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
    <Card
      sx={{
        height: "400px",
        position: "fixed",
        top: 150,
        left: 1200,
        zIndex: 1000,
        backgroundColor: "white",
        // paddingLeft: "40px",
        // paddingRight: "40px",
        paddingBottom: "20px",
        // padding: "20px 10px 20px 10px",
        borderRadius: "8px",
        display: "flex",
        justifyContent: "center",
        flexDirection: "column",
        textAlign: "center",
      }}
    >
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
    </Card>
  );
}
