import React, { useContext, useState, useEffect } from "react";
import classes from "./TextQueryForm.module.css";


function TextQueryForm({ setDataList, setClicked, setQuery, sketch, isEnabled }) {
    const [imageList, setImageList] = useState({ data: [] });
    const [text, setText] = useState(""); // <-- Add state for the query input

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
                console.log(data);
                setDataList(data);
                console.log(data)
                setImageList(data);
                setClicked("true");
                setQuery(text);
            }
        };
        fetch_image();
    };

    const handleQueryChange = (event) => {
        setText(event.target.value); // <-- Update the query state when the input value changes
    };

    // ...

    return (
        <div>
            <form onSubmit={handleSubmission} className={classes.form}>
                <label className={classes.label}>Vietnamese Query</label>
                <input className={classes.input} type="text" value={text} onChange={handleQueryChange}/> 
                <button className={classes.scoreBtn}>Submit</button>
            </form>
        </div>
    );
}

export default TextQueryForm;