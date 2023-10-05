import React, { useState } from "react";
import classes from "./TextQueryForm.module.css";


function TextQueryForm({ setDataList, setClicked, setQuery, sketch, isEnabled, clickedImages, setClickedImages }) {
    const [text, setText] = useState(""); // <-- Add state for the query input
    const [noti, setNoti] = useState("");
    const handleSubmission = (event) => {
        event.preventDefault();

        const fetch_image = async () => {
            const response = await fetch(`http://localhost:5000/`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({query: text, sketch: sketch, isEnabled: isEnabled})
            });

            if (response.ok) {
                const data = await response.json();
                setDataList(data)
            }
        };
        fetch_image();
    };

    const handleMakeFileSubmit = (event) => {
        event.preventDefault();

        const fetch_make_file = async () => {
            const response = await fetch(`http://localhost:5000/makefile`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({idx_images: clickedImages})
            });
            console.log(clickedImages)
            if (response.ok) {
                const data = await response.json();
                console.log("okiiii");
                alert(JSON.stringify(data)); // Display response in an alert
            }
        };
        fetch_make_file();
    };
    const handleClean = (event) => {
        event.preventDefault();
        console.log("aaaaaaaaaaaaaaaaaaaaaaaaa")
        setClickedImages([]);
    };

    const handleQueryChange = (event) => {
        setText(event.target.value); // <-- Update the query state when the input value changes
    };

    const handleDeleteLastValue = () => {
        setClickedImages((prevList) => prevList.slice(0, prevList.length - 1));
      };

    // ...

    return (
        <div>
            <form onSubmit={handleSubmission} className={classes.form}>
                <label className={classes.label}>Vietnamese Query</label>
                <input className={classes.input} type="text" value={text} onChange={handleQueryChange}/> 
                <button className={classes.scoreBtn}>Submit</button>
            </form>
            <div className={classes.form} >
                 <button onClick={handleMakeFileSubmit} className={classes.scoreBtn}>Make File</button>
                 <button onClick={handleClean} className={classes.scoreBtn}>Clean</button>
                 <button onClick={handleDeleteLastValue} className={classes.scoreBtn}>Undo</button>
                 <label  className={classes.label}>{clickedImages}</label>
            </div>


        </div>
    );
}

export default TextQueryForm;