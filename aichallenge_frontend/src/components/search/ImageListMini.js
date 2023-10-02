import React, { useEffect, useCallback } from "react";
import { useState } from "react";
import "./ImageList.module.css";
import {
  Row,
  Col,
  Container,
  Button
} from "reactstrap";
import "bootstrap/dist/css/bootstrap.min.css"; // Import the Bootstrap CSS file
import { Link} from "react-router-dom";
import { LazyLoadImage } from "react-lazy-load-image-component";

function ImageListMini({ dataListMini, clicked, query, setClickedImages }) {
  const handleImageIdx = useCallback((id) => {
    setClickedImages((prevList) => [...prevList, id]);
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
  const [images, setImages] = useState([]);
  useEffect(() => {
    let counter = 0;
    const im = Object.entries(dataListMini["minidata"]).map((item, index) => {
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
              onClick={() => handleImageIdx(item[0])}
            />
            <div style={{ position: "relative", bottom: "2rem", }}>
              <Link to={{
                pathname: `/knn/${index}`,
                search: `?clicked=true&imgPath=${item[0]}`
              }} target="_blank" rel="noopener noreferrer">
                <Button style={{fontSize: '6px', padding: '5px 8px'}} className="image-button btn-sm float-start">KNN</Button>
              </Link>
            </div>

            <div style={{ position: "relative", bottom: "2rem"}}>
                <Button style={{fontSize: '6px', padding: '5px 8px'}} onClick={() => handleMakeURL(item[0])} className="image-button btn-sm float-end">Show</Button>
            </div>
        </Col>
      );
    });
    setImages(im);
  }, [dataListMini, clicked, query]);

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