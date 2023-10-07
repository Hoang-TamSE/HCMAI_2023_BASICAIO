import React, { useState } from "react";
import classes from "./TextQueryForm.module.css";


function QueryFormForMiniImage({ setDataListMini}) {
    const [text, setText] = useState(""); // <-- Add state for the query input
    const [object, setObject] = useState("");
    const [color, setColors] = useState(""); // <-- Add state for the query input

    const handleSubmission = (event) => {
        event.preventDefault();

        const fetch_image = async () => {
            const response = await fetch(`http://localhost:5000/getbyscript`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({text})
            });

            if (response.ok) {
                const data = await response.json();
                console.log('okiiiiii')
                console.log(data);
                setDataListMini(data.minidata);
            }
        };
        fetch_image();
    };

    const handleSubmissionExtra = (event) => {
        event.preventDefault();

        const fetch_image = async () => {
            const response = await fetch(`http://localhost:5000/getbyextra`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({"object": object,
                                    "color": color})
            });

            if (response.ok) {
                const data = await response.json();
                console.log('okiiiiii')
                console.log(data);
                setDataListMini(data.minidata);
            }
        };
        fetch_image();
    };

    // const handleMakeFileSubmit = (event) => {
    //     event.preventDefault();

    //     const fetch_make_file = async () => {
    //         const response = await fetch(`http://localhost:5000/makefile`, {
    //             method: "POST",
    //             headers: {
    //                 "Content-Type": "application/json"
    //             },
    //             body: JSON.stringify({idx_images: clickedImages})
    //         });
    //         console.log(clickedImages)
    //         if (response.ok) {
    //             console.log("okiiii")
    //         }
    //     };
    //     fetch_make_file();
    // };
    // const handleClean = (event) => {
    //     event.preventDefault();
    //     console.log("aaaaaaaaaaaaaaaaaaaaaaaaa")
    //     setClickedImages([]);
    // };

    const handleQueryChange = (event) => {
        setText(event.target.value); // <-- Update the query state when the input value changes
    };

    const handleQueryChangeObject = (event) => {
        setObject(event.target.value); // <-- Update the query state when the input value changes
    };
    const handleQueryChangeColor = (event) => {
        setColors(event.target.value); // <-- Update the query state when the input value changes
    };
    // const handleDeleteLastValue = () => {
    //     setClickedImages((prevList) => prevList.slice(0, prevList.length - 1));
    //   };

    // ...

    return (
        <div>
            <form onSubmit={handleSubmission} className={classes.form}>
                <label>Script</label>
                <input className={classes.input} type="text" value={text} onChange={handleQueryChange}/> 
            </form>
            {/* <div className={classes.form} >
                 <button onClick={handleMakeFileSubmit} className={classes.scoreBtn}>Make File</button>
                 <button onClick={handleClean} className={classes.scoreBtn}>Clean</button>
                 <button onClick={handleDeleteLastValue} className={classes.scoreBtn}>Undo</button>
                 <label  className={classes.label}>{clickedImages.length}</label>
            </div> */}
            <form className={classes.form} onSubmit={handleSubmissionExtra}>
                <label>Object</label>
                <input className={classes.input} type="text" value={object} onChange={handleQueryChangeObject}></input>
                <label>Color</label>
                <input className={classes.input} type="text" value={color} onChange={handleQueryChangeColor}></input>
                <button>Submit</button>
            </form>


        </div>
    );
}

export default QueryFormForMiniImage;