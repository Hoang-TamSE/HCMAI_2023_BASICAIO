import React, { useRef, useState, useEffect } from "react";
import classes from "./BoxStyle.module.css";
import Boxable from "./Boxable";
import CanvasDraw from 'react-canvas-draw';
import html2canvas from 'html2canvas';


export default function Box({ imagePaths = [], setImagePaths, setSketch, isEnabled }) {

  const firstCanvas = useRef(null);
  const boxRef = useRef(null);
  const captureArea = useRef(null);
  const [computedStyle, setComputedStyle] = useState(null);

  useEffect(() => {
    const element = boxRef.current;

    if (element) {
      const computedStyle = window.getComputedStyle(element);
      setComputedStyle(computedStyle)
    }
  }, [boxRef]);

  const clear = () => {
    firstCanvas.current.clear();
  };
  const undo = () => {
    firstCanvas.current.undo();
  };
  

  const handleDeleteImage = (index) => {
    const newImages = [...imagePaths];
    newImages.splice(index, 1);
    setImagePaths(newImages);
  };

  const capture = () => {
    const boxElement = captureArea.current;

    // Hide the capture button temporarily


    html2canvas(boxElement).then((canvas) => {
      // Convert the canvas to an image URL
      const imageUrl = canvas.toDataURL();

      // Perform any necessary action with the captured image URL
      if (isEnabled){
        setSketch(imageUrl)
      } else{
        setSketch(null)
      }

      // Restore the visibility of the capture button
    });
  };

 

  return (
    <div className={classes.box} ref={boxRef}>
      <div id="list-Button">
        <button onClick={clear}>Clear</button>
        <button onClick={undo}>Undo</button>
        <button id="capture-button" onClick={capture}>Capture</button>
      </div>
        <div ref={captureArea}>
        {imagePaths.map((imagePath, index) => (
          <React.Fragment key={index}>
            <Boxable
              targetKey="box"
              label={index}
              image={imagePath}
              onDelete={() => handleDeleteImage(index)}
              bottom= {computedStyle}
            />  
          </React.Fragment>
        ))}
        <CanvasDraw
        brushRadius={1}
        ref={firstCanvas}
        style={{ borderRadius: 1, border: '1px solid  black', margin: 'auto', width:"100%", height: "175px" }}
      />
        </div>
    </div>
  );
}