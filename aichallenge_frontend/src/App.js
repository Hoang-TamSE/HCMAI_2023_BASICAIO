import TextQueryForm from "./components/query/TextQueryForm";
import classes from "./App.module.css";
import Logo from "./components/query/Logo";
import ImageList from "./components/search/ImageList";
import React, { useState, useEffect } from "react";
import "../node_modules/rsuite/dist/rsuite.min.css";
import ImageListMini from "./components/search/ImageListMini";
import { useLocation } from "react-router-dom";
import IconList from "./components/drag/IconList";
import Box from "./components/drag/Box";
import Radio from "./components/drag/Radio";
import QueryFormForMiniImage from "./components/query/QueryFromForMiniImage";

function App() {
  const location = useLocation();
  const [dataList, setDataList] = useState({ data: {}});
  const [clicked, setClicked] = useState("false");
  const [query, setQuery] = useState(""); // <-- Add state for the query input
  const [imagePaths, setImagePaths] = useState([]);
  const [sketch, setSketch] = useState(null);
  const [isEnabled, setIsEnabled] = useState(true);
  const [isAnd, setIsAnd] = useState(true);
  const [imgPath, setImgPath] = useState("");
  const [clickedImages, setClickedImages] = useState([]);
  const [dataListMini, setDataListMini] = useState({ data: {}});


  // const location = useLocation();
  // const data = location.state?.dataList;

  // useEffect(() => {
  //   if (location.state && location.state.dataList) {
  //     setDataList(location.state.dataList);
  //   }
  // }, [location]);


  


  const fetch_image = async () => {
    const response = await fetch(`http://localhost:5000/imgPath`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({imgPath, isEnabled: isEnabled})

            });

    if (response.ok) {
        const data = await response.json();
        setDataList(data)
        console.log("aaaaaaaaaaaaa")
        // setDataList(data);
        // setQuery(query);
    }
};

useEffect(() => {
  const searchParams = new URLSearchParams(location.search);
  const isClicked = searchParams.get("clicked") === "true";  console.log(imgPath)
  if(isClicked && imgPath !== null && imgPath !== "") {
    fetch_image();
  }
}, [imgPath])

useEffect(() => {
    const searchParams = new URLSearchParams(location.search);
    setImgPath(searchParams.get("imgPath"))
}, []);

  // useEffect(() => {
  //   console.log(data)
  //   if (data !== null) {
  //     setDataList(JSON.parse(data));
  //   }
  // }, [data]);

  // useEffect(() => {
  //   if (dataList && dataList.data.length > 0) {
  //     localStorage.setItem("dataList", JSON.stringify(dataList));
  //   }
  // }, [dataList]);

  return (
    <div className={classes.container}>
      <div className={classes.search_space}>
        <Logo />
        
      {/* <IconList setImagePaths={setImagePaths}/>
      <Radio setIsEnabled={setIsEnabled}/>
      <Box isEnabled={isEnabled} imagePaths={imagePaths} setImagePaths={setImagePaths} setSketch={setSketch}/> */}
          <QueryFormForMiniImage setDataListMini={setDataListMini}/>
          <div className={classes.image_list_mini_container}>
            <ImageListMini dataListMini={dataListMini} clicked={clicked} query={query} />
          </div>
      
        
      </div>
      <div className={classes.result_space}>
  <div className={classes.header}>
    <TextQueryForm isEnabled={isEnabled} setDataList={setDataList} setClicked={setClicked} setQuery={setQuery} sketch={sketch} clickedImages={clickedImages} setClickedImages={setClickedImages} />
  </div>
  <div className={classes.imageListContainer}>
    <ImageList dataList={dataList} clicked={clicked} query={query} setClickedImages={setClickedImages} />
  </div>
</div>
    </div>
  );
}

export default App;