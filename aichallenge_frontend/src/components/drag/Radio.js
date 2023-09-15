import { useState } from "react";

export default function Radio({setIsEnabled}) {
    const [isEnabled, setIsEnabled_2] = useState(true);
    const [isAnd, setIsAnd] = useState(true);
    
    const handleEnableChange = (e) => {
        setIsEnabled(e.target.value === "enable");
        setIsEnabled_2(e.target.value === "enable");

      };
    
      const handleLogicChange = (e) => {
        setIsAnd(e.target.value === "and");
      };

    return(
        <div style={{ display: "inline-flex" }}>
        <div style={{ margin: 10,
       }}>
          <label style={{marginRight: 5}}>
            <input
              type="radio"
              value="enable"
              checked={isEnabled}
              onChange={handleEnableChange}
            />
            Enable
          </label>

          <label>
            <input
              type="radio"
              value="disable"
              checked={!isEnabled}
              onChange={handleEnableChange}
            />
            Disable
          </label>
        </div>
        <div style={{
            borderRight: "1px solid black",
            height: 30
        }}></div>


        <div
          style={{
            margin: 10,
          }}
        >
          <label style={{marginRight: 5}}>
            <input
              type="radio"
              value="and"
              checked={isAnd}
              onChange={handleLogicChange}
            />
            AND
          </label>

          <label>
            <input
              type="radio"
              value="or"
              checked={!isAnd}
              onChange={handleLogicChange}
            />
            OR
          </label>
        </div>
      </div>
    )
}