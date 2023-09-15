import React, { useEffect, useState } from "react";
import {

    Button
  } from "reactstrap";
import classes from "./BoxStyle.module.css";

function IconList({ setImagePaths }) {
  const [imageNames, setImageNames] = useState([]);

  useEffect(() => {
    function importAll(r) {
        return r.keys().map((fileName) => `${process.env.PUBLIC_URL}/img/${fileName.replace("./", "")}`);
      }
      
      const images = importAll(require.context("../../../public/img", false, /\.(png|jpe?g|svg)$/));
      setImageNames(images);
  }, []);

  const handleImageClick = (imagePath) => {
    setImagePaths((prevList) => [...prevList, imagePath]);
  };

  return (
    <div>
      <div className={classes.button_list}>
        <Button style={{marginRight: 5}}>Clean</Button>
        <Button>Un-Clean</Button>
      </div>
      <div style={{ display: "inline-block" }}>
        {imageNames.map((imagePath, index) => (
          <React.Fragment key={index}>
            <img
              src={imagePath}
              height="45"
              style={{ margin: 2, cursor: "pointer" }}
              onClick={() => handleImageClick(imagePath)}
              alt={index}
            />
          </React.Fragment>
        ))}
      </div>
    </div>
  );
}

export default IconList;