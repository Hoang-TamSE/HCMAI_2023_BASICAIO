import React, { useEffect } from "react";
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

function ImageList({ dataList, clicked, query }) {
  const [images, setImages] = useState([]);

  useEffect(() => {
    let counter = 0;

    const im = Object.entries(dataList["data"]).map((item, index) => {
      return (
        <Col
          key={`${item}${++counter}`}
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
              src={`data:image/png;base64,${item[1]}`}
              alt={`Image ${counter}`}
            />
            <div style={{ position: "relative", bottom: "3.5rem"}}>
              <Link to={{
                pathname: `/knn/${index}`,
                search: `?clicked=true&imgPath=${item[0]}`
              }} target="_blank" rel="noopener noreferrer">
                <Button className="image-button btn-sm float-start">KNN</Button>
              </Link>
            </div>
        </Col>
      );
    });
    setImages(im);
  }, [dataList, clicked, query]);

  return (
    <div>
      <Container>
        <Row >{images}</Row>
      </Container>
    </div>
  );
}


// function ImageListRoutes({ dataList }) {
//   return (
//     <Routes>
//       <Route path="/knn/:id" element={<App data={dataList} />} />
//     </Routes>
//   );
// }

export default function ImageListWithRoutes(props) {
  return (
    <div>
      <ImageList {...props} />
      {/* <ImageListRoutes {...props} /> */}
    </div>
  );
}