import React, { useEffect } from "react";
import { useState } from "react";
import "./ImageList.module.css";
import {
  Row,
  Col,
  Container,
} from "reactstrap";
import "bootstrap/dist/css/bootstrap.min.css"; // Import the Bootstrap CSS file
import { Link} from "react-router-dom";
import { LazyLoadImage } from "react-lazy-load-image-component";

function ImageListMini({ dataList, clicked, query }) {
  const [images, setImages] = useState([]);
  useEffect(() => {
    let counter = 0;
    console.log( Object.entries(dataList["data"]))
    const im = Object.entries(dataList["data"]).map((item, index) => {
      return (
        <Col key={`${item}${++counter}` } 
        xs={6} sm={4} md={3} lg={2} style={{padding: "0px 2px", margin: "2px 0px"}}>
          <Link to={{
                pathname: `/knn/${index}`,
                search: `?clicked=${clicked}&query=${query}`
              }} target="_blank" rel="noopener noreferrer">
            <LazyLoadImage
              height="100%"
              width="100%"
              effect="opacity"
              src={`data:image/png;base64,${item[1]}`}
              alt={`Image ${counter}`}
            />
          </Link>
        </Col>
      );
    });
    setImages(im);
  }, [dataList, clicked, query]);

  return (
    <div>
            <Container>
                    <Row>{images}</Row>
            </Container>
    </div>
  );
}

// function ImageListRoutes() {
//   return (
//     <Routes>
//       <Route path="/knn/:id" element={<App />} />
//     </Routes>
//   );
// }

export default function ImageListWithRoutes(props) {
  return (
    <div>
      <ImageListMini {...props} />
    </div>
  );
}