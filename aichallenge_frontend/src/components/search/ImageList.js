import React, { useEffect, useCallback } from "react";
import { useState } from "react";
import { Link } from "react-router-dom";
import "./ImageList.module.css";
import {
  Row,
  Col,
  Container,
  Button,
  FormText
} from "reactstrap";
import {LazyLoadImage} from "react-lazy-load-image-component"
import "bootstrap/dist/css/bootstrap.min.css";

function ImageList({ dataList, clicked, query, setClickedImages }) {
  const [images, setImages] = useState([]);

  const handleImageIdx = useCallback((id) => {
    setClickedImages(id);
  }, [setClickedImages]);


  const handleMakeURL = (id) => {

    const fetch_make_file = async () => {
        const response = await fetch(`http://localhost:5000/geturl`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({id: id})
        });
        console.log(id)
        if (response.ok) {
            const data = await response.json();
            var url = data['data']
            window.open(url, "_blank");
            console.log("okiiii")
        }
    };
    fetch_make_file();
};

  useEffect(() => {
    let counter = 0;
    console.log(dataList)
    const im = dataList.map(([id, imageUrl], index) => {
      console.log(id)
      return (
        <Col
          key={`${id}${++counter}`}
          xs={6}
          sm={4}
          md={3}
          lg={2}
          style={{padding: "0px 2px", margin: "2px 0px"}}
        >
            <LazyLoadImage
              width="100%"
              height="100%"
              effect="opacity"
              src={`data:image/png;base64,${imageUrl}`}
              alt={`Image ${counter}`}
              onClick={() => handleImageIdx(id)}
            />
            <div style={{ position: "relative", bottom: "3.5rem"}}>
              <Link to={{
                pathname: `/knn/${index}`,
                search: `?clicked=true&imgPath=${id}`
              }} target="_blank" rel="noopener noreferrer">
                <Button className="image-button btn-sm float-start">KNN</Button>
              </Link>
            </div>

            <div style={{ position: "relative", bottom: "3.5rem"}}>
                <Button onClick={() => handleMakeURL(id)} className="image-button btn-sm float-end">Show</Button>
            </div>
        </Col>
      );
    });
    setImages(im);
  }, [dataList, clicked, query, handleImageIdx]);

  return (
    <div>
      <Container>
        <Row >{images}</Row>
      </Container>
    </div>
  );
}

export default function ImageListWithRoutes(props) {
  return (
    <div>
      <ImageList {...props} />
    </div>
  );
}